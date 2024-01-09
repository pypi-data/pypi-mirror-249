
from setuptools import setup, find_packages
with open('README.md',"r",encoding='utf-8') as f:
    long_description=f.read()

setup(
    name="NodeStickyLinks", #更改项目名字，并不是后面要import的 package name
    version="0.2",
    license="MIT",
    description="NodeStickyLinks by python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Xiangfang Zeng",
    author_email="xiangfangzeng15@gmail.com",
    url="https://github.com/SZUVIZ/StickyLinks",
    packages=find_packages(),
    install_requires=[
        'pycairo>=1.19.1',
        'pandas',
        'networkx',
    ],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        #target python version
        'Programming Language :: Python :: 3.9 ',
    ],
     )