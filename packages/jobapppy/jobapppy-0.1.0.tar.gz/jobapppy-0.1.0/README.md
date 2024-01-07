# jobapppy

[![PyPI version](https://badge.fury.io/py/jobapppy.svg)](https://badge.fury.io/py/jobapppy)[![Python Versions](https://img.shields.io/pypi/pyversions/jobapppy?style=plastic)](https://pypi.org/project/jobapppy)
[![Main](https://github.com/cahna/jobapppy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/jobapppy/actions/workflows/main.yaml)[![codecov](https://codecov.io/gh/cahna/jobapppy/graph/badge.svg?token=3XULKTDJ2I)](https://codecov.io/gh/cahna/jobapppy)

Command-line tools and interfaces to generate formatted resume documents (markdown, tex, pdf, etc).

Documentation: [https://cahna.github.io/jobapppy](https://cahna.github.io/jobapppy)

## CLI Usage

- via script name installed in path:
   ```console
   jobapppy --help
   ```
- as a python module:
   ```console
   python -m jobapppy --help
   ```

## Tutorial

1. Create a `resume.yaml` file that satisfies jobapppy's schema 
   - see `resume.example.yaml`
   - view the JSONSchema by running:
      ```console
      jobapppy schema -i2
      ```
2. (optional) Check that `resume.yaml` can be parsed:
   ```console
   jobapppy parse -c resume.yaml
   ```
3. Generate resume from templates:
   - Markdown (default, `-t md`)
      - Echo to stdout (default):
         ```console
         jobapppy template resume.yaml
         ```
      - Echo to file:
         ```console
         jobapppy template resume.yaml resume.md
         ```
   - Tex (`-t tex`)
      1. Generate `resume.tex`:
         ```console
         jobapppy template -t tex resume.yaml resume.tex
         ```
      2. Generate `resume.pdf`:
         ```console
         docker run --rm -it -v "$(pwd):/data" --net=none --user="$(id -u):$(id -g)" cahna/jobapp lualatex -synctex=1 -interaction=nonstopmode resume.tex
         ```
