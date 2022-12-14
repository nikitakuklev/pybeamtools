import multiprocessing
import os
import queue
import random
import traceback
from multiprocessing import Process, Queue
import logging
import threading
from multiprocessing.process import BaseProcess

from .errors import ControlLibException, WrappedException
from .interlocks import Interlock
from ..utils.logging import setup_worker_logging, LogManager


def interlock_worker_loop(log_queue: multiprocessing.Queue,
                          queue_out: multiprocessing.Queue,
                          queue_in: multiprocessing.Queue,
                          i: Interlock):
    setup_worker_logging(q=log_queue)
    logger = logging.getLogger(__name__)

    while True:
        try:
            msg: RPCMessage = queue_out.get()
            if msg is None:
                return
            assert isinstance(msg, RPCMessage)
            logger.info(f'RPC message {msg.mode=} received on PID {os.getpid()}')
            if msg.mode == 'read':
                response = i.callback_read(**msg.data)
            elif msg.mode == 'write':
                response = i.callback_write(**msg.data)
            elif msg.mode == 'ping':
                response = 'pong'
            else:
                raise Exception(f'Unrecognized message mode {msg.mode}')
            resp = RPCResponse(counter=msg.counter,
                               uuid=i.uuid,
                               mode='response',
                               data=response)
            queue_in.put(resp)
        except Exception as ex:
            tb = traceback.format_exc()
            we = WrappedException()
            we.ex = ex
            we.tb = tb
            queue_in.put(we)


class RPCMessage:
    def __init__(self, counter: int, uuid: str, mode: str, data):
        self.counter = counter
        self.uuid = uuid
        self.mode = mode
        self.data = data


class RPCResponse:
    def __init__(self, counter: int, uuid: str, mode: str, data):
        self.counter = counter
        self.uuid = uuid
        self.mode = mode
        self.data = data


class ProcessManager:
    def __init__(self):
        self.spawn_method = 'spawn'
        self.process_map: dict[str, BaseProcess] = {}
        self.counter = 0
        self.queue_map = {}
        self.id_map = {}
        self.last_message_id: dict[str, int] = {}
        self.ctx = multiprocessing.get_context(self.spawn_method)
        self.mode = 'local'
        self.logger = logging.getLogger(self.__class__.__name__)

    def start_new_worker(self, f, *args) -> BaseProcess:
        p = self.ctx.Process(target=f, args=args)
        p.start()
        return p

    def stop_worker(self, pid: int = None):
        if pid is None:
            for k, v in self.queue_map.items():
                self.logger.debug(f'Terminating worker process_read {v[0].pid}')
                v[0].terminate()
        else:
            self.logger.debug(f'Terminating worker process_read {pid}')
            p, queue_out, queue_in, interlock = self.queue_map[pid]
            p.terminate()

    def start_interlock(self, interlock: Interlock):
        queue_out = multiprocessing.Queue(1)
        queue_in = multiprocessing.Queue(1)
        args = (LogManager.queue, queue_out, queue_in, interlock)
        p = self.start_new_worker(interlock_worker_loop, *args)
        self.logger.debug(f'Interlock worker started on PID {p.pid}')
        self.queue_map[p.pid] = (p, queue_out, queue_in, interlock)
        self.process_map[interlock.uuid] = p
        self.id_map[interlock.uuid] = p.pid
        self.counter += 1

    def stop_interlock(self, interlock: Interlock):
        pid = self.id_map[interlock.uuid]
        self.stop_worker(pid)
        #p, queue_out, queue_in, interlock = self.queue_map[pid]
        #ueue_out.put(None)

    def poll(self, interlocks_list: list[Interlock],
             data_list: list, timeout: float = 1.0) -> list[tuple[int, RPCResponse]]:
        for i in interlocks_list:
            if i.uuid not in self.id_map:
                raise KeyError(f'Interlock ID not recognized')
            if self.id_map[i.uuid] not in self.queue_map:
                raise KeyError(f'Interlock internal failure')
            if self.queue_map[self.id_map[i.uuid]][0].exitcode is not None:
                raise ControlLibException(f'Interlock process_read terminated unexpectedly with code ({self.queue_map[self.id_map[i.uuid]][0].exitcode})')

        for i, v in zip(interlocks_list, data_list):
            pid = self.id_map[i.uuid]
            p, queue_out, queue_in, interlock = self.queue_map[pid]
            msg = RPCMessage(counter=random.randint(0, 1000000), uuid=i.uuid, mode='write', data=v)
            queue_out.put(msg)
            self.last_message_id[i.uuid] = msg.counter
            self.logger.debug(f'Sent message {msg.data} (id {msg.counter}) to interlock ({i.uuid})')

        responses = []
        for i, v in zip(interlocks_list, data_list):
            pid = self.id_map[i.uuid]
            p, queue_out, queue_in, interlock = self.queue_map[pid]
            try:
                response = queue_in.get(timeout=timeout)
            except queue.Empty as ex:
                response = ex
            if isinstance(response, RPCResponse):
                responses.append((i.uuid, response))
                self.logger.debug(f'Received response (id {response.counter}) from interlock ({i.uuid})')
            elif isinstance(response, Exception):
                responses.append((i.uuid, response))
                if isinstance(response, WrappedException):
                    self.logger.debug(f'Internal failure in interlock ({i.uuid})')
                else:
                    self.logger.debug(f'Received exception from interlock ({i.uuid})')
            else:
                raise ControlLibException(f'Response ({type(response)}) not recognized')
        for (uuid, response) in responses:
            if isinstance(response, RPCResponse):
                assert response.counter == self.last_message_id[response.uuid]
                # assert response.uuid == i.uuid

        return responses

    def ping(self, pid: int, timeout=1.0):
        p, queue_out, queue_in, interlock = self.queue_map[pid]
        queue_out.put((random.randint(0, 1000000), 'ping'))
        return queue_in.get(timeout=timeout)
