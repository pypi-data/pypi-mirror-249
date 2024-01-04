from setuptools import find_packages, setup

INSTALL_REQUIRES = (
    "python-dateutil",
    "daft_scraper",
    "thefuzz",
    "backoff",
    "gspread",
    "email_validator",
    "cachetools"
)

setup(
    name="irish-property",
    description="Irish property buy / rent helper",
    long_description="Irish property buy / rent helper",
    version="0.0.2",
    python_requires=">=3.5",
    author="Robert Lucey",
    url="https://github.com/RobertLucey/irish_property",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "irish_property_find = irish_property.bin.find:main",
            "irish_property_run_ntfy = irish_property.bin.run_notify:main",
            "irish_property_remove_persistence = irish_property.bin.remove_persistence:main",
            "irish_property_finder_add_config = irish_property.bin.configure:main",
        ]
    },
)
