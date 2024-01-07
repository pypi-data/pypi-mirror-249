from setuptools import setup


classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]


with open("README.md", "r") as fp:
    long_description = fp.read()


setup(name="print_rank_0",
      version="0.1.1",
      author="Tailing Yuan",
      author_email="yuantailing@gmail.com",
      url="https://github.com/yuantailing/print_rank_0",
      tests_require=["pytest", "torch"],
      description="Print on rank 0",
      long_description=long_description,
      license="MIT",
      classifiers=classifiers,
      python_requires=">=3.3",
      )
