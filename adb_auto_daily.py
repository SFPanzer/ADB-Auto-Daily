import time

import adb_root
import utils.basic_task
from tasks.games.bluearchive.bluearchive import BlueArchive

if __name__ == '__main__':
    adb_root_instance = adb_root.ADBroot()
    adb_root_instance.tasks.put(utils.basic_task.Unlock(adb_root_instance))
    time.sleep(5)
    adb_root_instance.tasks.put(BlueArchive(adb_root_instance, BlueArchive.Server.Global_zhHant))
    adb_root_instance.tasks.put(adb_root.end_execute)
