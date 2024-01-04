"""Populate the property objects
"""
import copy
import json
from abc import ABCMeta, abstractmethod

from compipe.exception.validate_error import GErrorNullObject, GErrorValue, GErrorKeyNotFound
from compipe.response.command_result import MSGStatusCodes
from compipe.utils.logging import logger
from compipe.utils.parameters import (ARG_DATA, ARG_FILE, ARG_GUID,
                                      ARG_NAME, ARG_OBJ, ARG_PARENT)
from compipe.utils.task_queue_helper import TQHelper
from pydantic.error_wrappers import ValidationError

from ..github_app.github_helper import JsonPropertiesHelper
from ..hash_code_helper import hexdigest_str
from .resolver_parameter import ResolverParam

IDENTITY_KEYS = {'id', 'name'}


class AbstractAssetResolver(metaclass=ABCMeta):

    @abstractmethod
    def populate(self):
        """Populate asset to full version config.
        """
        pass

    @abstractmethod
    def validate(self):
        """Validate content when populating
        """
        pass


class AssetResolver(AbstractAssetResolver):
    def __init__(self, param: ResolverParam):
        self._repo_helper = None
        self.ignore_paths = param.ignore_paths
        self.main_branch = param.main_branch
        self.param = param

        # validate schema-json
        # e.g. validate(instance=value, schema=self.schema)
        self.model = param.model
        self.schema = param.model.schema_json(indent=4)
        self.configs = {}
        self.dependency = {}

        # it's aimed to cache the resolved config when building dependencies
        self._cached_configs = {}

    @property
    def repo_helper(self):
        if not self._repo_helper:
            self._repo_helper = JsonPropertiesHelper(self.param.repo,
                                                     self.param.filter_source,
                                                     self.param.filter_export,
                                                     self.param.output_path,
                                                     self.param.base_url)
        return self._repo_helper

    def get(self, path):
        return self.configs.get(path)

    def load_configs(self):
        self.configs = self.repo_helper.get_properties(branch=self.main_branch,
                                                       filters=self.param.filter_source)

        for cfg in [cfg for _, cfg in self.configs.items() if not cfg.get(ARG_PARENT)]:
            obj = self.model.parse_obj(cfg.get(ARG_DATA))
            cfg[ARG_DATA] = json.loads(obj.json())

    def populate(self):

        self.load_configs()

        # start to build inheritance dependencies
        for path, value in self.configs.items():
            branches = self.build_dependencies(path, value, [])
            route = '.'.join(branches)
            if route not in self.dependency:
                self.dependency.update({
                    route: branches
                })

        # start to build all configs
        # the building routes would be:
        # root -> parent -> child
        #                -> child
        #                -> child -> sub-child
        #                         -> sub-child
        for routes in self.dependency.values():
            for path in routes:

                if path in self._cached_configs:
                    continue

                config = self.configs.get(path)
                if config.get(ARG_PARENT):
                    parent_config = self.configs.get(config[ARG_PARENT])
                    populated_config_data = copy.deepcopy(parent_config.get(ARG_DATA))

                    # start to override the sub-config properties
                    self.override_data(config[ARG_DATA], populated_config_data)
                    populated_config_data[ARG_GUID] = self._gen_guid(path)

                else:
                    populated_config_data = copy.deepcopy(config.get(ARG_DATA))

                asset = self.validate(path, populated_config_data)
                self.configs[path][ARG_DATA] = dict(populated_config_data)
                self.configs[path][ARG_OBJ] = asset

                # mark the built config as cached
                self._cached_configs[path] = True

    def _gen_guid(self, data):
        return next(iter(hexdigest_str(data)), None)

    @classmethod
    def override_data(cls, source: dict, target: dict):
        """Perform the resolver on dict object. The child object inherits values
        from parent

        Arguments:
            source {dict} -- [description]
            target {dict} -- [description]
        """
        for key, value in source.items():
            # process the dictionary type object
            if isinstance(value, dict):
                if key in target:

                    if not target[key]:
                        target[key] = value
                    else:
                        cls.override_data(value, target[key])
                        continue
            # process the array type object
            elif isinstance(value, list) and key in target:
                if not str(key).startswith('uid_'):
                    value = cls.resolve_list_items(value, target[key])

            target.update({
                key: value
            })

    @classmethod
    def resolve_list_items(cls, source, target):
        """Perform the resolver on 'list' property. 

        Comparing rules:
            Dict type: The dict item would be using "name" key as an 
            identifer to compare the values between child and par

        Arguments:
            source {list} -- Represent the source list.
            target {list} -- Represent the target list.

        Returns:
            list -- Represent the resolved new lists.
        """
        new_list = []
        # check element type
        list_item = next(iter(source + target), None)
        if isinstance(list_item, dict):
            # copy the items from source that don't exist in target
            for item in source:
                if not any(item[ARG_NAME] == t_item[ARG_NAME] for t_item in target):
                    new_list.append(item)
            # resolve the target items
            for item in target:
                # parse the valid identity key to compare the list elements
                if (identity_key := next(iter(IDENTITY_KEYS.intersection(item.keys())), None)) is None:
                    raise GErrorKeyNotFound(f'Not found one of the valid identity keys from {IDENTITY_KEYS}')

                source_item = next(iter([src for src in source if src[identity_key] == item[identity_key]]), None)
                if source_item:
                    # copy the source list item to the target
                    cls.override_data(source=source_item, target=item)

                # add the resolved target item to the new lists
                new_list.append(item)

        else:
            new_list = list(set(source + target))

        # # sort 'str' lists
        # if len(new_list) > 0 and isinstance(new_list[0], str):
        #     new_list.sort()

        return new_list

    def build_dependencies(self, path, config, branches=[]):
        """Build asset hierarchy dependencies. It would describe the relationship
        between children and parent object.

        Arguments:
            path {str} -- Represent the object path.
            config {dict} -- Represent the object value.

        Keyword Arguments:
            branches {list} -- Represent the route paths (default: {[]})

        Returns:
            list -- Represent the route dependencies.
        """
        logger.debug(f'Build dependencies on: [{path}]')
        parent = config.get(ARG_PARENT)
        branches.insert(0, path)
        if parent:
            parent_config = self.configs.get(parent)
            if not parent_config:
                raise GErrorNullObject(
                    f'Found invalid parent:[{self.configs.get(ARG_FILE)}] -> [{parent}]')
            return self.build_dependencies(parent, parent_config, branches)
        else:
            return branches

    def validate(self, path, dataset):
        try:
            # for path, value in self.configs.items():
            # ignore the "template" or some other customized ignored configs
            if not any(map(lambda x: path.startswith(x), self.ignore_paths)):

                # check parent object
                parent = dataset.get(ARG_PARENT)
                if parent and parent not in self.configs:
                    raise GErrorValue(f'Parent path is invalid: [{parent}]')

                # resolve object from metadata json
                return self.model.parse_obj(dataset)

        except ValidationError as e:
            TQHelper.post(message=f'Failed to validate object [{path}]',
                          payload=str(e),
                          msg_status=MSGStatusCodes.error)
            raise e
