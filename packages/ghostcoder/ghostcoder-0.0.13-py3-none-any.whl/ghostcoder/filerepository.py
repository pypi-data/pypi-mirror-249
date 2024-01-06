import difflib
import logging
import os
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

import tiktoken
from git import Repo, Tree, IndexObject, Blob

from ghostcoder.schema import Folder, File, SaveFilesRequest, DiscardFilesRequest, FileItem
from ghostcoder.utils import language_by_filename, get_extension, get_purpose_by_filepath

logger = logging.getLogger(__name__)

class ContextScope(Enum):
    LISTED = "listed"
    READ = "read"
    UPDATED = "updated"


class FileRepository:

    def __init__(self,
                 repo_path: Path,
                 use_git: bool = True,
                 read_untracked: bool = False,
                 repo: Optional[Repo] = None,
                 exclude_dirs: Optional[List[str]] = None,
                 include_dirs: Optional[List[str]] = None,
                 ignore_hidden: bool = True):
        super().__init__()
        self.repo_path = repo_path

        if use_git:
            self.repo = repo if repo else Repo(path=repo_path)
            if not self.repo.heads:
                raise Exception("Git repository has no heads, you need to do an initial commit.")
            self._current_branch = self.repo.active_branch.name

            logger.debug(f"Initiate repo {self.repo_path} on branch {self._current_branch}")
        else:
            self.repo = None
            logger.debug(f"Initiate repo {self.repo_path} without Git")

        self.enc = tiktoken.get_encoding("cl100k_base")

        self.file_context = {}

        self.read_untracked = read_untracked
        self.ignore_hidden = ignore_hidden
        self.exclude_file_extensions = [".pem", ".csv"]
        self.exclude_dirs = [".gcoder", ".index"]
        if exclude_dirs:
            self.exclude_dirs.extend(exclude_dirs)

        self.include_dirs = include_dirs

    @property
    def identifier(self):
        return str(self.repo_path)

    def file_tree(self, directory: str = None, file_suffix: str = None) -> Folder:
        return self._generate_file_tree(directory=directory, file_suffix=file_suffix)

    def _generate_file_tree(self, directory: str = None, file_suffix: str = None) -> Folder:
        dir_parts = directory.split("/") if directory else []
        children = self.__generate_file_tree(tree=self.repo.tree(), dir_parts=dir_parts, file_suffix=file_suffix)

        name = self.repo_path.name
        root_dir = Folder(
            name=name,
            path="")
        root_dir.children = children  # FIXME: Get the wrong typing if set in constructor

        if self.read_untracked:
            untracked_files = [item.a_path for item in self.repo.index.diff(None)]
            for path in self.repo.untracked_files + untracked_files:
                if directory is None or path.startswith(directory):
                    self.add_file_to_tree(root_dir, path, False)

            staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
            for path in staged_files:
                if directory is None or path.startswith(directory):
                    self.add_file_to_tree(root_dir, path, True)

        return root_dir

    def __generate_file_tree(self, tree: Tree, dir_parts: List[str] = None, file_suffix: str = None) -> list[Union[File, Folder]]:
        if tree is None:
            return []

        nodes = []
        for item in tree:

            if item.name.startswith(".") and self.ignore_hidden:
                continue
            if item.type == "blob":
                if self.include_dirs and not any(item.path.startswith(dir) for dir in self.include_dirs):
                    continue

                if dir_parts:
                    continue
                full_path = os.path.join(self.repo_path, item.path)
                if file_suffix and not item.path.endswith(file_suffix):
                    continue
                if any(item.path.endswith(ext) for ext in self.exclude_file_extensions):
                    continue
                if not os.path.exists(full_path):
                    continue
                if self._is_binary(full_path):
                    continue
                nodes.append(self._build_file_from_object(obj=item))
            elif item.type == "tree":
                if item.name in self.exclude_dirs:
                    continue

                if dir_parts and item.name != dir_parts[0]:
                    continue

                folder = Folder(
                    name=item.name,
                    path=item.path)
                folder.children = self.__generate_file_tree(tree=item, dir_parts=dir_parts[1:])  # FIXME: Get the wrong typing if set in constructor
                nodes.append(folder)
        nodes.sort(key=lambda x: x.name)
        return nodes

    def _build_file_from_object(self, obj: Blob) -> File:
        language = language_by_filename(obj.path)
        purpose = get_purpose_by_filepath(language, obj.path)
        return File(
            name=obj.name,
            path=obj.path,
            hash=obj.hexsha,
            staged=True,
            language=language,
            purpose=purpose
        )

    def _build_file(self, file_path: str, staged: bool = False) -> File:
        language = language_by_filename(file_path)
        if language:
            purpose = get_purpose_by_filepath(language, file_path)
            return File(
                path=file_path,
                staged=staged,
                language=language,
                purpose=purpose
            )
        return File(path=file_path, staged=staged)

    def add_file_to_tree(self, root: Folder, path: str, staged: bool):
        full_path = os.path.join(self.repo_path, path)
        if not os.path.exists(full_path):
            return
        if self._is_binary(full_path):
            return

        p = Path(path)
        path_parts = p.parts
        current_folder = root

        for part in path_parts[:-1]:
            if part in self.exclude_dirs:
                return
            if part.startswith(".") and self.ignore_hidden:
                return

            new_folder_path = str(Path(current_folder.path) / part)
            folder = current_folder.find(new_folder_path)
            if folder is None:
                folder = Folder(name=part, path=new_folder_path, children=[])
                current_folder.children.append(folder)

            current_folder = folder

        file_path = str(p)

        file = current_folder.find(file_path)

        if file is None:
            file = self._build_file(file_path, staged)
            current_folder.children.append(file)
        else:
            file.staged = staged

    def _new_files(self, dir_path: str, files: list[str]) -> list[File]:
        return [
            self._build_file(file_path=os.path.join(dir_path, file), staged=False)
            for file in files]

    def _is_binary(self, file_path: str):
        with open(file_path, 'rb') as file:
            chunk = file.read(8192)
            return b'\0' in chunk

    def listed_in_context(self, file_path: str):
        self.file_context[file_path] = ContextScope.LISTED

    def read_in_context(self, file_path: str):
        self.file_context[file_path] = ContextScope.READ

    def get_files_by_suffix(self, file_suffixes: List[str]) -> list[str]:
        return [file.path
                for file in self.file_tree().traverse()
                if any(file.path.endswith(suffix) for suffix in file_suffixes)]

    def get_source_files(self, language: str = None, directory: str = None, include_test_files: bool = False):
        language_test_suffix = {  # TODO: Move to utils
            "python": "_test.py",
            "java": "Test.java"
        }

        full_dir_path = self.repo_path / directory if directory else self.repo_path

        if language:
            file_pattern = f"*{get_extension(language)}"
        else:
            file_pattern = "*.*"

        all_files = list(full_dir_path.rglob(file_pattern))
        file_paths = [
            file
            for file in all_files if file.is_file() and not any(part.startswith('.') for part in file.parts) and
                                     (include_test_files or "test" not in file.name.lower())
        ]

        file_items = []
        for file in file_paths:
            try:
                file_items.append(
                    FileItem(file_path="/" + str(file.relative_to(self.repo_path)), content=file.read_text()))
            except Exception as e:
                logging.warning(f"Failed to read file {file}. Error: {e}")

        return file_items

    def get_file_content(self, file_path: str) -> Optional[str]:
        if file_path.startswith("/"):
            file_path = file_path[1:]

        if not os.path.exists(os.path.join(self.repo_path, file_path)):
            return None

        with open(os.path.join(self.repo_path, file_path), 'r') as f:
            return f.read()

    def get_file(self, file_path: str) -> Optional[FileItem]:
        if file_path.startswith("/"):
            file_path = file_path[1:]

        if not os.path.exists(os.path.join(self.repo_path, file_path)):
            return None

        with open(os.path.join(self.repo_path, file_path), 'r') as f:
            return FileItem(file_path=file_path, content=f.read())

    def find_files_in_content(self, content=str, folder: Folder=None):
        folder = folder or self.file_tree()

        found_files = []
        for node in folder.children:
            if isinstance(node, File) and node.path in content:
                found_files.append(node)
            elif isinstance(node, Folder) and node.path in content:
                found_files.extend(self.find_files_in_content(content, node))

        return found_files

    def file_tokens(self, file_path: str) -> int:
        file = self.get_file_content(file_path)
        if file is not None:
            tokens = self.enc.encode(file)
            return len(tokens)

    @property
    def active_branch(self):
        return self._current_branch

    def create_branch(self, branch_name: str):
        if branch_name in self.repo.heads:
            raise Exception(f"Branch {branch_name} already exists.")

        self.repo.create_head(branch_name)
        logger.info(f"Created branch: {branch_name}")

    def checkout(self, branch_name: str):
        if branch_name not in self.repo.heads:
            new_branch = self.repo.create_head(branch_name)
        else:
            new_branch = self.repo.heads[branch_name]

        new_branch.checkout()
        self._current_branch = branch_name
        logger.info(f"Active branch: {branch_name}")

    def update_file(self, file_path: str, content: str):
        if file_path.startswith("/"):
            file_path = file_path[1:]

        """Write file content to disk and stage the file for commit. """
        full_path = self.repo_path / file_path

        is_new = not full_path.exists()
        untracked = is_new or self.repo is None or file_path in self.repo.untracked_files

        if is_new:
            parent_path = os.path.split(full_path)[0]
            os.makedirs(parent_path, exist_ok=True)
            old_content = []
        else:
            with open(full_path, 'r') as f:
                old_content = f.readlines()

        with open(full_path, 'w') as f:
            f.write(content)

        if untracked:
            file_name = full_path.name
            new_content = content.splitlines(True)
            diff = ''.join(
                difflib.unified_diff(old_content, new_content, fromfile=file_name, tofile=file_name, lineterm='\n'))
        elif self.repo is not None:
            diff = self.repo.git.diff(file_path)
        return diff

    def get_diff(self):
        return self.repo.git.diff('--staged')

    def stage_files(self, file_paths: List[str]):
        """Stage the files for commit."""

        for file_path in file_paths:
            self.stage_file(file_path)

    def stage_file(self, file_path: str):
        logging.info(f"Staging file {file_path} to commit.")

        if file_path.startswith("/"):
            file_path = file_path[1:]

        self.repo.git.add(file_path)
        self.repo.index.write()

    def stage_all_files(self):
        logging.info(f"Stage all files to commit.")
        self.repo.git.add("-A")
        self.repo.index.write()

    def discard_files(self, file_paths: List[str]):
        """Discards the changes by resetting the file to HEAD."""

        for file_path in file_paths:
            self.discard_file(file_path)

    def discard_file(self, file_path: str):
        """Discards the changes by resetting the file to HEAD."""

        if file_path.startswith("/"):
            file_path = file_path[1:]

        if file_path in self.repo.untracked_files:
            logging.info(f"Discard file {file_path} by running clean -df")
            self.repo.git.clean('-df', file_path)
        else:
            logging.info(f"Discard file {file_path} by running reset HEAD")
            self.repo.git.reset("HEAD", file_path)
            self.repo.git.checkout("HEAD", file_path)

    def discard_all_files(self):
        """Discards all changes by resetting the file to HEAD."""

        logging.info(f"Discard all files by running clean -df and reset HEAD")
        self.repo.git.clean('-df')
        self.repo.git.reset("HEAD")
        self.repo.git.checkout("HEAD")

    def commit(self, message: str):
        self.repo.git.commit('-m', message)
