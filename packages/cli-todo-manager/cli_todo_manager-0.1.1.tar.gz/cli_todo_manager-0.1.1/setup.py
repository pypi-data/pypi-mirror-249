from setuptools import setup

with open("requirements.txt", "r") as r:
    install_requires = r.readlines()

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="cli_todo_manager",
    version="0.1.1",
    description="A simple command line utility that manages your ToDos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Nwungang",
    author_email="timnw.dev@gmail.com",
    url="https://github.com/timnw2000/todos",
    requires=["setuptools"],
    install_requires=install_requires,
    license="MIT",
    maintainer_email="timnw.dev@gmail.com",
    project_urls={
        "Documentation": "https://github.com/timnw2000/todos/blob/main/README.md",
    },
    entry_points={
        "console_scripts": [
            "todo=main:todo",
        ]
    }
)