from setuptools import setup, find_packages
import glob

manifest_files = [name.replace("pistarlab_envs_gym_minigrid/","",1) for name in glob.glob("pistarlab_petting_zoo/manifest_files/**",recursive=True)]


setup(
    name="pistarlab-envs-gym-minigrid",
    version="0.0.1",
    author="piSTAR",
    author_email="pistar3.14@gmail.com",
    description="https://github.com/maximecb/gym-minigrid",
    long_description='This is a pistarlab extension',
    url="https://github.com/pistarlab/pistarlab/extensions",
    license='',
    install_requires=['gym-minigrid'],
    package_data={'pistarlab-envs-gym-minigrid':  ['README.md',"*.json","*.jpg", "manifest_files", "manifest.json","pistarlab_extension.json"] + manifest_files
      },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6',
)