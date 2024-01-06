import os
from pathlib import Path
from typing import List, Dict, Any


def list_all_projects(projects_folder: Path) -> List[str]:
    folders = [x.path for x in os.scandir(projects_folder) if x.is_dir()]
    return folders


def get_projects_envs(project_folder: Path, environment_folders: List[str]) -> Dict[str, Any]:
    folders = list_all_projects(project_folder)
    folder_dict = dict()
    for folder in folders:
        path = Path(folder)
        for environment_folder in environment_folders:
            envs = path / environment_folder
            if envs.exists():
                folder_dict[path.name] = {'envs': envs}
    return folder_dict
