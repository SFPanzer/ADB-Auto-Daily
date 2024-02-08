import json
import logging
import queue
import threading
import time
import subprocess
from abc import abstractmethod

import utils


class ADBroot:
    class ADBTask(object):
        def __init__(self, adb_root):
            self.adb_root: ADBroot = adb_root
            self.package_name = ""
            self.activity_name = ""
            self.meta_tasks = queue.Queue()

        def _start(self):
            self.adb_root.execute(["shell", "am", "start", "-n", f"{self.package_name}/.{self.activity_name}"])

        def _stop(self):
            self.adb_root.execute(["shell", "am", "force-stop", f"{self.package_name}"])

        def launch(self):
            self._start()
            while True:
                func = self.meta_tasks.get()
                try:
                    self.adb_root.logger.info(f"Execute meta-task {func.__name__}...")
                    func()
                    self.adb_root.logger.info(f"Meta-task {func.__name__} finished.")
                except StopIteration:
                    self.adb_root.logger.info(f"All meta-task of {self.__class__.__name__} has been finished.")
                    break
            self._stop()

    def __init__(self):
        with open("config.json") as config_file:
            self.adb_config = json.load(config_file)["adb"]
        utils.setup_logging()
        self.logger = logging.getLogger('ADB-Auto-Daily')

        # init abd
        version = self.execute(["version"])
        if len(version) < 30:
            self.logger.critical("Can not launch adb")
            exit(-1)
        for i in range(3):
            try:
                self.devices = self.execute(["devices"]).split("\n")[1]
            except IndexError:
                self.logger.warning(f"Device not found. ({i + 1}/3)")
                time.sleep(5)
                continue
            break
        else:
            self.logger.critical("Unable to connect to device.")
            exit(-1)

        # Power up and Unlock phone.
        self.execute(["shell", "input", "keyevent", "KEYCODE_WAKEUP"])
        dreaming_lock_screen = self.execute(["shell", "dumpsys", "window", "|", "grep", "mDreamingLockscreen"])
        if "mDreamingLockscreen=true" in dreaming_lock_screen:
            self.execute(["shell", "input", "text", self.adb_config["unlock_password"]])
            self.execute(["shell", "input", "keyevent", "66"])

        # Go to home page.

        self.tasks = queue.Queue()
        self.task_exec_thread = threading.Thread(target=self._launch)
        self.task_exec_thread.start()

    def execute(self, args: list) -> str:
        output = subprocess.check_output([self.adb_config["adb_path"]] + args)
        output = output.decode(self.adb_config["terminal_encoding"])
        self.logger.debug(f"exec: {args}\n{output}".strip())
        return output

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
