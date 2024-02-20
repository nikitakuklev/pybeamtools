import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

INSTALL_REQUIRES = [
    'numpy>=1.13.3',
    # 'pandas>=1.0'
]
EXTRAS_REQUIRES = {
    "develop": [
        "pytest>=6.0",
    ]
}
LICENSE = 'MIT'
DESCRIPTION = 'Various tools for accelerator physics'
CLASSIFIERS = [
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering",
    "Intended Audience :: Science/Research",
]

setuptools.setup(
        name="pybeamtools",
        author="Nikita Kuklev",
        version="0.2.3",
        packages=setuptools.find_packages(where='.', include=['pybeamtools*']),
        include_package_data=True,
        package_data={
            "pybeamtools": ["*.sdds", "*.txt", "*.json", "*.ui", "*.yaml", "*.yml", "*.workspace",
                            "*.py"],
        },
        description=DESCRIPTION,
        license=LICENSE,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        classifiers=CLASSIFIERS,
        platforms="any",
        install_requires=INSTALL_REQUIRES,
        python_requires=">=3.9",
        extras_require=EXTRAS_REQUIRES
)
