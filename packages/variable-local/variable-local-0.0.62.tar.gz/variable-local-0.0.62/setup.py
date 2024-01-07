import setuptools

PACKAGE_NAME = 'variable-local'
package_dir = PACKAGE_NAME.replace('-', '_')

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.62',  # https://pypi.org/project/variable-local
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles <project-name> Local/Remote Python",
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
    install_requires=[
        'logger-local',
        'profiles-local',
        'language_local',
        'database-mysql-local',
    ],
)
