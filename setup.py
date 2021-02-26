import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yaps-victorhook',
    version='0.0.8',
    author='Victor Krook',
    author_email='victorkrook96@gmail.com',
    description='A lightweight publish, subscribe protocol api',
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
    entry_points={
        'console_scripts': [
            'yaps-server = yaps.scripts.server:main',
            'yaps-publish = yaps.scripts.publish:main',
            'yaps-subscribe = yaps.scripts.subscribe:main'
        ],
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
)
