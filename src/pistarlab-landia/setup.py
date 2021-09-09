from setuptools import setup, find_packages, convert_path
import glob
import json
manifest_files = [name.replace("pistarlab_landia/","",1) for name in glob.glob("pistarlab_landia/manifest_files/**",recursive=True)]


def get_version():
  ver_path = convert_path('pistarlab_landia/pistarlab_extension..py')
  with open(ver_path) as ver_file:
      exec(ver_file.read(), main_ns)


setup(
    name="pistarlab-landia",
    version="0.0.1.dev0",
    author="piSTAR.ai",
    author_email="",
    description="",
    long_description='',
    url="https://github.com/pistarlab/pistarlab/extensions",
    license='',
    install_requires=["landia @ https://github.com/pistarlab/landia/archive/ctf.zip#egg=landia-0.0.1.dev0"],
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