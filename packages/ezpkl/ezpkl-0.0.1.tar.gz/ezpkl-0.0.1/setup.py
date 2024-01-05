from setuptools import setup, find_packages

setup(
    name="ezpkl",
    version="0.0.1",
    description="lovely package to use pickle file system for context manager hater",
    author="bailando",
    author_email="bailando.ys@gmail.com",
    url="https://github.com/yesinkim/ezpkl.git",
    packages=find_packages(exclude = []),
    keywords=["pickle", "file", "easy", "easypickle"],
    python_requires=">=3",
    
)
