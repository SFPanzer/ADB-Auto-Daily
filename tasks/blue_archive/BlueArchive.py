from enum import Enum

import adbRoot
from adbRoot import ADBroot


class BlueArchive(ADBroot.ADBTask):
    class Server(Enum):
        JP = 1
        CN = 2
        Global_zhHant = 3

    def __init__(self, adb_root, server: Server):
        super().__init__(adb_root)
        if server == self.Server.JP:
            self.adb_root.logger.critical("JP server is not supported yet.")
        elif server == self.Server.CN:
            self.package_name = "com.RoamingStar.bluearchive"
        else:
            self.package_name = "com.nexon.bluearchive"
        self.activity_name = "MxUnityPlayerActivity"

        self.meta_tasks.put(adbRoot.end_execute)

