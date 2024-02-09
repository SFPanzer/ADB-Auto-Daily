import os
from dotenv import load_dotenv

import adb_root


class Unlock(adb_root.ADBroot.ADBTask):
    def __init__(self, adb_root_instance: adb_root.ADBroot):
        load_dotenv()
        super().__init__(adb_root_instance)

    def launch(self):
        self.adb_root_instance.execute("input keyevent KEYCODE_WAKEUP")
        dreaming_lock_screen = self.adb_root_instance.execute("dumpsys window | grep mDreamingLockscreen")
        if "mDreamingLockscreen=true" in dreaming_lock_screen:
            self.adb_root_instance.execute(f"input text {os.environ.get('UNLOCK_PASSWORD')}")
            self.adb_root_instance.execute("input keyevent 66")
