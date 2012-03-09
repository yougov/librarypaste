import setuptools

setuptools.setup(
    name='librarypaste',
    use_hg_version=True,
    author='Jamie Turner',
    author_email='jamie@jamwt.com',
    url='http://bitbucket.org/chmullig/librarypaste/',
    description='Simple pastebin',
    long_description='Simple pastebin',
    license='MIT',
    packages=['librarypaste'],
    package_dir={'librarypaste': 'librarypaste'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'librarypaste=librarypaste.librarypaste:main',
        ],
    },
    install_requires=[
        'pygments',
        'Mako',
        'simplejson',
        'cherrypy',
        'routes < 1.12',
    ],
    setup_requires=[
        'hgtools',
    ],
    zip_safe=False,
)
