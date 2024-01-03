# 🙌 Handsdown - Python documentation generator


[![PyPI - Handsdown](https://img.shields.io/pypi/v/handsdown.svg?color=blue&label=awscliv2e)](https://pypi.org/project/handsdown)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/handsdown.svg?color=blue)](https://pypi.org/project/handsdown)
[![PyPI - Downloads](https://static.pepy.tech/badge/handsdown)](https://pepy.tech/project/handsdown)
[![Code Coverage](https://img.shields.io/codecov/c/gh/vemel/handsdown.svg)](https://codecov.io/gh/vemel/handsdown/tree/main/handsdown)
[![Docs](https://img.shields.io/readthedocs/handsdown.svg?color=blue)](https://handsdown.readthedocs.io/)

Python docstring-based documentation generator for lazy perfectionists.

- [🙌 Handsdown - Python documentation generator](#-handsdown---python-documentation-generator)
  - [Features](#features)
  - [Do you need handsdown?](#do-you-need-handsdown)
  - [Examples](#examples)
  - [Usage](#usage)
    - [💻 From command line](#-from-command-line)
    - [🚀 Use a new Material design](#-use-a-new-material-design)
    - [📦 As a Docker image](#-as-a-docker-image)
    - [📝 As a GitHub Pages manager](#-as-a-github-pages-manager)
    - [🐏 Deploy on Read the Docs](#-deploy-on-read-the-docs)
    - [📋 Build static HTML](#-build-static-html)
    - [🧩 As a module](#-as-a-module)
    - [⌨️ CLI arguments](#️-cli-arguments)
  - [Installation](#installation)
  - [Development](#development)
  - [Changelog](#changelog)

## Features

- [Material design](#-use-a-new-material-design) support!
- [PEP 257](https://www.python.org/dev/peps/pep-0257/),
  [Google](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings),
  [Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
  and [reStructuredText](https://www.python.org/dev/peps/pep-0287/)
  docstrings support. All of them are converted to a valid Markdown.
- Works with [Django](https://www.djangoproject.com/) and [Flask](https://palletsprojects.com/p/flask/) apps
- Can be used locally, or
  [right on GitHub](https://github.com/vemel/handsdown/blob/docs/docsmd/README.md) or even deployed on
  [GitHub Pages](https://vemel.github.io/handsdown/) and [Read the Docs](https://handsdown.readthedocs.io/)!
- Signatures for every class, function, property and method.
- Support for type annotations. Even for the ones from the `__future__`!
- Nice list of all modules in [Index](https://github.com/vemel/handsdown/blob/docs/docsmd/README.md)
- Gather all scattered `README.md` in submodules to one place
- Find related source code from every doc section.
- Make links by just adding `module.import.String` to docs.
- Do you use type annotations? Well, you get auto-discovery of related modules for free!

## Do you need handsdown?

You definitely *do* if you:

- prefer to automate documentation builds
- work with a team and plan to simplify knowledge sharing
- want to show your project without navigating through a source code
- build `Django` or `Flask` applications
- are proud of your project and not afraid to show it
- love Open Source

And probably *do not* if you:

- not very into docstrings and type annotations
- like to abstract a documentation away from the way things really are
- use [Pandas docstrings](https://pandas.pydata.org/pandas-docs/stable/development/contributing_docstring.html)
  as they are not supported yet

## Examples

- [All documentation](https://vemel.github.io/handsdown/) in this project
- [Main](https://github.com/vemel/handsdown/blob/main/examples/main_example.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/main_example.md)
- [RST docstrings](https://github.com/vemel/handsdown/blob/main/examples/rst_docstrings.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/rst_docstrings.md)
- [Google docstrings](https://github.com/vemel/handsdown/blob/main/examples/google_docstrings.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/google_docstrings.md)
- [PEP 257 docstrings](https://github.com/vemel/handsdown/blob/main/examples/pep257_docstrings.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/pep257_docstrings.md)
- [Sphinx docstrings](https://github.com/vemel/handsdown/blob/main/examples/sphinx_docstrings.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/sphinx_docstrings.md)
- [Type annotations](https://github.com/vemel/handsdown/blob/main/examples/typed.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/typed.md)
- [Comment-style type annotations](https://github.com/vemel/handsdown/blob/main/examples/comment_typed.py) with [generated output](https://github.com/vemel/handsdown/tree/docs/docsmd/examples/comment_typed.md)

## Usage

### 💻 From command line

Just go to your favorite project that has lots of docstrings but missing
auto-generated docs and let `handsdown` do the thing.

```bash
cd ~/my/project

# build documentation *.md* files in docs/* directory
handsdown

# or provide custom output directory: output_dir/*
handsdown -o output_dir

# generate docs only for my_module, but exclude migrations
handsdown my_module --exclude my_module/migrations

# generate documentation for deployment
handsdown --external `git config --get remote.origin.url` -n ProjectName --branch main --create-configs
```

Navigate to `docs/README.md` to check your new documentation!

### 🚀 Use a new Material design

- Add `mkdocs` and `mkdocs-material` to your dev dependencies or just install them

```bash
# generate MarkDown documentation in docsmd folder
handsdown --external `git config --get remote.origin.url` -o docsmd -n <project_name> --theme=material --create-configs

# generate html files to docs folder
python -m mkdocs build
```

### 📦 As a Docker image

- Install [Docker](https://docs.docker.com/install/)
- Pull latest `handsdown` version and tag it

```bash
docker pull ghcr.io/vemel/handsdown/handsdown:latest
docker tag ghcr.io/vemel/handsdown/handsdown:latest handsdown
```

- Generate docs for `ProjectName` in current directory

```bash
# for Python 3 project
docker run -v `pwd`:/app handsdown -n ProjectName

# for Python 2 project
PYTHON_VER=2 docker run -v `pwd`:/app handsdown -n ProjectName

# generate documentation for deployment
docker run -v `pwd`:/app handsdown --external `git config --get remote.origin.url` -n ProjectName --create-configs
```

### 📝 As a GitHub Pages manager

With `--external` CLI flag, `handsdown` generates all required configuration
for [GitHub Pages](https://pages.github.com/), so you just need to setup your
GitHub repository.

```bash
# Generate documentation that points to main branch
# do not use custom output location, as `GitHub Pages`
# works only with `docs` directory
handsdown --external `git config --get remote.origin.url` --create-configs

# or specify GitHub url directly
handsdown --external https://github.com/<user>/<project> --create-configs
```

- Generate documentation with `--external` flag as shown above, do not use `--output`
  flag, only `docs` folder is supported by `GitHub Pages`
- Commit and push all changes a to `main` branch.
- Set your GitHub project `Settings` > `GitHub Pages` > `Source` to `main branch /docs folder`

All set! You can change `docs/_config.yml` to add your own touch.

With `--external` flag links to your source are absolute and point to your GitHub repo. If you
still want to have relative links to source, e.g. for using docs locally,
generate docs to another folder

```bash
# `docs_local` folder will be created in your project root
# you probably want to add it to .gitignore
handsdown -o docs_local
```

### 🐏 Deploy on Read the Docs

With `--external` CLI flag, `handsdown` generates all required configuration
for [Read the Docs](https://readthedocs.org/), so you just need to to add your
GitHub repository to `Read the Docs`.

```bash
# Generate documentation that points to main branch
# do not use custom output location, as `GitHub Pages`
# works only with `docs` directory
handsdown --external `git config --get remote.origin.url` --create-configs

# or specify GitHub url directly
handsdown --external https://github.com/<user>/<project>/ --create-configs
```

- Generate documentation with `--external` flag as shown above, do not use `--output`
  flag, only `docs` folder is supported by `Read the Docs`
- Commit and push all changes a to `main` branch.
- Add your repository on [Read the Docs](https://readthedocs.org/)

All set! You can change `.readthedocs.yml` and `mkdocs.yml` to add your own touch.

### 📋 Build static HTML

```bash
# Generate documentation that points to main branch
# with source links pointing to your repository
# this command also creates `mkdocs.yml`
handsdown --external `git config --get remote.origin.url` --create-configs

# Run mkdocs to build HTML
python -m mkdocs build
```

### 🧩 As a module

```python
from handsdown.generator import Generator
from handsdown.utils.path_finder import PathFinder

# this is our project root directory
repo_path = Path.cwd()

# this little tool works like `pathlib.Path.glob` with some extra magic
# but in this case `repo_path.glob("**/*.py")` would do as well
path_finder = PathFinder(repo_path, "**/*.py")

# no docs for tests and build
path_finder.exclude("tests/*", "build/*")

# initialize generator
handsdown = Generator(
    input_path=repo_path,
    output_path=repo_path / 'output',
    source_paths=path_finder.glob("**/*.py")
)

# generate all docs at once
handsdown.generate_docs()

# or generate just for one doc
handsdown.generate_doc(repo_path / 'my_module' / 'source.py')

# generate index.md file
handsdown.generate_index()

# and generate GitHub Pages and Read the Docs config files
handsdown.generate_configs()

# navigate to `output` dir and check results
```

### ⌨️ CLI arguments

```bash
handsdown [-h] [--exclude [EXCLUDE ...]] [-i INPUT_PATH] [-f [FILES ...]]
  [-o OUTPUT_PATH] [--external REPO_URL] [--source-code-path REPO_PATH]
  [--branch BRANCH] [--toc-depth TOC_DEPTH] [--cleanup] [-n PROJECT_NAME]
  [-e ENCODING] [--panic] [-d] [-q] [-V]
  [include ...]
```

| Argument | Description | Default |
|-|-|-|
| `include` | Path expressions to include source files | |
| `--exclude` | Path expressions to exclude source files | |
| `-i` / `--input-path` | Path to project root folder | |
| `-f` / `--files` | List of source files to use for generation. If empty - all are used. | |
| `-o` / `--output-path` | Path to output folder | `<cwd>/docs` |
| `--external` | Build docs and config for external hosting, GitHub Pages or Read the Docs. Provide the project GitHub .../blob/main/ URL here. | |
| `--source-code-path` | Path to source code in the project. Overrides `--branch` CLI argument | |
| `--branch` | Main branch name | `main` |
| `--toc-depth` | Maximum depth of child modules ToC | `3` |
| `--cleanup` | Remove orphaned auto-generated docs | |
| `-n` / `--name` | Project name | `<cwd>` |
| `-e` / `--encoding` | Input and output file encoding | `utf-8` |
| `--panic` | Panic and die on import error | |
| `--debug` | Show debug messages| |
| `--quiet` | Hide log output | |
| `--create-configs` | Create config files for deployment to RtD and GitHub Pages | |
| `-t` / `--theme` | Output mkdocs theme | `readthedocs` |
| `-h` | Show help | |


## Installation

Install using `pip` from PyPI

```bash
pip install handsdown
```

or directly from GitHub if you cannot wait to test new features

```bash
pip install git+https://github.com/vemel/handsdown.git
```

## Development

- Install [poetry](https://python-poetry.org/)
- Run `poetry install`
- Use `black` formatter in your IDE

## Changelog

Changelog can be found in [Releases](https://github.com/vemel/handsdown/releases)
