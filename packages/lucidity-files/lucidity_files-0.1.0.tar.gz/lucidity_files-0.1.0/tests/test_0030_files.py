'''
Created on Aug 28, 2021

@author: Eduardo Grana
'''
import unittest
import random
import inspect
import copy
import lucidity_files

import test_helper

# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string


WHITELIST = []
# WHITELIST = ['0020']
# WHITELIST = ['0030']


TEST_DATA = {
    'ext': ['ma', 'exr'],
    'layer': ['ol', 'bg'],
    'task': ['anim', 'model'],
    'group': ['seq', 'se2'],
    'name': ['test', 'final'],
    'entitytype': ['shot'],
    'outputtype': ['img'],
    'publish': ['work', 'publish'],
    'entity': ['1010', '1020', '1030'],
    'project': ['testprj'],
    'step': ['art'],
    'version': ['001', '002', '003'],
    'XTDXrootout': [r'D:\work\pilates_test'],
}


class Test(unittest.TestCase):
    @unittest.skipIf((WHITELIST and '0010' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0010_create(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')
        print(template.lucidity_name)

        for _ in range(10):  # @UnusedVariable
            data = {k: random.choice(TEST_DATA.get(k, ['miss'])) for k in template.getRawKeys()}
            path = template.format(data)
            test_helper.touch(path)

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0015' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0015_create(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')
        print(template.lucidity_name)

        this_test_data = copy.deepcopy(TEST_DATA)
        this_test_data['ext'] = ['exr']

        for _ in range(10):  # @UnusedVariable
            data = {k: random.choice(TEST_DATA.get(k, ['miss'])) for k in template.getKeys()}
            path = template.format(data)
            test_helper.touch(path)

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0016' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0016_create_multi(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_all_multi')
        print(template.lucidity_name)

        for _ in range(10):  # @UnusedVariable
            data = {k: random.choice(TEST_DATA.get(k, ['miss'])) for k in template.getKeys()}
            for v in TEST_DATA['version']:
                data['version'] = v
                for f in range(1, 11):
                    data['seq4'] = str(f).zfill(4)
                    path = template.format(data)
                    test_helper.touch(path)

        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0020' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0020_list(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))

        template = test_helper.getTemplateByName('output_part_single_layer')
        paths = template.getPaths(strict_check=True)
        for p in paths:
            print(p)
        print('Finished test {}'.format(inspect.stack()[0][3]))

    @unittest.skipIf((WHITELIST and '0030' not in WHITELIST), 'Whitelist is on for {} only '.format(WHITELIST))
    def test_0030_list(self):
        print('Starting test {}'.format(inspect.stack()[0][3]))
        pattern = '{XTDXrootout:[\\w_.\\-:]+}/{project}/{entitytype}/{group}/{entity}/{step}/{publish}/{task}/{outputtype}/{entity}_{step}_{task}_{name}_v{version}'
        pattern += '/{layer}/{entity}_{step}_{task}_{name}_v{version}_{layer}.{ext}'
        roots = {'XTDXrootout': 'D:/work/pilates_test'}
        template = lucidity_files.TemplateFile.create('test', pattern, roots=roots)
        paths = template.getPaths(strict_check=True)
        for p in paths:
            print(p)
        print('Finished test {}'.format(inspect.stack()[0][3]))


if __name__ == "__main__":
    unittest.main()
