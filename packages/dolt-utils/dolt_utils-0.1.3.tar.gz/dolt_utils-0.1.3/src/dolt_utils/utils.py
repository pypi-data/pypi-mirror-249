import re
from typing import Optional, Self
from doltcli import Dolt
import os
import tempfile
import atexit
from logging import basicConfig, getLogger
import random
import pandas as pd

basicConfig(level="INFO")
logger = getLogger(__name__)


class DoltRepo:
    def __init__(
        self: Self,
        repo_name: str,
        branch: Optional[str] = None,
        existing_location: Optional[str] = None,
        sha: Optional[str] = None,
        pull: bool = False,
    ) -> None:
        self.repo_name = repo_name
        if branch and sha:
            raise ValueError("Cannot specify both branch and sha")
        if pull and sha:
            raise ValueError("Cannot specify both pull and sha")
        if branch is None:
            branch = "main"
        self.branch = branch
        if existing_location:
            self.dolt = Dolt(existing_location)
        else:
            self.tmp_folder = tempfile.TemporaryDirectory()
            self.dolt = Dolt.clone(repo_name, self.tmp_folder.name, branch=branch)
            atexit.register(self.cleanup)

        if sha:
            random_branch_name = f"branch-{random.randint(0, 1000000)}"
            self.dolt.checkout(branch=random_branch_name, checkout_branch=True, start_point=sha)

        if pull:
            self.dolt.checkout(branch=branch)
            self.dolt.pull()

    def cleanup(self: Self) -> None:
        self.tmp_folder.cleanup()

    def ls(self: Self):
        return self.dolt.ls()
        # pass

    def get_bool_cols(self: Self, table_name: str) -> list:
        tmp_loc = tempfile.TemporaryDirectory()
        file_path = os.path.join(tmp_loc.name, "temp_schema.sql")
        self.dolt.schema_export(table_name, filename=file_path)
        with open(file_path, "r") as f:
            matches = re.findall(r"`(\w+)` tinyint\(1\)", f.read())
        os.remove(file_path)
        return matches

    def convert_cols(self: Self, table_name: str, file_path: str) -> None:
        # Load in the csv
        df = pd.read_csv(file_path)
        # Get the boolean columns
        bool_cols = self.get_bool_cols(table_name)
        # Convert the columns
        for col in bool_cols:
            df[col] = df[col].astype(bool)
        # Save the csv
        df.to_csv(file_path, index=False)

    def get_csv(self: Self, table_name: str, save_path: str) -> None:
        # If save_path is relative, make it absolute
        if not os.path.isabs(save_path):
            save_path = os.path.join(os.getcwd(), save_path)
        save_path = self.__clean_file_name(save_path)
        save_path = save_path + ".csv"
        logger.info(f"Saving {table_name} to {save_path}")
        self.dolt.table_export(table_name, save_path, force=True, file_type="csv")
        self.convert_cols(table_name, save_path)

    def __clean_file_name(self: Self, file_name: str) -> str:
        if file_name.endswith(".csv"):
            file_name = file_name[:-4]
        if file_name.endswith(".dolt"):
            file_name = file_name[:-5]
        return file_name

    def discover_dlt_files(self: Self, path: str) -> list:
        # If path is relative, make it absolute
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        # Get all files in path and subdirectories
        files = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
        # Filter out non-dolt files
        dolt_files = [file for file in files if file.endswith(".dolt")]
        return dolt_files

    def get_dolt_files(self: Self, path: str, add_to_gitignore: bool = False) -> None:
        dolt_files = self.discover_dlt_files(path)
        for file in dolt_files:
            file_name = os.path.basename(file)
            table_name = self.__clean_file_name(file_name)
            csv_name = table_name + ".csv"
            base_path = os.path.dirname(file)
            self.get_csv(table_name, file)
            if add_to_gitignore:
                with open(os.path.join(base_path, ".gitignore"), "r+") as f:
                    # Check if csv already in gitignore
                    if csv_name not in f.read():
                        f.write(csv_name + "\n")
