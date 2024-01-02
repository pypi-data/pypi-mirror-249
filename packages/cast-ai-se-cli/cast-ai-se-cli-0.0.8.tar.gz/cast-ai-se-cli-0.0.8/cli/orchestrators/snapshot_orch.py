from models.config import ConfigObject
from orchestrators.base_orch import BaseOrchestrator


class SnapshotOrchestrator(BaseOrchestrator):
    def __init__(self, cfg: ConfigObject):
        super().__init__(cfg)
        # self._cast_ctrl = CastController(cfg.app_config["CAST"]["CASTAI_API_TOKEN"],
        #                                  cfg.app_config["CAST"]["DEFAULT_CLUSTER_ID"],
        #                                  self._log_level)
        # self._kubectl_ctrl = KubectlController(self._log_level)
        #
        # self._initial_nodes = self._cast_ctrl.get_nodes()
        #
        # self._cloud_ctrl = None
        # self._set_cloud_controller()
        self.snapshot_subcommand_mapping = {

        }

    def execute(self) -> None:
        subcommand = self._cfg.app_inputs["snapshot_subcommand"]
        if subcommand in self.snapshot_subcommand_mapping:
            self.snapshot_subcommand_mapping[subcommand]()
        else:
            raise ValueError(f'Invalid option: {subcommand}')
