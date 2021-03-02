import setuptools

with open('UserGuide.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yaps-lib',
    version='0.0.1',
    author='Victor Krook',
    author_email='victorkrook96@gmail.com',
    description='A lightweight publish, subscribe library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/victorhook/yaps',
    project_urls={
        'Bug Tracker': 'https://github.com/victorhook/yaps/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    scripts=[
        'yaps/scripts/yaps-publish',
        'yaps/scripts/yaps-subscribe',
        'yaps/scripts/yaps-server',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
)
