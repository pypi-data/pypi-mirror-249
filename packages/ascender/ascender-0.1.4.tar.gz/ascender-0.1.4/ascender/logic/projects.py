from pathlib import Path
from ascender.settings import FRAMEWORK_STABLE_LATEST_VERSION, FRAMEWORK_TYPES, IS_UNIX
from typing import Literal, Optional
from rich.console import Console
from rich.progress_bar import ProgressBar
from git import RemoteProgress, Repo
from virtualenv.run import cli_run
from toml import load

import os
import subprocess
import requests


class CloneProgress(RemoteProgress):
    progress_bar: ProgressBar

    def update(self, op_code: int, cur_count: str | float, max_count: Optional[str | float] = None, message: str = ''):
        if max_count:
            progress = (cur_count / max_count) * 100
            
            self.progress_bar.update(progress)
            print(f"Progress: {progress:.2f}%", end='\r')
    

class UpdaterMasterLogic:
    def __init__(self, base_path: str, framework_type: Literal["standard"] = "standard") -> None:
        self.base_path = base_path
        self.framework_type = framework_type
        self.toml_path = f"{base_path}/pyproject.toml"
    
    def is_project(self):
        """
        Check if the current directory is an AscenderFramework project or not.
        """
        directory = os.getcwd()

        if os.path.exists(f"{directory}/.asc_venv") and os.path.exists(f"{directory}/start.py") and os.path.exists(f"{directory}/core"):
            return True

    def get_version(self) -> str:
        toml_data = load(self.toml_path)
        return toml_data["tool"]["poetry"]["version"]
    
    def get_latest_version(self) -> str:
        repo_name = "AscenderTeam/AscenderFramework"
        url = f"https://api.github.com/repos/{repo_name}/releases/latest"

        response = requests.get(url)
        latest_release = response.json()

        return latest_release.get("name", FRAMEWORK_STABLE_LATEST_VERSION)

    def compare_versions(self, v1: str, v2: str):
        # Removing the 'v' prefix and splitting the versions into components
        components1 = v1.lstrip('v').split('.')
        components2 = v2.lstrip('v').split('.')

        # Compare each component
        for c1, c2 in zip(components1, components2):
            # Convert components to integers for comparison
            if int(c1) < int(c2):
                return -1
            elif int(c1) > int(c2):
                return 1

        # If all components are equal, the versions are the same
        return 0

    def update(self, safe_mode: bool = True) -> bool:
        if not self.is_project():
            raise Exception("Cannot recognize project directory") # TODO: Add custom exception
        
        current_version = self.get_version()
        latest_version = self.get_latest_version()
        
        if self.compare_versions(current_version, latest_version) >= 0:
            return False
        
        temp_inst = InstallationMasterLogic(Console(), f"{self.base_path}/.asc_temp", self.framework_type)
        temp_inst.run_installation(safe_mode)

        # Copy core directory from self.base_path/.asc_temp to self.base_path (overwrite)
        subprocess.run(f"cp -r {self.base_path}/.asc_temp/core {self.base_path}", shell=True)
        subprocess.run(f"cp -r {self.base_path}/.asc_temp/pyproject.toml {self.base_path}", shell=True)
        # Delete .asc_temp directory
        subprocess.run(f"rm -rf {self.base_path}/.asc_temp", shell=True)


class InstallationMasterLogic:
    def __init__(self, 
                console: Console,
                installation_dir: Optional[str] = None,
                framework_type: Literal["standard"] = "standard") -> None:
        self.installation_dir = os.getcwd() if not installation_dir else installation_dir
        self.framework_type = framework_type
        self.console = console
    
    def run_installation(self, safe_mode: bool = True) -> bool:
        _project = Path(self.installation_dir)
        
        # Does project exist or not
        if _project.exists():
            self.console.print(f"[bold red]Fatal error: Cannot create project[/bold red]")
            self.console.log(f"Project with name {self.installation_dir} already exists!")
            return False
        
        self.console.print(f"[yellow]Installing Ascender Framework to [/yellow] [cyan]{self.installation_dir}[cyan]")
        
        # Set progress
        CloneProgress.progress_bar = ProgressBar()
        project = Repo.clone_from(FRAMEWORK_TYPES[self.framework_type], self.installation_dir, progress=CloneProgress(), allow_unsafe_options=(not safe_mode))
        project.delete_remote("origin")
        return True
    
    def create_environment(self, name: str = ".asc_venv"):
        # Create virtual environment
        self.console.print(f"[yellow]Starting to create virtual environment at[/yellow] [cyan]{self.installation_dir}/{name}[cyan]")
        cli_run([f"{self.installation_dir}/{name}"])
    
    def install_requirements(self, name: str = ".asc_venv"):
        # Install requirements
        if IS_UNIX:
            subprocess.run(f"source {self.installation_dir}/{name}/bin/activate && pip3 install -r {self.installation_dir}/requirements.txt", shell=True)
            return
        subprocess.run(f". {self.installation_dir}/{name}/bin/activate && pip install -r {self.installation_dir}/requirements.txt", shell=True)
    
    def run_update(self, safe_mode: bool = True) -> bool:
        # Set progress
        update_master = UpdaterMasterLogic(self.installation_dir, self.framework_type)
        update_master.update(safe_mode)