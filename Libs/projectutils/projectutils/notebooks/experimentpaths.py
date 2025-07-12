from pathlib import Path

from projectutils.notebooks import paths


class ExperimentPaths:

    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir.absolute()
        self.experiment_data_dir = paths.get_create_data_dir(experiment_dir)

    def write_envrc_file(self):
        """
        Creates the .envrc file at the root of the project repo. The file is then read by dirEnv to generate env vars.
        """
        envrc_content = 'source_up\n'
        envrc_content = self._add_class_paths_to_envrc_content(envrc_content)
        envrc_file = self.experiment_dir / ".envrc"
        envrc_file.write_text(envrc_content, encoding="utf-8")
        print(f'Environment written in "{envrc_file.absolute()}"')

    def _add_class_paths_to_envrc_content(self, current_envrc_content: str) -> str:
        for var_name_lowercase, path in self.__dict__.items():
            assert isinstance(path, Path)
            path_from_project_dir = path.absolute().relative_to(paths.project_dir)
            envrc_path = f'${{PROJECT_DIR}}/{path_from_project_dir}'
            current_envrc_content += f'export {var_name_lowercase.upper()}="{envrc_path}"\n'
        return current_envrc_content
