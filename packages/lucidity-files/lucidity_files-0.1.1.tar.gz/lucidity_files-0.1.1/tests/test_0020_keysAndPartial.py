'''
Created on Aug 28, 2021

@author: Eduardo Grana
'''
import inspect
import unittest

from tests import test_helper

WHITELIST = []
# WHITELIST = ['0015']

# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string


class Test(unittest.TestCase):
    @unittest.skipIf((WHITELIST and '0010' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0010_orderedTokens(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')
        r = template._getOrderedKeyTokens(template.l_template.pattern)

        expected = [
            'XTDXrootout',
            'project',
            'entitytype',
            'group',
            'entity',
            'step',
            'publish',
            'task',
            'outputtype',
            'name',
            'version',
            'layer',
            'ext',
        ]
        msg = 'Expected {} and got {}'.format(expected, r)
        self.assertEqual(r, expected, msg)

        print(r)

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0015' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0015_orderedTokens(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')
        r = template.getKeys(ordered=True)

        expected = [
            'project',
            'entitytype',
            'group',
            'entity',
            'step',
            'publish',
            'task',
            'outputtype',
            'name',
            'version',
            'layer',
            'ext',
        ]
        msg = 'Expected {} and got {}'.format(expected, r)
        self.assertEqual(r, expected, msg)

        print(r)

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0020' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0020_partialPattern(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')
        r = template._getPartialPattern('entity')

        expected = '{XTDXrootout:[\\w_.\\-:]+}/{project}/{entitytype}/{group}/{entity}'

        msg = 'Expected {} and got {}'.format(expected, r)
        self.assertEqual(r, expected, msg)

        print(r)

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0030' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0030_partialPattern(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')

        template_file = template.getPartialTemplateFile('entity')
        paths = template_file.getPaths()
        datas = [template_file.parse(p) for p in paths]

        r = (paths, datas)

        expected = (
            [
                'D:\\work\\pilates_test\\testprj\\shot\\se2\\1010',
                'D:\\work\\pilates_test\\testprj\\shot\\se2\\1020',
                'D:\\work\\pilates_test\\testprj\\shot\\se2\\1030',
                'D:\\work\\pilates_test\\testprj\\shot\\seq\\1010',
                'D:\\work\\pilates_test\\testprj\\shot\\seq\\1020',
                'D:\\work\\pilates_test\\testprj\\shot\\seq\\1030',
            ],
            [
                {
                    'project': 'testprj',
                    'group': 'se2',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'entitytype': 'shot',
                    'entity': '1010',
                },
                {
                    'project': 'testprj',
                    'group': 'se2',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'entitytype': 'shot',
                    'entity': '1020',
                },
                {
                    'project': 'testprj',
                    'group': 'se2',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'entitytype': 'shot',
                    'entity': '1030',
                },
                {
                    'project': 'testprj',
                    'group': 'seq',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'entitytype': 'shot',
                    'entity': '1010',
                },
                {
                    'project': 'testprj',
                    'group': 'seq',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'entitytype': 'shot',
                    'entity': '1020',
                },
                {
                    'project': 'testprj',
                    'group': 'seq',
                    'XTDXrootout': 'D:/work/pilates_test',
                    'entitytype': 'shot',
                    'entity': '1030',
                },
            ],
        )

        msg = 'Expected {} and got {}'.format(expected, r)
        self.assertEqual(r, expected, msg)

        print(r)

        print('Finished test {}'.format(inspect.stack()[0][3]))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
