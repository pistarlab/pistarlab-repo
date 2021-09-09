from setuptools import setup, find_packages
import glob
from distutils.util import convert_path

EXT_MODULE_NAME = 'pistarlab_unity_envs'

manifest_files = [name.replace(f"{EXT_MODULE_NAME}/","",1) for name in glob.glob(f"{EXT_MODULE_NAME}/manifest_files/**",recursive=True)]
env_files = [name.replace(f"{EXT_MODULE_NAME}/","",1) for name in glob.glob(f"{EXT_MODULE_NAME}/envs/**",recursive=True)]

setup(
    name="pistarlab-unity-envs",
    version="0.0.1.dev0",
    author="",
    author_email="",
    description="TODO",
    long_description='',
    url="https://github.com/pistarlab/pistarlab-repo/src/extensions",
    license='',
    install_requires=['mlagents',"mlagents-envs"],
    package_data={EXT_MODULE_NAME: ['README.md',"*.json","*.jpg", "manifest_files", "manifest.json","pistarlab_extension.json"] + manifest_files + env_files
      },
    packages=find_packages(),
    entry_points={ },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6',
)