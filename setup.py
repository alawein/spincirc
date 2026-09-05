"""Build configuration for the SpinCirc Python package."""
from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent


def read_requirements(name: str) -> list[str]:
    return [
        line.strip()
        for line in (ROOT / "requirements" / name).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


setup(
    name="spincirc",
    version="1.0.0",
    author="Meshal Alawein",
    author_email="contact@meshal.ai",
    description="Python analysis tools for SpinCirc simulation results",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/alawein/spincirc",
    project_urls={"Repository": "https://github.com/alawein/spincirc", "Issues": "https://github.com/alawein/spincirc/issues"},
    packages=find_packages(where="python", exclude=("tests", "tests.*")),
    package_dir={"": "python"},
    python_requires=">=3.9",
    install_requires=read_requirements("runtime.txt"),
    extras_require={"test": read_requirements("test.txt"), "docs": read_requirements("docs.txt"), "ml": read_requirements("ml.txt")},
    entry_points={"console_scripts": ["spincirc-process=spincirc.analysis.data_processor:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    license="MIT",
    zip_safe=False,
)
