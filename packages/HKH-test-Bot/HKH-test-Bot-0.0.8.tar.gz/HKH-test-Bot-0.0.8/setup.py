from setuptools import setup, find_packages

NAME = "HKH-test-Bot"
VERSION = "0.0.8"
AUTHOR = "HKH"
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = "Let's make chatbots !"
LICENSE = ""
KEYWORDS = ("orange3 add-on")
PACKAGES = find_packages()
PACKAGE_DATA = {
    "orangecontrib.hkh_test_bot.widgets": ["icons/*"]
}
INSTALL_REQUIRES = ["faiss-cpu==1.7.4", "sentence-transformers==2.2.2", "gpt4all==2.0.2", "PyMuPDF==1.22.5"]
ENTRY_POINTS = {"orange.widgets":
                    (
                        "HKH-test-Bot = orangecontrib.hkh_test_bot.widgets",
                     )
                }


NAMESPACE_PACKAGES = ["orangecontrib"]

setup(name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
    namespace_packages=NAMESPACE_PACKAGES,
)