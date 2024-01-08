from setuptools import setup, find_packages

setup(
    name='stock-indicators-2101410',  # Package name
    version='0.1.0',  # Version number
    packages=find_packages('src'),  # Specify package directories
    package_dir={'': 'src'},  # Specify the root package directory
    install_requires=[
        # List of dependencies required for your package
    ],
)
