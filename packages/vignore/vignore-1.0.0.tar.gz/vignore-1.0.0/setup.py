from setuptools import setup

setup(
    name="vignore",
    version="1.0.0",
    packages=["vignore"],
    install_requires=[
        "numpy",
        "rich",
        "textual",
        "jinja2",
        "beartype",
        "aiofiles",
        "asyncio",
    ],
    entry_points="""
        [console_scripts]
        vignore=vignore.cli:main
    """,
)
