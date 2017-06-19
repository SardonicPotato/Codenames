from setuptools import setup

setup(
    name='web-server',
    version='0.1.0',
    packages=['webserver', 'solver'],
    package_data={'webserver': ['resources/*', 'templates/*', 'public/*']},
    include_package_data=True,
    install_requires=[
        'cherrypy',
        'jinja2',
        'numpy'
    ],
    extra_requires={
        'Util': ['gensim']
    },
    url='',
    license='',
    author='andy',
    author_email='',
    description=''
)
