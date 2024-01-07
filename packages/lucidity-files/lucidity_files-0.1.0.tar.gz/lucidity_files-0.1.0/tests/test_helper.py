'''
Created on Feb 1, 2022

@author: Eduardo Grana
'''
import os
import lucidity_files


def getTemplatesPaths():
    return [os.path.join(os.path.dirname(__file__), 'templates')]


def getTemplateByName(name):
    ''' get templates in a Lucidity fashion '''
    templates = lucidity_files.discover_templates(paths=getTemplatesPaths())  # @UndefinedVariable
    return lucidity_files.get_template(name, templates)


def touch(path):
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    with open(path, 'w'):
        pass
    print('touched {}'.format(path))
