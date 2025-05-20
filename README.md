# Homepage

This repository contains the source code of my personal homepage hosted at [https://till-knollmann.com](https://till-knollmann.com).

## CI/CD

On commit to the main branch, a github workflow is activated that:
- Generates localized pages
- Minifies Javascript, CSS and HTML files
- Inlines Javascript and CSS into the HTML
- Pushes an incremental update to the webspace at [https://till-knollmann.com](https://till-knollmann.com)

## Run

Pull the repository in a [VSCode Devcontainer](https://code.visualstudio.com/docs/devcontainers/containers).
The container configures itself and allows to run a local server for testing (`Open with Live Server`).

## Localizations

To generate localizations of the page, run `/generator/generate.py`.
The localization inputs texts from .json files in `/generator/` into the `/generator/template.html` by matching placholders for each language.
