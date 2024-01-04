import hashlib
import json
import logging
import os
import re
from collections import OrderedDict
from contextlib import contextmanager
from typing import Dict, Tuple, List

from compipe.exception.validate_error import GErrorValue
from compipe.utils.access import GITHUB_TOKEN_KEY, AccessHub
from compipe.utils.logging import logger
from compipe.utils.parameters import (ARG_DATA, ARG_DIR, ARG_FILE, ARG_OUTPUT,
                                      ARG_PARENT)
from github import Github
from github import Auth

DEFAULT_BASE_URL = "https://api.github.com"


@contextmanager
def logger_blocker(logger_level=logging.DEBUG):
    try:
        logger = logging.getLogger()  # pylint: disable=no-member
        ori_level = logger.level
        logger.setLevel(logger_level)
        yield
    finally:
        logger.setLevel(ori_level)


class GithubHelper():

    def __init__(self, repo_name, re_filter_source=None, re_filter_export=None, output=None, base_url=None):

        token = AccessHub().get_credential(GITHUB_TOKEN_KEY)
        # using an access token
        auth = Auth.Token(token)
        self.g = Github(base_url=base_url or DEFAULT_BASE_URL, auth=auth)
        # parse repo client
        self.repo_name = repo_name

        # use with statement to avoid printing spammy log messages
        with logger_blocker(logger_level=logging.ERROR): 
            self.repo = self.g.get_repo(self.repo_name)

        # initialize filters
        self.re_filter_source = re_filter_source
        # keep exsiting file sha information
        self.re_filter_export = re_filter_export
        # it could help keep the 'sha' info for the existing file
        self.sha_mappings = {}
        # keep the export config path
        self.output = output

    def get_config(self, name):
        with logger_blocker(logger_level=logging.ERROR):
            return self.repo.get_contents(name)

    def get_properties(self, branch: str, filters=None):
        """Get the config sha lists and cache the config content. 

        Args:
            branch (str): Represent the the branch name.
            filters (_type_, optional): Represent the regex to filter the configs. 
                                        Defaults to None.

        Raises:
            GErrorValue: represent the flag of founding invalid repo name

        Returns:
            List[ContentFile]: Represent the config content file lists.
        """

        with logger_blocker(logger_level=logging.ERROR):

            file_lists = []

            if not self.repo_name or not self.repo:
                raise GErrorValue('Repo\'s not been initialized.')

            git_trees = self.repo.get_git_tree(sha=branch or self.repo.default_branch, recursive=True)

            for tree_node in git_trees.tree:

                # keep the sha cache for the whole git file/folder trees
                self.sha_mappings.update({
                    tree_node.path: tree_node.sha
                })

                # involve regex to filter the file lists
                if filters and re.fullmatch(filters, tree_node.path):
                    file_lists.append(self.repo.get_contents(path=tree_node.path))

        logger.debug(f'Loaded properties from repo: [{self.repo_name}]')

        return file_lists


class JsonPropertiesHelper(GithubHelper):

    def get_properties(self, branch="", filters=None):

        configs = super().get_properties(branch=branch, filters=filters)

        properties = {}

        with logger_blocker(logger_level=logging.ERROR):

            for config in configs:

                path, ext = os.path.splitext(config.path)

                if ext != ".json":
                    # skip the non-json files
                    continue

                json_content = json.loads(config.decoded_content)

                properties.update({
                    path: {
                        ARG_FILE: config.path,
                        ARG_OUTPUT: f'{self.output}/{os.path.basename(config.path)}',
                        ARG_PARENT: json_content.get(ARG_PARENT),
                        ARG_DATA: json_content}
                })

        return properties

    def commit(self, output: str, data: Dict, sha=None, branch='master') -> Tuple[bool, str]:

        # remove temporary (internal) keys from the config data before committing
        _data = OrderedDict(sorted(data.items()))

        # tmp attribute name has '_' prefix
        _tmp_keys = [key for key in _data.keys() if key[0] == '_']

        # remove keys
        for _key in _tmp_keys:

            del _data[_key]

        config_data = json.dumps(_data, indent=4)

        # represent the git status
        # true: add/change
        # message: logging message
        results = (True, 'None')

        with logger_blocker(logger_level=logging.WARNING):

            message_header = '[AUTO] Generate configs'
            # message = f'{message_header} - source:{self.file_path} target:{self.output}'
            # if 'sha' is valid, it would perform update behaviors
            # update_file and create_file methods are the build-in functions
            # from pygithub Repository https://github.com/PyGithub/PyGithub
            if sha:
                # compare the str hash between local data and remote file. It would skip commit if the
                # hash values are the same.
                remote_file_data = json.dumps(json.loads(self.repo.get_contents(output).decoded_content),
                                              indent=4)
                # remote config file hash
                remote_data_hash = hashlib.md5(remote_file_data.encode('utf-8')).hexdigest()

                # local config file hash
                local_data_hash = hashlib.md5(config_data.encode('utf-8')).hexdigest()

                # compare config hash and perform the commit if they were different
                if remote_data_hash != local_data_hash:

                    self.repo.update_file(output,
                                          f'{message_header} [UPDATED]',
                                          config_data,
                                          sha,
                                          branch=branch)

                    results = (True, f'Updated config: {output}')

                else:

                    results = (False, f'[Skip Commit] No change happend on file: [{output}]')

            else:
                self.repo.create_file(path=output,
                                      message=f'{message_header} [ADDED]',
                                      content=json.dumps(data, indent=4),
                                      branch=branch)

                results = (True, f'Added config: {output}')

        return results
