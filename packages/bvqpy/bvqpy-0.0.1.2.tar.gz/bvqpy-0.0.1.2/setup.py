from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__name__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

VERSION = '0.0.1.2'

# Setting up
setup(
    name="bvqpy",
    version=VERSION,
    author="Gonzalo Garcia-Castro",
    author_email="gongarciacastro@gmail.com",
    description="Barcelona Vocabulary Questonnaire",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gongcastro/bvqpy",
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'pandas',
        'numpy'
    ],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/gongcastro/bvqpy/issues",
        "Source": "https://github.com/gongcastro/bvqpy/",
    },
    keywords=['python', 'vocabulary'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ]
)
