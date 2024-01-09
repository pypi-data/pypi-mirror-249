from setuptools import find_packages, setup

install_requires = ("requests", "emzed>=3.0.0a1")

setup(
    name="emzed_ext_mzmine2",
    version="3.0.0a2",
    description="emzed extension to access some algorithms from mzmine2",
    long_description="emzed extension to access some algorithms from mzmine2",
    long_description_content_type="text/x-rst",
    url="",
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
)
