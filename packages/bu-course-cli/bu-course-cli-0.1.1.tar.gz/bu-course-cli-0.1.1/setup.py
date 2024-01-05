from setuptools import setup, find_packages

setup(
    name='bu-course-cli',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'requests', # Make sure to include any additional dependencies your CLI may have
    ],
    entry_points={
        'console_scripts': [
            'bu-course-cli=bu_course_cli.cli:main', # Corrected entry point
        ],
    },
)
