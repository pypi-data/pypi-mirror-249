from setuptools import find_packages, setup

with open("app/network_simulator/Readme.md") as file:
    long_description = file.read()

setup(
    name="network-simulator",
    version="1.0.0",
    description="Simulator that generates synthetic social network data",
    package_dir={"":"app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minsoos/network_simulator",
    author="Min Soo Jeon Acevedo",
    author_email="mjeon@uc.cl",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        # "Operating System :: MacOS",
        "Operating System :: Unix",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Natural Language :: Spanish",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["anytree>=2.8.0", "soil==0.20.7", "scipy>=1.8.0", "numpy>=1.24.3", "pyenchant>=3.2.2"],
    extras_require={
        "openai": ["openai>=1.6.1",],
        "llama2": ["torch>=2.1.2", "transformers>=4.36", "langchain>=0.0.352"]
    },
    python_requires=">=3.7"
)