[![Python 3.12](
https://img.shields.io/badge/python-3.12-blue.svg)](
https://www.python.org/downloads/release/python-31012/)

<p float="left">
    <img style="vertical-align: top" src="./images/ai-in-healthcare.webp" width="40%" />
</p>


<!-- ABOUT THE PROJECT -->

## The CCB MedAI Repository ##

This repository contains the `Ollama` class, derived from the [Ollama](https://pypi.org/project/ollama/) project. Its primary goal is to assist you in getting started with Ollama models on your own hardware. The containerized environment is particularly beneficial if you plan to use the Ollama library with an NVIDIA GPU.

### Local Installation with Docker ###

1. Install [Docker](https://docs.docker.com/) on your machine.

2. Clone the GitHub repository to create a local copy:
   ```bash
   git clone git@github.com:ccb-hms/medai.git
   ```

3. Navigate to the repository's directory and build the Docker images:
   ```bash
   cd medai && docker-compose build
   ```
   This command builds the Ollama image and a specialized development image for using the Ollama Python library, along with any other necessary packages for your data science project (e.g., pandas, numpy, scikit-learn, etc.). The MedAI image includes a Dockerfile that uses the official [Python 3.12](https://hub.docker.com/layers/library/python/3.12.10/images/sha256-2749d801aca0c7d0b0b2106dabe3a8bca138c597b273d18c4e497f61e703603c) Docker image as the base image, along with the dependencies outlined in the project's `pyproject.toml` file. The image is built locally and stored in the Docker image cache directory. To rebuild the image, simply run `docker-compose build` again. To remove the image, use the command `docker-compose down --rmi all`.

4. Run the Docker container:
   ```bash
   docker-compose up
   ```
   This command creates the Ollama and development containers and starts a Jupyter server, which can be accessed through a web browser.

5. Access the Jupyter Lab server from your browser by visiting the link that begins with `localhost:8888`.

### Installation without Docker ###

For installation in a local programming environment, we use [uv](https://github.com/astral-sh/uv) to create a pure, repeatable application environment. Mac and Windows users should install uv as described in the [installation instructions](https://github.com/astral-sh/uv#installation). UV is a fast Python package installer and resolver, written in Rust. It serves as a drop-in replacement for pip and pip-tools, offering significant performance improvements and a more efficient workflow.

UV manages dependencies on a per-project basis. To install this package, navigate to your project directory and run:

```bash
# Install the package. This assumes that Python version 3.12 is set as the current global Python interpreter. 
uv venv --python=3.12.11

# Activate the environment
source .venv/bin/activate 
# On Windows use: .venv\Scripts\activate 
uv pip install -e .

# Next, install the dependencies
uv sync

# Lastly, run the Jupyter Lab server in the new environment
uv run jupyter lab
```

### Installing with Other Python Versions ###

The package has been tested with Python 3.12.11, as specified in the project's configuration. However, it includes compatibility libraries to ensure that it can be used with earlier Python versions. To install this package with a different version of Python, such as Python 3.10, first create a virtual environment with the desired version:

```bash
uv venv --python=3.10 
source .venv/bin/activate 
# On Windows use: .venv\Scripts\activate 
uv pip install -e .
```

It is also possible to install the package using a local Python interpreter that is installed in a specific directory, for example, within a virtual environment created with [Miniconda](https://docs.anaconda.com/miniconda/):

```bash
uv venv --python=/home/.../miniconda3/envs/uv-test/bin/python
source .venv/bin/activate 
# On Windows use: .venv\Scripts\activate 
uv pip install -e .
```
In this case, `uv-test` refers to the directory containing the executable Python interpreter created by Miniconda.