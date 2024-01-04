from setuptools import setup, find_packages

setup(
    name='OnyxRequests',
    version='0.1.0',
    packages=find_packages(),
    description='Small modification of python requests.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='mmenamore',
    author_email='markvega2023@outlook.com',
    url='https://github.com/longold/OnyxRequests',
    install_requires=[
        'requests>=2.25.1', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


# 