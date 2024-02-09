import json
import logging
import queue
import threading
import subprocess
from ppadb.client import Client as AdbClient

import utils


class ADBroot:
    class ADBTask(object):
        def __init__(self, adb_root_instance):
            self.adb_root_instance: ADBroot = adb_root_instance
            self.package_name = ""
            self.activity_name = ""
            self.meta_tasks = queue.Queue()

        def _start(self):
            self.adb_root_instance.execute(f"am start -n {self.package_name}/.{self.activity_name}")

        def _stop(self):
            self.adb_root_instance.execute(f"am force-stop {self.package_name}")

        def launch(self):
            self._start()
            while True:
                func = self.meta_tasks.get()
                try:
                    self.adb_root_instance.logger.info(f"Execute meta-task {func.__name__}...")
                    func()
                    self.adb_root_instance.logger.info(f"Meta-task {func.__name__} finished.")
                except StopIteration:
                    self.adb_root_instance.logger.info(f"All meta-task of {self.__class__.__name__} has been finished.")
                    break
            self._stop()

    def __init__(self):
        with open("config.json") as config_file:
            self.adb_config = json.load(config_file)["adb"]
        utils.setup_logging()
        self.logger = logging.getLogger('ADB-Auto-Daily')

        # init ADB
        self.logger.debug(subprocess.call(["adb", "start-server"]))
        self.client = AdbClient(host="127.0.0.1", port=5037)
        try:
            self.device = self.client.devices()[0]
        except IndexError:
            self.logger.critical("Unable to connect to device.")
            exit(-1)

        self.tasks = queue.Queue()
        self.task_exec_thread = threading.Thread(target=self._launch)
        self.task_exec_thread.start()

    def execute(self, cmd: str) -> str:
        self.logger.debug(f"Executing shell {cmd}...")
        result = self.device.shell(cmd)
        self.logger.debug(result)
        return result

    def screenshot(self):
        with open("screenshot.png", "bw") as file:
            file.write(subprocess.check_output(["adb", "shell", "screencap", "-p"]))
            self.logger.debug("Screenshot taken.")

    def _launch(self):
        while True:
            try:
                self.logger.debug("Getting task form queue...")
                task = self.tasks.get(block=True)
                if callable(task):
                    task_name = task.__name__
                    self.logger.info(f"Executing task \"{task_name}\"...")
                    task()
                elif isinstance(task, self.ADBTask):
                    task_name = task.__class__.__name__
                    self.logger.info(f"Executing task \"{task_name}\"...")
                    task.launch()
                else:
                    raise Exception(f"Not an executable task: {type(task)}")
                self.logger.info(f"Task {task_name} has been executed.")

            except StopIteration:
                self.logger.info("All Task finished")
                break
            except Exception as e:
                self.logger.critical(f"Unknown error occurred: {e}")


def end_execute():
    raise StopIteration
