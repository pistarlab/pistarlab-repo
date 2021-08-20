from setuptools import setup, find_packages
import glob

manifest_files = [name.replace("pistarlab_landia/","",1) for name in glob.glob("pistarlab_landia/manifest_files/**",recursive=True)]

setup(
    name="pistarlab-landia",
    version="0.0.1",
    author="pistar",
    author_email="",
    description="",
    long_description='',
    url="https://github.com/pistarlab/pistarlab/extensions",
    license='',
    install_requires=[],
    package_data={'pistarlab_landia': ['README.md',"*.json","*.jpg", "manifest_files", "manifest.json","pistarlab_extension.json"] + manifest_files
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