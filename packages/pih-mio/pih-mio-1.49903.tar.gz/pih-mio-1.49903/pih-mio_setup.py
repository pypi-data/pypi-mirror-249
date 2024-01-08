import shutil
import os
import importlib.util
import sys
from setuptools import setup

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A
from pih.tools import j
from MobileHelperService.const import MODULE_NAME, VERSION

#########################################################################################################
"""
1. python pih-mio_setup.py sdist --dist-dir dist\pih-mio bdist_wheel --dist-dir dist\pih-mio build --build-base uild\pih-mio
2. twine upload --repository pypi dist/pih-mio/*
3. pip install pih-mio -U
"""
module_name: str = MODULE_NAME
folder = j(("//pih/facade/dist/", module_name))
for filename in os.listdir(folder):
    file_path = A.PTH.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as error:
        print("Failed to delete %s. Reason: %s" % (file_path, error))

setup(
    name=module_name,
    entry_points={
        "console_scripts": [
            j((module_name, "=MobileHelperService.__main__:start")),
        ]
    },
    version=VERSION,
    description="PIH Mobile Helper library",
    long_description_content_type="text/markdown",
    url="https://pacifichosp.com/",
    author="Nikita Karachentsev",
    author_email="it@pacifichosp.com",
    license="MIT",
    classifiers=[],
    packages=["MobileHelperService", "shared"],
    include_package_data=True,
    install_requires=["pih", j((module_name, "-content"))],
)
