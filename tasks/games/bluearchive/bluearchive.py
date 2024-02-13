from enum import Enum

import adb_root
import utils.behavior_trees
from adb_root import ADBroot


class BlueArchive(ADBroot.ADBTask):
    class Server(Enum):
        JP = 1
        CN = 2
        Global_zhHant = 3

    def __init__(self, adb_root_instance, server: Server):
        super().__init__(adb_root_instance)
        if server == self.Server.JP:
            self.adb_root_instance.logger.critical("JP server is not supported yet.")
        elif server == self.Server.CN:
            self.package_name = "com.RoamingStar.bluearchive"
        else:
            self.package_name = "com.nexon.bluearchive"
        self.activity_name = "MxUnityPlayerActivity"

        # Add behavior tree.
        self.behavior_tree = utils.behavior_trees.BehaviorTree()
        behavior_login = utils.behavior_trees.ConditionNode(self.behavior_tree.blackboard, )
        self.behavior_tree.root.children.append(behavior_login)

        self.meta_tasks.put(adb_root.end_execute)

    def login(self):
        pass
