import os
from dlrover.python.common import env_utils
from dlrover.python.elastic_agent.torch.ckpt_saver import AsyncCheckpointSaver
from multiprocessing import Process
import time
from dlrover.python.common.log import default_logger as logger


def start_async_save():
    AsyncCheckpointSaver.start_async_saving_ckpt()
    while True:
        time.sleep(36000)


def start_async_process():
    local_rank = env_utils.get_local_rank()
    role_name = os.getenv("ROLE_NAME", "")
    # Only start the process to asynchronously save checkpoint on local rank 0
    # if the training process is not launched by dlrover-run.
    if role_name != "dlrover-trainer" and local_rank == 0:
        p = Process(target=start_async_save, daemon=True)
        p.start()
        logger.info("Start a process to asynchronously save checkpoint.")
