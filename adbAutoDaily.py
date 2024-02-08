import adbRoot
from tasks.blue_archive.BlueArchive import BlueArchive

if __name__ == '__main__':
    adb_root = adbRoot.ADBroot()
    adb_root.tasks.put(BlueArchive(adb_root, BlueArchive.Server.Global_zhHant))
    adb_root.tasks.put(adbRoot.end_execute)


