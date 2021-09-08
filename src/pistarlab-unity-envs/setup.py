from setuptools import setup, find_packages
import glob

manifest_files = [name.replace("pistarlab_unity_envs/","",1) for name in glob.glob("pistarlab_unity_envs/manifest_files/**",recursive=True)]
env_files = [name.replace("pistarlab_unity_envs/","",1) for name in glob.glob("pistarlab_unity_envs/envs/**",recursive=True)]

setup(
    name="pistarlab-unity-envs",
    version="0.0.1",
    author="",
    author_email="",
    description="TODO",
    long_description='',
    url="https://github.com/pistarlab/pistarlab-repo/src/extensions",
    license='',
    install_requires=['mlagents',"mlagents-envs"],
    package_data={'pistarlab_unity_envs': ['README.md',"*.json","*.jpg", "manifest_files", "manifest.json","pistarlab_extension.json"] + manifest_files + env_files
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