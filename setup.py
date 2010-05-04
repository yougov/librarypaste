from setuptools import setup

import librarypaste

setup(
        name='librarypaste',
        version=librarypaste.version,
        author='Jamie Turner',
        author_email='jamie@jamwt.com',
        url='http://bitbucket.org/chmullig/librarypaste/',
        description='Simple pastebin',
        long_description='Simple pastebin',
        license='MIT',
        packages=['librarypaste'],
        package_dir={'librarypaste':'librarypaste'},
        include_package_data=True,
        entry_points={
            'console_scripts':['librarypaste=librarypaste.librarypaste:main'],
        },
        install_requires=[
            'pygments',
            'Mako',
            'simplejson',
            'cherrypy',
            'routes < 1.12',
        ],
        zip_safe=False,
)
