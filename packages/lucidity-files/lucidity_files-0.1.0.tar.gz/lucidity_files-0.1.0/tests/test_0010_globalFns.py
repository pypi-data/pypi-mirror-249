'''
Created on Aug 28, 2021

@author: Eduardo Grana
'''

import inspect
import unittest
import functools

# this is awful, need to setup environment properly!
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dependencies'))

from tests import test_helper
import lucidity_files

# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string

WHITELIST = []
# WHITELIST = ['0040']


class Test(unittest.TestCase):
    @unittest.skipIf((WHITELIST and '0010' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0010_discover_templates(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        templates = lucidity_files.discover_templates(paths=test_helper.getTemplatesPaths())
        for t in templates:
            msg = 'An objects listed are not TemplateFile but "{}"'.format(str(type(t)))
            self.assertIsInstance(t, lucidity_files.TemplateFile, msg)
            print('"{}" is an ok type'.format(t))

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0020' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0020_get_template(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))
        templates = lucidity_files.discover_templates(paths=test_helper.getTemplatesPaths())

        # check names
        name_list = ['output_part_single_layer', 'source_no_folder']
        for name in name_list:
            template = lucidity_files.get_template(name, templates)
            template_name = template.lucidity_name
            msg = 'Got a template but with wrong name: "{}" instead of "{}"'.format(template_name, name)
            self.assertEqual(template_name, name, msg)
            print('Got template {} for name {}'.format(template, name))

        # must raise exception if not found
        callableObj = functools.partial(lucidity_files.get_template, 'nonexistingtemplate', templates)
        self.assertRaises(Exception, callableObj)
        print('Got exception for non existing name {} OK!'.format(name))

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0030' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0030_format(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        data_list = [
            (
                {
                    'layer': 'ol',
                    'task': 'model',
                    'group': 'se2',
                    'name': 'final',
                    'entitytype': 'shot',
                    'outputtype': 'img',
                    'publish': 'publish',
                    'entity': '1030',
                    'project': 'testprj',
                    'ext': 'exr',
                    'version': '001',
                    'XTDXrootout': 'C:\\test\\Xfolder',
                    'step': 'art',
                },
                r'C:\test\Xfolder\testprj\shot\se2\1030\art\publish\model\img\1030_art_model_final_v001\ol\1030_art_model_final_v001_ol.exr',
                'output_part_single_layer',
            ),
        ]

        templates = lucidity_files.discover_templates(paths=test_helper.getTemplatesPaths())

        for data, expected_path, template_name in data_list:
            matches = lucidity_files.format_(data, templates, match_multiple=False)
            path, template = matches[0]

            # check count
            msg = 'Got multiple matches instead of one: {}'.format(matches)
            self.assertEqual(len(matches), 1, msg)
            print('Got template {} \nfor data {}\npath: {}'.format(template, data, path))

            # check path
            msg = 'Expected path {} and got {}'.format(expected_path, path)
            self.assertEqual(expected_path, path, msg)
            print('Got path OK: {}'.format(path))

            # check template
            msg = 'Expected template {} and got {}'.format(template_name, template.lucidity_name)
            self.assertEqual(template_name, template.lucidity_name, msg)
            print('Got template OK: {}'.format(template.lucidity_name))

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0040' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0040_parse(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))
        path_list = [
            (
                r'D:\work\pilates_test\testprj\shot\se2\1030\art\publish\model\img\1030_art_model_final_v001\ol\1030_art_model_final_v001_ol.exr',
                {
                    'layer': 'ol',
                    'task': 'model',
                    'group': 'se2',
                    'name': 'final',
                    'entitytype': 'shot',
                    'outputtype': 'img',
                    'publish': 'publish',
                    'entity': '1030',
                    'project': 'testprj',
                    'ext': 'exr',
                    'version': '001',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'step': 'art',
                },
                'output_part_single_layer',
            ),
        ]

        templates = lucidity_files.discover_templates(paths=test_helper.getTemplatesPaths())

        for path, expected_data, template_name in path_list:
            matches = lucidity_files.parse(path, templates, match_multiple=False)
            data, template = matches[0]

            # check count
            msg = 'Got multiple matches instead of one: {}'.format(matches)
            self.assertEqual(len(matches), 1, msg)
            print('Got template {} \nfor path {}\ndata: {}'.format(template, path, data))

            # check path
            msg = 'Expected data {} and got {}'.format(expected_data, data)
            self.assertEqual(expected_data, data, msg)
            print('Got data OK: {}'.format(data))

            # check template
            msg = 'Expected template {} and got {}'.format(template_name, template.lucidity_name)
            self.assertEqual(template_name, template.lucidity_name, msg)
            print('Got template OK: {}'.format(template.lucidity_name))

        print('Finished test {}'.format(inspect.stack()[0][3]))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
