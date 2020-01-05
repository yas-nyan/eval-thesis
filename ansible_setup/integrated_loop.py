import subprocess
from subprocess import PIPE
import generate_pods_vars as gen
import time
from logzero import logger


def __proc_base(CMD):
    proc = subprocess.run(CMD)
    return proc.returncode == 0


def initialize_pods():
    CMD = ["ansible-playbook", "-i", "hosts", "pods.yml"]
    return __proc_base(CMD)


def initialize_rr():
    CMD = ["ansible-playbook", "-i", "hosts", "rr.yml"]
    return __proc_base(CMD)


def initialize_extra_server():
    CMD = ["ansible-playbook", "-i", "hosts", "add_extra_server.yml"]
    return __proc_base(CMD)


def experiment_add():
    CMD = ["ansible-playbook", "-i", "hosts", "experiment_add_server.yml"]
    return __proc_base(CMD)


def experiment_remove():
    CMD = ["ansible-playbook", "-i", "hosts", "experiment_remove_server.yml"]
    return __proc_base(CMD)


if __name__ == "__main__":
    REPEAT = 10
    SLEEP_TIME_RATIO = 2
    COUNTS = [10, 100, 200, 300, 400]

    for count in COUNTS:
        logger.info(f"Start. Servers: {count}")
        # configの作成
        gen.generate_config(count)

        # 諸々の初期化
        logger.info("Initializing...")
        if initialize_rr():
            logger.info("sucess: initializing RR")
        else:
            logger.error("failed: initializing RR")

        if initialize_pods():
            logger.info("sucess: initializing pods")
        else:
            logger.error("failed: initializing pods")

        # sleep
        logger.info("sleep for converfence")
        time.sleep(SLEEP_TIME_RATIO*count)

        # loop
        logger.info("start add loop")
        for i in range(REPEAT):
            if experiment_add():
                logger.info(f"sucess: add experiment count:{i+1}/{REPEAT}")
            else:
                logger.error(f"failed: add experiment count:{i+1}/{REPEAT}")
        logger.info("end add loop")

        logger.info("start remove loop")
        logger.info("start add loop")
        if initialize_extra_server():
            logger.info("sucess: initializing extra server")
        else:
            logger.error("failed: initializing extra server")

        for i in range(REPEAT):
            if experiment_remove():
                logger.info(f"sucess: remove experiment count:{i+1}/{REPEAT}")
            else:
                logger.info(f"failed: remove experiment count:{i+1}/{REPEAT}")
