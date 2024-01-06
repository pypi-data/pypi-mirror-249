from setuptools import setup, find_packages

setup(
    name="small-ass-cache",
    version="0.9.1",
    packages=find_packages(),
    include_package_data=True,
    description="An asset loading and caching utility for game assets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wegfawefgawefg/small-ass-cache",
    author="Gibson Martin",
    author_email="668es218pur@gmail.com",
    license="MIT",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
