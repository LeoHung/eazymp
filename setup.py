from setuptools import setup, find_packages

setup(
    name = "eazymp",
    version = "0.1.0.0.3",
    #packages = find_packages(),
    packages =['eazymp'],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        "pyre>=0.8.2.0-pathos",
        "processing>=0.52-pathos",
        "ppft>=1.6.4.5",
        "dill>=0.2.2",
        "Pillow>=2.8.1",
        "pathos>=0.2a1.dev0",
        "ppft>=1.6.4.5",
        "dill>=0.2.2",
        "pyre>=0.8.2.0-pathos",
        "processing>=0.52-pathos"
    ],

    dependency_links = [
        "https://github.com/uqfoundation/pathos/raw/master/external/pyre-0.8.2.0-pathos.zip",
        "https://github.com/uqfoundation/pathos/raw/master/external/processing-0.52-pathos.zip",
        "git+https://github.com/uqfoundation/pathos#egg=pathos-0.2a1.dev0"
    ],

    entry_points = {
        'console_scripts': [
            'eazymp = eazymp.main:run',
        ],
    },

    # metadata for upload to PyPI
    author = "San-Chuan Hung, Jiajun Wang",
    author_email = "sanchuah@andrew.cmu.edu",
    description = "Easily and lazily make your Python code in parallel",
    license = "MIT",
    keywords = "easy lazy openmp parallel",
    url = "http://leohung.net/pymp",   # project home page, if any
    # could also include long_description, download_url, classifiers, etc.
)
