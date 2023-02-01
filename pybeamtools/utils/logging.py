import json
import logging
import multiprocessing
import os
import threading
import logging.handlers
import queue


class LogManager:
    queue = multiprocessing.Queue(10000)


def config_root_logging(level=logging.DEBUG):
    root = logging.getLogger()
    for handler in root.handlers:
        root.removeHandler(handler)
    logging.basicConfig(level=level,
                        # format='%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s', #[%(name)s]
                        format='[%(levelname)-5.5s][%(threadName)10.10s][%(asctime)s.%(msecs)03d %(filename)10s %(lineno)3s] %(message)s',
                        datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)
    logger.info(f'Starting shared logging thread on PID {os.getpid()}')
    receive_thread = threading.Thread(target=_listener, name='log_listener', args=(LogManager.queue,))
    receive_thread.daemon = True
    receive_thread.start()
    logger.info('Logging setup finished')


def _listener(q: multiprocessing.Queue):
    local_logger = logging.getLogger(__name__)
    local_logger.info(f'Logging listener started on PID {os.getpid()}')
    while True:
        try:

            record = q.get()#timeout=10
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except queue.Empty:
            pass
            #local_logger.debug(f'Logging thread heartbeat from PID {os.getpid()}')
        except Exception as ex:
            import sys, traceback
            print('Logging thread exception:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


def setup_worker_logging(q):
    h = logging.handlers.QueueHandler(q)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Starting worker logging finished')


def pretty_json(v):
    return json.dumps(v, indent=4)