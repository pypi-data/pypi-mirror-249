"""Module for the main class."""
import copy
import glob
import re

import lucidity  # used only for errors and creating in one go

from . import file_utils

# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string


class TemplateFile(object):
    """Class that wraps lucidity template adding the ability for listing files and partial templates."""

    MAX_FILES_COUNT = 999999
    DEFAULT_VALUES_KEY = 'default_values'
    ROOT_KEY = 'roots'

    @classmethod
    def create(
        cls,
        name,
        pattern,
        default_placeholder_expression='[\\w_.\\-]+',
        template_resolver=None,
        default_values=None,
        roots=None,
    ):
        """Creates a TemplateFile object initialized.

        Args:
            name (str): Name of the template.
            pattern (str): File pattern to use with lucidity.
            default_placeholder_expression (str, optional): Pseudo regex used in the pattern fields.
                Defaults to '[\\w_.\\-]+'.
            template_resolver (lucidity.Resolver, optional): A resolver for the inner templates. Defaults to None.
            default_values (dict, optional): A mapping between values and their defaults. Defaults to None.
            roots (dict, optional): A mapping between root names and root paths. Defaults to None.

        Returns:
            TemplateFile: The initialized template file.
        """
        l_template = lucidity.Template(
            name,
            pattern,
            anchor=lucidity.Template.ANCHOR_BOTH,
            default_placeholder_expression=default_placeholder_expression,
            duplicate_placeholder_mode=lucidity.Template.STRICT,
            template_resolver=template_resolver,
        )

        return cls(l_template, default_values=default_values, roots=roots)

    def __init__(self, l_template, default_values=None, roots=None):
        '''

        Args:
            l_template (lucidity.Template): the template to wrap
            default_values (dict): the default values for some key in lucidity template. This overrides values added to
                the template
            roots (dict): the root values for the templates. This overrides values added to the template
        '''

        self.l_template = l_template
        # without STRICT the whole system breaks, because you could have multiple values for same key
        self.l_template.duplicate_placeholder_mode = self.l_template.STRICT
        # without ANCHOR_BOTH the whole system breaks, because you could have partial matches
        self.l_template._anchor = self.l_template.ANCHOR_BOTH
        # Check that supplied pattern is valid and able to be compiled.
        self.l_template._construct_regular_expression(self.l_template.pattern)

        self.roots = self._resolveParam(self.ROOT_KEY, roots, {})
        self.default_values = self._resolveParam(self.DEFAULT_VALUES_KEY, default_values, {})

    def __str__(self):
        msg = '<TemplateFile id:{} name:{} pattern:{}>'.format(id(self), self.lucidity_name, self.l_template.pattern)
        return msg

    def _resolveParam(self, key, override, default):
        '''Helper to resolve parameters.

        Args:
            key (str): key to resolve
            override (obj): the overriding value, can be None in case it's not overridden.
            default (obj): the value to use in case it's not defined on the template or the override.

        Returns:
            obj: the resolved value.
        '''
        # Resolution order of roots and default values
        # 1) args in this init overrides the values in the template
        if override is not None:
            return override

        # 2) if not defined in args, it uses templates ones
        if hasattr(self.l_template, key):
            return getattr(self.l_template, key)

        # 3) if there is none on the template and non defined in args, it assumes there is no need for them and a
        # functional default is returned (this should be passed as argument)
        return default

    # lucidity stuff ----

    @property
    def lucidity_name(self):
        '''returns lucidity template name'''
        return self.l_template.name

    def parse(self, path, return_roots=True):
        '''Wraps lucidity parse function.

        Args:
            path (str): the path to parse
            return_roots (bool): whether or not to return the roots in the result

        Returns:
            dict: the key values pairs

        Raises
            lucidity.ParseError if path cant be parsed.
        '''

        path = file_utils.toLucidityPath(path)

        # replace root path so it matches
        r_path, root_found = self._replaceKeysOnPath(path, self.roots)

        data = self.l_template.parse(r_path)

        # add root real value or remove the key (otherwise you'll get 'XTDXrootout': 'XTDXrootout')
        if return_roots:
            data.update(root_found)
        else:
            for root_key in root_found:
                data.pop(root_key)

        return data

    def _replaceKeysOnPath(self, path, key_dict):
        '''Replaces keys in a template path with their corresponding values.

        Args:
            path (str): path to replace roots on.
            key_dict (dict): the dict of keys to find and values to put in replacement.

        Returns:
            str: the path with the roots replaced.

        Notes:
            TODO: this dont depend on self, could be extracted
        '''
        found = {}

        # search for each value and replace with the key
        for k, v in key_dict.items():
            # because of bars, we need to convert the values to something compatible
            v_safe = file_utils.toLucidityPath(v)
            if v_safe not in path:
                continue

            # replace on the path with the key
            path = re.sub(re.escape(v_safe), k, path, re.IGNORECASE)

            found[k] = v_safe

        return path, found

    def format(self, data):
        '''wraps lucidity format function.

        Args:
            data (dict): the dict with the keys to find in template and the values to replace the keys found.

        Returns:
            str: the builded path.

        Raises
            lucidity.FormatError if path cant be formatted.
        '''

        # order is 1) default values 2) roots overrides def values 3) data provided overrides all
        f_data = copy.deepcopy(self.default_values)
        f_data.update(self.roots)
        f_data.update(data)

        formatted = self.l_template.format(f_data)

        # adjust path to current file system
        path = file_utils.toCleanPath(formatted)
        return path

    # list files ----

    def _getGlobPath(self, fields, skip_keys=None):
        '''Builds a glob path to use with python's glob function.

        Args:
            fields (dict): the fields to define. Undefined fields will become an * .
            skip_keys (list): the keys to ignore from the fields dict.

        Returns:
            str: a path to use with glob.
        '''

        keys = self.l_template.keys()
        all_fields = {k: '*' for k in keys}

        # shouldn't we replace the roots?
        if self.roots:
            for root_key, root_value in self.roots.items():
                if root_key in keys:
                    all_fields[root_key] = root_value

        update_fields = {k: v for k, v in fields.items() if not skip_keys or k not in skip_keys}
        all_fields.update(update_fields)

        glob_path = self.format(all_fields)

        return glob_path

    def getPaths(self, fields=None, skip_keys=None, strict_check=True, max_count=None):
        '''Returns the found paths that matched this template.

        Args:
            fields (dict): the fields to define. Undefined fields will become an wildcard.
            skip_keys (list): the keys to ignore from the fields dict.
            strict_check (bool): whether or not to strictly check that the paths found can be parsed (takes more time).
            max_count (int): maximum files to return.

        Returns:
            list[str]: the list of paths found that matched the template and the fields.
        '''

        # resolve optional parameters
        if fields is None:
            fields = {}

        if max_count is None:
            max_count = self.MAX_FILES_COUNT

        # build glob path to use
        glob_path = self._getGlobPath(fields, skip_keys=skip_keys)

        result = []
        count = 0
        for path in glob.iglob(glob_path):
            if max_count <= count:
                break

            # parse path to strictly check
            if strict_check and not self.checkPath(path):
                continue

            result.append(file_utils.toCleanPath(path))
            count += 1

        return result

    # check ----

    def checkPath(self, path):
        '''Check if path is consistent with this template.

        Args:
            path (str): the path to check.

        Returns:
            bool: True if check is passed, False otherwise.
        '''
        try:
            self.parse(path)

        except lucidity.ParseError:
            return False
        return True

    def checkData(self, data):
        '''Check if data is consistent with this template.

        Args:
            data (dict): the data to check.

        Returns:
            bool: True if check is passed, False otherwise.
        '''
        try:
            self.format(data)

        except lucidity.FormatError:
            return False
        return True

    def roundTripCheckData(self, data):
        '''Check if data is consistent with this template by converting back and forth.

        Args:
            data (dict): the data to check.

        Returns:
            bool: True if check is passed, False otherwise.

        Notes:
            TODO: move to tests!
        '''

        # convert to path and back to data
        built_path = self.format(data)
        built_data = self.parse(built_path)

        # check if result is the same
        if built_data != data:
            return False

        return True

    def roundTripCheckPath(self, path, platform=None):
        '''Check if path is consistent with this template by converting back and forth.

        Args:
            path (str): the path to check.
            platform (str): the name of the platform as defined in file_utils.

        Returns:
            bool: True if check is passed, False otherwise.

        Notes:
            TODO: move to tests!
        '''
        # convert to data and back to path
        built_data = self.parse(path)
        built_path = self.format(built_data)

        # check if result is the same (we need to be careful because of windows)
        compare_path = file_utils.toComparePath(path, platform=platform)
        compare_built_path = file_utils.toComparePath(built_path, platform=platform)
        if compare_path != compare_built_path:
            return False

        return True

    # keys ---

    def getRawKeys(self):
        '''Get the keys as defined in lucidity template.

        Args:
            None.

        Returns:
            list: the unordered list of keys.
        '''
        return list(self.l_template.keys())

    def getDefaultKeys(self):
        '''Get the keys that have a default value.

        Args:
            None.

        Returns:
            list: the unordered list of keys.
        '''
        return list(self.default_values.keys())

    def getRootKeys(self):
        '''Get the keys that are root.

        Args:
            None.

        Returns:
            list: the unordered list of keys.
        '''
        return list(self.roots.keys())

    def getKeys(self, ordered=False, no_dups=True):
        '''Get the keys as defined in lucidity template but without roots.

        Args:
            ordered (bool): whether or not to order the keys.
            no_dups (bool): whether or not to remove the duplicates keeping the first
                appearance for each key. Only valid for ordered.

        Returns:
            list: the unordered list of keys.
        '''
        if ordered:
            keys = self._getOrderedKeyTokens(self.l_template.pattern, no_dups=no_dups)
        else:
            keys = self.getRawKeys()

        # root keys should be removed?
        root_keys = self.getRootKeys()
        keys = [k for k in keys[:] if k not in root_keys]
        return keys

    def _getOrderedKeyTokens(self, pattern, no_dups=True):
        '''return keys found in a pattern in order.

        Args:
            pattern (str): the lucidity pattern.
            no_dups (bool): whether or not to remove the duplicates keeping the first
                appearance for each key.

        Returns:
            list[str]: the keys in order.
        '''
        # remove extra specs in pattern
        ns_pattern = self.l_template._construct_format_specification(pattern)  # pylint: disable=protected-access
        # list all keys
        tokens = self.l_template._PLAIN_PLACEHOLDER_REGEX.findall(ns_pattern)  # pylint: disable=protected-access

        # remove dups if requested while keeping order
        if no_dups:
            tokens_nd = []
            for key in tokens:
                if key not in tokens_nd:
                    tokens_nd.append(key)
            tokens = tokens_nd

        return tokens

    # partial paths ---

    def _getPartialPattern(self, split_key):
        '''return a partial pattern splitting by a key and up to the path separator

        Args:
            split_key (str): the key to do the split at (inclusive).

        Returns:
            str or None: the lucidity template pattern or None if it could not be made.
        '''

        # key must exists (and must not be a root key)
        if split_key not in self.getKeys():
            print('Get Partial Pattern: Cant split by a key ({}) not in the pattern!'.format(split_key))
            return None

        pattern = self.l_template.expanded_pattern()
        rexp = '(^.*?{{{}(:|}}).*?)/'.format(split_key)
        match = re.match(rexp, pattern)

        if not match:
            print('Get Partial Pattern: Cant split by a key ({})!'.format(split_key))
            return

        partial_pattern = match.group(1)
        return partial_pattern

    def getPartialTemplateFile(self, split_key):
        '''Returns a TemplateFile object with a partial pattern.

        Args:
            split_key (str): the key to do the split at (inclusive).

        Returns:
            TemplateFile or None: the TemplateFile with the partial pattern or None if it could not be made.

        Examples:
            Get paths from partial template and get data too

            partial_template_file = self.getPartialTemplateFile('entity')
            paths = partial_template_file.getPaths()
            datas = [template_file.parse(p) for p in paths]
        '''

        # get partial pattern
        partial_pattern = self._getPartialPattern(split_key)
        if partial_pattern is None:
            raise KeyError('Cant build partial pattern with key {}'.format(split_key))

        # duplicate template and replace pattern
        l_temp = copy.deepcopy(self.l_template)
        l_temp._pattern = partial_pattern  # pylint: disable=protected-access
        l_temp._construct_regular_expression(l_temp.pattern)  # pylint: disable=protected-access

        # build new template file
        temp_file = TemplateFile(l_temp, roots=self.roots, default_values=self.default_values)
        return temp_file
