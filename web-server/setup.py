from setuptools import setup

setup(
    name='web-server',
    version='0.1.0',
    packages=['webserver', 'solver'],
    package_data={'webserver': ['resources/*', 'templates/*', 'public/*'],
                  'solver': ['data/reduced_embedding_100000.npy', 'data/reduced_vocab_100000.npy']},
    include_package_data=True,
    url='',
    license='',
    author='andy',
    author_email='',
    description=''
)
