import setuptools

with open('README') as readme_stream:
    long_description = readme_stream.read()

setuptools.setup(
    name='librarypaste',
    use_hg_version=dict(increment='0.1'),
    author='YouGov, Plc.',
    author_email='open-source@yougov.com',
    url='http://bitbucket.org/yougov/librarypaste/',
    description='A simple pastebin implementation in Python',
    long_description=long_description,
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'librarypaste=librarypaste.launch:main',
        ],
    },
    install_requires=[
        'pygments',
        'Mako',
        'cherrypy',
        'PyYAML',
    ],
    setup_requires=[
        'hgtools',
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pymongo',
        'jaraco.test',
    ],
    zip_safe=False,
)
