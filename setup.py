import setuptools

with open('README.txt') as readme_stream:
    long_description = readme_stream.read()

setup_params = dict(
    name='librarypaste',
    use_scm_version=True,
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
        'genshi',
        'cherrypy',
        'PyYAML',
    ],
    setup_requires=[
        'setuptools_scm',
        'pytest-runner>=2.1',
    ],
    tests_require=[
        'pytest',
        'pymongo>=3',
        'jaraco.test',
    ],
    zip_safe=False,
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
