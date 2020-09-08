Documentation to run the **Translator OpenPredict API** in development.

Contributions, feedbacks and pull requests are welcomed from anyone!

# Alternative: install for dev 📥

Install `openpredict` locally, if you want to run **OpenPredict** in development, make changes to the source code, and build new models.

### Clone

```bash
git clone https://github.com/MaastrichtU-IDS/translator-openpredict.git
cd translator-openpredict
```

### Install

This will install `openpredict` and update the package automatically when the files changes locally 🔃

```bash
pip install -e .
```

# Run in dev 🚧

### Start API

Use the CLI to run in development with [Flask 🧪](https://flask.palletsprojects.com/en/1.1.x/). The API will reload automatically at each change 🔃

```bash
openpredict start-api --debug
```

### Run tests

Run the **OpenPredict API** tests locally:

```bash
pytest tests
```

Run a specific test file and display `print`:

```bash
pytest tests/test_openpredict_api.py -s
```

## Generate documentation

Documentation in [docs/ 📖](docs/)  generated from the Python source code docstrings using [pydoc-markdown](https://pydoc-markdown.readthedocs.io/en/latest/).

```bash
pip install pydoc-markdown
```

Generate markdown documentation page for the `openpredict` package in `docs/`

```bash
pydoc-markdown --render-toc -p openpredict > docs/README.md
```

Modify the generated page title:

```bash
find docs/README.md -type f -exec sed -i "s/# Table of Contents/# OpenPredict Package documentation 🔮🐍/g" {} +
```

> This can also be done using Sphinx, see this article on [deploying Sphinx to GitHub Pages](https://circleci.com/blog/deploying-documentation-to-github-pages-with-continuous-integration/)
>
> ```bash
> pip install sphinx
> sphinx-quickstart sphinx-docs/ --project 'openpredict' --author 'Vincent Emonet'
> cd sphinx-docs/
> make html
> ```

---

# See also 👀

* **[Documentation main page 🔮🐍](https://maastrichtu-ids.github.io/translator-openpredict)**
* **[Documentation generated from the source code 📖](https://maastrichtu-ids.github.io/translator-openpredict/docs)**
* **[Code of Conduct 🤼](https://github.com/MaastrichtU-IDS/translator-openpredict/blob/master/CODE_OF_CONDUCT.md)**