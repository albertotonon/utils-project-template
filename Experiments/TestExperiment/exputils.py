from pydantic import BaseSettings
from pathlib import Path
from projectutils.notebooks.experimentpaths import ExperimentPaths


class ExpEnvironment(ExperimentPaths):
    # from this class you can access
    # - self.experiment_dir
    #   containing the directory where this file and the notebooks are
    # - self.experiment_data_dir
    #   containing the data directory associated to this experiment folder
    def __init__(self):
        super().__init__(Path(".").absolute())
        self._init_paths()
        self.write_envrc_file()

    def _init_paths(self):
        """
        Put here all relevant paths you're accessing during your experiments.Ç
        """
        self.dataset_dir = self.experiment_data_dir / "datasets"


env = ExpEnvironment()