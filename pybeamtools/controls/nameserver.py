import asyncio
import functools
import logging
import time
import warnings
from typing import Annotated

import caproto as ca
import requests
import uvicorn
from caproto import CaprotoKeyError, CaprotoNetworkError, ChannelType, MAX_UDP_RECV, \
    RemoteProtocolError, get_environment_variables
from caproto._commands import Beacon, read_datagram
from caproto.asyncio.server import AsyncioAsyncLayer
from caproto.asyncio.utils import AsyncioQueue, _DatagramProtocol, _TaskHandler, _UdpTransportWrapper, \
    _create_udp_socket
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class CustomBroadcaster(ca.Broadcaster):
    def recv(self, byteslike, address):
        try:
            commands = read_datagram(byteslike, address, self.their_role)
        except RemoteProtocolError:
            raise
        except Exception as ex:
            raise RemoteProtocolError(f'Broadcaster malformed packet received:'
                                      f' {ex.__class__.__name__} {ex}') from ex

        tags = {'their_address': address,
                'direction': '<<<---',
                'role': repr(self.our_role)
                }
        for command in commands:
            tags['bytesize'] = len(command)
            for address in self.our_addresses:
                tags['our_address'] = address
                if isinstance(command, Beacon):
                    log = self.beacon_log
                else:
                    log = self.log
                if isinstance(command, ca.SearchRequest):
                    if command.name.startswith('AOP:'):
                        log.info(f"SearchRequest {command.name}")
                # log.debug("%r", command, extra=tags)
        return commands


class DefaultContext:
    def __init__(self, pvdb, interfaces=None):
        if interfaces is None:
            interfaces = ca.get_server_address_list()
        self.interfaces = interfaces
        self.udp_socks = {}  # map each interface to a UDP socket for searches
        self.pvdb = pvdb
        self.log = logging.getLogger('caproto.ctx')

        self.addresses = []
        self.broadcaster = CustomBroadcaster(our_role=ca.SERVER)
        self.environ = get_environment_variables()

        # ca_server_port: the default tcp/udp port from the environment
        self.ca_server_port = self.environ['EPICS_CA_SERVER_PORT']
        # the specific tcp port in use by this server
        self.port = None

        self.log.debug('EPICS_CA_SERVER_PORT set to %d. This is the UDP port '
                       'to be used for searches, and the first TCP server port'
                       ' to be tried.', self.ca_server_port)

        ignore_addresses = self.environ['EPICS_CAS_IGNORE_ADDR_LIST']
        self.ignore_addresses = ignore_addresses.split(' ')

        self.broadcaster_datagram_queue = AsyncioQueue(
                ca.MAX_COMMAND_BACKLOG
        )
        self.command_bundle_queue = asyncio.Queue(
                ca.MAX_COMMAND_BACKLOG
        )

        self.server_tasks = _TaskHandler()

    async def _core_broadcaster_loop(self, udp_sock):
        while True:
            try:
                bytes_received, address = await udp_sock.recvfrom(
                        MAX_UDP_RECV
                )
            except ConnectionResetError:
                # Win32: "On a UDP-datagram socket this error indicates
                # a previous send operation resulted in an ICMP Port
                # Unreachable message."
                #
                # https://docs.microsoft.com/en-us/windows/win32/api/winsock/nf-winsock-recvfrom
                self.log.debug('UDP server recvfrom error')
            except OSError:
                self.log.exception('UDP server recvfrom error')
            else:
                if bytes_received:
                    await self._broadcaster_recv_datagram(bytes_received, address)

    async def _broadcaster_recv_datagram(self, bytes_received, address):
        try:
            commands = self.broadcaster.recv(bytes_received, address)
        except RemoteProtocolError as ex:
            self.log.debug('_broadcaster_recv_datagram: %s', ex, exc_info=ex)
        else:
            await self.command_bundle_queue.put((address, commands))

    async def broadcaster_queue_loop(self):
        '''Reference broadcaster queue loop implementation

        Note
        ----
        Assumes self.command_bundle_queue functions as an async queue with
        awaitable .get()

        Async library implementations can (and should) reimplement this.
        '''
        while True:
            try:
                addr, commands = await self.command_bundle_queue.get()
                await self._broadcaster_queue_iteration(addr, commands)
            except asyncio.CancelledError:
                break
            except Exception as ex:
                self.log.exception('Broadcaster command queue evaluation failed',
                                   exc_info=ex)

    def __iter__(self):
        # Implemented to support __getitem__ below
        return iter(self.pvdb)

    def __getitem__(self, pvname):
        try:
            return self.pvdb[pvname]
        except KeyError as ex:
            try:
                (rec_field, rec, field, mods) = ca.parse_record_field(pvname)
            except ValueError:
                raise ex from None

            if not field and not mods:
                # No field or modifiers, but a trailing '.' is valid
                return self.pvdb[rec]

        # Without the modifiers, try 'record[.field]'
        try:
            inst = self.pvdb[rec_field]
        except KeyError:
            # Finally, access 'record', see if it has 'field'
            try:
                inst = self.pvdb[rec]
            except KeyError:
                raise CaprotoKeyError(f'Neither record nor field exists: '
                                      f'{rec_field}')

            try:
                inst = inst.get_field(field)
            except (AttributeError, KeyError):
                raise CaprotoKeyError(f'Neither record nor field exists: '
                                      f'{rec_field}')

        # Verify the modifiers are usable BEFORE caching rec_field in the pvdb:
        # if ca.RecordModifiers.long_string in (mods or {}):
        #     if inst.data_type not in (ChannelType.STRING,
        #                               ChannelType.CHAR):
        #         raise CaprotoKeyError(
        #                 f'Long-string modifier not supported with types '
        #                 f'other than string or char ({inst.data_type})'
        #         )

        # Cache record.FIELD for later usage
        self.pvdb[rec_field] = inst
        return inst

    async def _broadcaster_queue_iteration(self, addr, commands):
        self.broadcaster.process_commands(commands)
        if addr in self.ignore_addresses:
            return

        search_replies = []
        version_requested = False
        for command in commands:
            if isinstance(command, ca.VersionRequest):
                version_requested = True
            elif isinstance(command, ca.SearchRequest):
                pv_name = command.name
                if not pv_name.startswith('AOP:'):
                    continue
                try:
                    known_pv = self[pv_name]
                except KeyError:
                    known_pv = None
                    (rec_field, rec, field, mods) = ca.parse_record_field(pv_name)
                    if rec in self.pvdb:
                        known_pv = self.pvdb[rec]
                        self.log.info(f'SearchRequest for %s - FOUND FALLBACK', pv_name)
                        self.log.info(f'Parse {(rec_field, rec, field, mods)}')
                    else:
                        self.log.info(f'SearchRequest for %s - NOT FOUND', pv_name)
                        self.log.info(f'Parse {(rec_field, rec, field, mods)}')

                if known_pv is not None:
                    # responding with an IP of `None` tells client to get IP
                    # address from the datagram.
                    pv_addr, pv_port, timeout = known_pv #self.pvdb[pv_name]
                    # if negative timeout, it is a permanent mapping
                    if 0 < timeout < time.time():
                        self.log.debug('SearchRequest for %s - ENTRY TOO OLD', pv_name)
                        continue
                    self.log.info(f'SearchRequest for %s - REPLYING {pv_addr}:{pv_port}', pv_name)
                    search_replies.append(
                            ca.SearchResponse(pv_port, pv_addr, command.cid,
                                              ca.DEFAULT_PROTOCOL_VERSION)
                    )

        if search_replies:
            if version_requested:
                bytes_to_send = self.broadcaster.send(ca.VersionResponse(13),
                                                      *search_replies)
            else:
                bytes_to_send = self.broadcaster.send(*search_replies)

            for udp_sock in self.udp_socks.values():
                try:
                    await udp_sock.sendto(bytes_to_send, addr)
                except OSError as exc:
                    host, port = addr
                    raise CaprotoNetworkError(f"Failed to send to {host}:{port}") from exc

    async def _create_broadcaster_transport(self, interface):
        """Create broadcaster transport on the given interface."""
        old_transport = self.udp_socks.pop(interface, None)
        if old_transport is not None:
            try:
                old_transport.close()
            except OSError:
                self.log.warning(
                        "Failed to close old transport for interface %s", interface
                )

        sock = _create_udp_socket()
        sock.bind((interface, self.ca_server_port))
        transport, _ = await asyncio.get_running_loop().create_datagram_endpoint(
                functools.partial(_DatagramProtocol, parent=self,
                                  identifier=interface,
                                  queue=self.broadcaster_datagram_queue),
                sock=sock,
        )
        self.udp_socks[interface] = _UdpTransportWrapper(transport)
        self.log.debug('UDP socket bound on %s:%d', interface,
                       self.ca_server_port)

    async def broadcaster_receive_loop(self):
        # UdpTransport -> broadcaster_datagram_queue -> command_bundle_queue
        queue = self.broadcaster_datagram_queue
        while True:
            interface, data, address = await queue.async_get()
            if isinstance(data, OSError):
                # Win32: "On a UDP-datagram socket this error indicates a
                # previous send operation resulted in an ICMP Port Unreachable
                # message."
                #
                # https://docs.microsoft.com/en-us/windows/win32/api/winsock/nf-winsock-recvfrom
                # However, asyncio will stop sending callbacks after this with no way to
                # resume. See: https://github.com/python/cpython/issues/88906
                # So recreate the socket here and hope for the best:
                await self._create_broadcaster_transport(interface)
            elif isinstance(data, Exception):
                self.log.exception(
                        "Broadcaster failed to receive on %s",
                        interface, exc_info=data
                )
            else:
                await self._broadcaster_recv_datagram(data, address)

    async def run(self, *, log_pv_names=False, startup_hook=None):
        self.log.info('Asyncio server starting up...')

        for interface in self.interfaces:
            await self._create_broadcaster_transport(interface)

        self.server_tasks.create(self.broadcaster_receive_loop())
        self.server_tasks.create(self.broadcaster_queue_loop())

        async_lib = AsyncioAsyncLayer()

        if startup_hook is not None:
            self.log.debug('Calling startup hook %r', startup_hook.__name__)
            self.server_tasks.create(startup_hook(async_lib))

        self.log.info('Server startup complete.')
        if log_pv_names:
            self.log.info('PVs available:\n%s', '\n'.join(self.pvdb))

        return self.server_tasks.tasks


class Mapping(BaseModel):
    channel: str
    address: str #IPv4Address
    port: Annotated[int, Field(strict=True, ge=1024, le=65535)]
    timeout: Annotated[float, Field(strict=True, gt=0, le=120)]


class PublishMessage(BaseModel):
    mappings: list[Mapping]


class NSServer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.router = APIRouter()
        self.router.add_api_route("/ns", self.update_item, methods=["PUT"])
        self.router.add_api_route("/ns_bulk", self.update_items, methods=["POST"])
        self.router.add_api_route("/del_bulk", self.remove_items, methods=["POST"])
        self.router.add_api_route("/list", self.list_items, methods=["GET"])
        self.logger = logging.getLogger(__name__)

    async def update_item(self, channel: str, address: str, port: int, timeout: float):
        self.logger.info(f"NSSERVER | Update item [{channel}] [{address}] [{port}] [{timeout}]")

        if not 0 < timeout <= 120:
            self.logger.error(f"NSSERVER | Timeout invalid for {channel}")
            raise HTTPException(status_code=403, detail=f"Timeout invalid for {channel}")
        if not channel.startswith('AOP:'):
            raise HTTPException(status_code=403, detail="Channel must start with AOP:")
        self.ctx.pvdb[channel] = (address, port, time.time() + timeout)
        return {"status": 1}

    async def update_items(self, msg: PublishMessage):
        updates = {}
        for mapping in msg.mappings:
            # Pydantic should catch this first
            if not 0 < mapping.timeout <= 120:
                self.logger.error(f"NSSERVER | Timeout invalid for {mapping.channel}")
                raise HTTPException(status_code=403, detail=f"Timeout invalid for {mapping.channel}")
            if not mapping.channel.startswith('AOP:'):
                raise HTTPException(status_code=403, detail="Channel must start with AOP:")
            updates[mapping.channel] = (mapping.address, mapping.port, time.time() + mapping.timeout)
            self.logger.info(f"NSSERVER | Update item [{mapping.channel}] [{mapping.address}] [{mapping.port}] [{mapping.timeout}]")
        self.ctx.pvdb.update(updates)
        return {"status": 1}

    async def remove_items(self, channels: list[str]):
        self.logger.info(f"NSSERVER | Remove {channels}")
        for channel in channels:
            # Don't error on missing channels
            self.ctx.pvdb.pop(channel, None)
        return {"status": 1}

    async def list_items(self):
        return self.ctx.pvdb

class NSClient:
    def __init__(self, nameserver='cadmus.aps4.anl.gov', port=6064):
        self.ns_addr = nameserver
        self.ns_port = port
        self.s = requests.Session()
        self.s.trust_env = False
        logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)

    def publish_channel(self, channel: str, address: str, port: int, timeout: float):
        url = f"http://{self.ns_addr}:{self.ns_port}/ns"
        data = {"channel": channel, "address": address, "port": port, "timeout": timeout}
        r = self.s.put(url, params=data, timeout=0.2)
        assert r.status_code == 200, f"Error {r.status_code} {r.text} when updating NS"
        assert r.json()['status'] == 1
        return r.json()

    def publish_channels(self, channels: list[str], address: str, port: int, timeout: float):
        r = self.s.post(f"http://{self.ns_addr}:{self.ns_port}/ns_bulk",
                    json={"mappings": [{"channel": c, "address": address, "port": port, "timeout": timeout} for c in
                                       channels]},
                        timeout=0.2)
        assert r.status_code == 200, f"Error {r.status_code} {r.text} when updating NS"
        assert r.json()['status'] == 1
        return r.json()

    def remove_channels(self, channels: list[str]):
        r = self.s.post(f"http://{self.ns_addr}:{self.ns_port}/del_bulk",
                        json=channels,
                        timeout=0.2)
        assert r.status_code == 200, f"Error {r.status_code} {r.text} when removing channels"
        assert r.json()['status'] == 1
        return r.json()

    def list_channels(self):
        r = self.s.get(f"http://{self.ns_addr}:{self.ns_port}/list")
        assert r.status_code == 200, f"Error {r.status_code} {r.text} when listing channels"
        return r.json()

logger = logging.getLogger(__name__)


async def start_uvicorn(host=None):
    host = host or '0.0.0.0'
    config = uvicorn.Config(app, port=6064, host=host, timeout_keep_alive=125)
    server = uvicorn.Server(config)
    return asyncio.create_task(server.serve())
    # loop.run_until_complete(server.serve())


async def start_nameserver(pvdb, *, epics_interfaces=None,
                           api_host=None,
                           log_pv_names=False,
                           startup_hook=None
                           ):
    ctx = DefaultContext(pvdb, epics_interfaces)
    srv = NSServer(ctx)
    app.include_router(srv.router)

    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    logger.info(f"Routes: {url_list}")

    loop = asyncio.get_running_loop()
    # asyncio.set_event_loop(loop)

    t1l = await ctx.run(log_pv_names=log_pv_names, startup_hook=startup_hook)
    logger.info(f'{t1l=}')
    t2 = await start_uvicorn(api_host)
    logger.info(f'{t2=}')

    tasks = [*t1l, t2]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.info('Server task cancelled. Will shut down.')
        # await tasks.cancel_all()
        await ctx.server_tasks.cancel_all()
        return
    except Exception:
        logger.exception('Server error. Will shut down')
        raise
    finally:
        ctx.log.info('Server exiting....')
        shutdown_tasks = []
        await asyncio.gather(*shutdown_tasks)
        for sock in ctx.udp_socks.values():
            sock.close()

    # return await ctx.run(log_pv_names=log_pv_names, startup_hook=startup_hook)


def start_nameserver_loop(pvdb, epics_interfaces, api_host='0.0.0.0'):
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        warnings.warn('uvloop not available, using default event loop')

    asyncio.run(
            start_nameserver(pvdb, epics_interfaces=epics_interfaces, api_host=api_host)
    )



