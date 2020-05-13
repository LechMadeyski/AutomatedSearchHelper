import os
from setuptools import setup, find_packages
from setuptools.command.install import install


def _post_install():
    import nltk
    nltk.download('punkt')


class MyInstall(install):
    def run(self):
        install.run(self)
        self.execute(_post_install, [], msg='running _post_install task')


setup(
    name="AutomatedSearchHelper",
    version="0.0.1",
    author="Marek Sośnicki",
    packages=find_packages(),
    cmdclass={'install': MyInstall},
    install_requires=[
        'flask',
        'flask_wtf',
        'flask_jsglue',
        'werkzeug',
        'wtforms',
        'beautifulsoup4',
        'crossrefapi',
        'slate',
        'utils',
        'rispy',
        'cattrs',
        'nltk',
        'bibtexparser',
        'selenium'],
    scripts=[
        'run_articles_download.py',
        'run_articles_search.py',
        'run_results_html_generation.py',
        'run_whole_search.py',
        'create_proxy_configuration.py'
    ]
)
