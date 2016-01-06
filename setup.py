from setuptools import setup, find_packages

setup(
    name = "Greengraph",
    version = "1.0",
    description = "Greengraph Assignment",
    author = "Irina Grigorescu",
    author_email = "irina.grigorescu.15@ucl.ac.uk",
    url = "https://github.com/irinagrigorescu/homework1",
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/greengraph'],
    install_requires = ['argparse', 'pypng', 'numpy', 'geopy', 'matplotlib', 'requests']
)
