'''
TODO: not sure if match multiple makes sense

'''
import lucidity  # @UnresolvedImport

from .lucidity_files import TemplateFile
from . import file_utils

# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string

__version__ = '0.1.0'


def discover_templates(paths=None, recursive=True, default_values=None, roots=None):
    '''Wraps lucidity to return TemplateFiles instead for lucidity templates'''

    templates = lucidity.discover_templates(paths=paths, recursive=recursive)

    f_templates = [TemplateFile(t, default_values=default_values, roots=roots) for t in templates]

    return f_templates


def parse(path, templates, match_multiple=False, return_roots=True):
    '''Finds a template from templates that matches path and returns the parsed values and the matching template.
    Args:
        path (str): the path to match
        templates (list[TemplateFile]): the list of template files to match against the path
        match_multiple (bool): whether to return just the first or all that matches
        return_roots (bool): whether or not to return the roots in the result
    Returns:
        list[tuple(dict, TemplateFile)]: the list of the parsed data and template
    '''

    matches = []
    for template in templates:
        try:
            data = template.parse(path, return_roots=return_roots)
        except Exception:  # pylint: disable=broad-exception-caught
            continue

        if not match_multiple:
            return [(data, template)]

        matches.append((data, template))

    # if we are not looking for multiple matches, the only way of getting here is that there is no match
    if not match_multiple or not matches:
        raise NameError('Could no match path "{}" to any of the supplied templates.'.format(path))

    return matches


def format_(data, templates, match_multiple=False):
    '''Finds a template from templates that matches data and returns the builded path and the matching template.
    Args:
        data (dict): the data to construct a path
        templates (list[TemplateFile]): the list of template files to match against the path
        match_multiple (bool): whether to return just the first or all that matches
    Returns:
        list[tuple(path, TemplateFile)]: the list of the builded path and template
    '''
    matches = []
    for template in templates:
        try:
            path = template.format(data)
        except Exception:  # pylint: disable=broad-exception-caught
            continue

        if not match_multiple:
            return [(path, template)]

        matches.append((path, template))

    # if we are not looking for multiple matches, the only way of getting here is that there is no match
    if not match_multiple or not matches:
        raise NameError('Could no match data "{}" to any of the supplied templates.'.format(data))

    return matches


def get_template(name, templates):
    '''Finds a template by name from a provided list
    Args:
        name (str): the name of the template
        templates (list[TemplateFile]): the list of templates to look for the one with name
    Raises:
        Exception: if no template has the name (or no templates provided)

    '''
    for template in templates:
        if template.lucidity_name == name:
            return template

    raise NameError('Could not find a template named "{}"'.format(name))


__all__ = ['TemplateFile', 'file_utils', 'discover_templates', 'parse', 'format_', 'get_template']
