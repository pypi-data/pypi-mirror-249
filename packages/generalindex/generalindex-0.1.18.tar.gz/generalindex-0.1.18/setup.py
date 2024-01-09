import os

import setuptools


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generalindex",
    version="0.1.18",
    author="General Index",
    author_email="info@general-index.com",
    description="Python SDK for the General Index platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.general-index.com/",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"
                 ],
    install_requires=[
        'requests>=2.31.0',
        'urllib3>=2.1.0',
        'deprecated>=1.2.14'
    ],
    python_requires='>=3.6',
    cmdclass={
        'clean': CleanCommand,
    }
)
