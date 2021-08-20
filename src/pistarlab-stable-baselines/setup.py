from setuptools import setup, find_packages

setup(
    name="pistarlab-stable-baselines",
    version="0.0.1-dev0",
    author="",
    author_email="",
    description="Stable Baselines",
    long_description='This is a pistarlab extension',
    url="https://github.com/pistarlab/pistarlab/extensions",
    license='',
    install_requires=['stable-baselines3'],
    package_data={'pistarlab-stable-baselines': ['README.md']
      },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6',
)