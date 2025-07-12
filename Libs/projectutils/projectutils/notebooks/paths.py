from pathlib import Path


class Paths:
    """
    Class containing useful paths read from env vars. Use DirEnv to easily use them.
    """

    def __init__(self):
        self.project_dir = Path(__file__).parent.parent.parent.parent.parent
        self.data_root = self.project_dir / 'Data'
        self.experiments_root = self.project_dir / 'Experiments'
        self.scratches_root = self.project_dir / 'Scratches'
        self.experiments_data_root = self.data_root / 'Experiments'
        self._write_envrc_file(self.project_dir)

    def _write_envrc_file(self, output_dir: Path):
        """
        Creates the .envrc file at the root of the project repo. The file is then read by dirEnv to generate env vars.
        """
        envrc_content = 'export PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"\n'
        envrc_content = self._add_class_paths_to_envrc_content(envrc_content)
        envrc_content = self._add_credential_variables(envrc_content)
        envrc_file = output_dir / ".envrc"
        envrc_file.write_text(envrc_content, encoding="utf-8")
        print(f'Environment written in "{envrc_file.absolute()}"')

    def _add_class_paths_to_envrc_content(self, current_envrc_content: str) -> str:
        for var_name_lowercase, path in self.__dict__.items():
            if var_name_lowercase == 'project_dir':
                # project dir is already set in the first line.
                continue
            path_from_project_dir = path.relative_to(self.project_dir)
            envrc_path = f'${{PROJECT_DIR}}/{path_from_project_dir}'
            current_envrc_content += f'export {var_name_lowercase.upper()}="{envrc_path}"\n'
        return current_envrc_content

    def _add_credential_variables(self, current_envrc_content: str) -> str:
        # additional credential variables are stored in the git-ignored file project_dir/credentials.sh
        if (self.project_dir / 'credentials.sh').is_file():
            current_envrc_content += ('\n# load credentials stored in the git-ignored file "credentials.sh"\n"'
                                      'source credentials.sh\n')
        return current_envrc_content

    def get_create_data_dir(self, experiment_path: Path) -> Path:
        """
        Returns the data directory for the specified experiment path.
        For example, suppose you're working on an experiment in EXPERIMENTS_ROOT/coverage/exp0, the corresponding data
        directory would be DATA_ROOT/coverage/exp0.
        :param experiment_path:
        :return:
        """
        exp_data = self.data_root / experiment_path.relative_to(self.experiments_root)
        exp_data.mkdir(parents=True, exist_ok=True)
        return exp_data


paths = Paths()
