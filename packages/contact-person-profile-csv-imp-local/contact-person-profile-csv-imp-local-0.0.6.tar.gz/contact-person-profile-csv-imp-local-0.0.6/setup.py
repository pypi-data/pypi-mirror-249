import setuptools
# Each Python project should have pyproject.toml or setup.py
# TODO: Please create pyproject.toml instead of setup.py (delete the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away from needing to generate a setup.py file to enable editable installs - We might able to delete this file in the near future
setuptools.setup(
     # TODO: Please update the name and delete this line i.e. XXX-local or XXX-remote (without the -python-package suffix). Only lower case

     name='contact-person-profile-csv-imp-local',  
     # TODO: Please update the URL below
     version='0.0.6', # https://pypi.org/project/contact-person-profile-csv-imp-local/ # noqa E501
     author="Circles",
     author_email="info@circles.life",
     description="PyPI Package for Circles CSVToContactPersonProfile-local Local/Remote Python", # noqa E501
     long_description="This is a package for sharing common XXX function used in different repositories", # noqa E501
     long_description_content_type="text/markdown",
     url="https://github.com/circles",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )
