[![Version](https://img.shields.io/pypi/v/openpredict)](https://pypi.org/project/openpredict) [![Run tests](https://github.com/MaastrichtU-IDS/translator-openpredict/workflows/Run%20tests/badge.svg)](https://github.com/MaastrichtU-IDS/translator-openpredict/actions?query=workflow%3A%22Run+tests%22) [![Publish package](https://github.com/MaastrichtU-IDS/translator-openpredict/workflows/Publish%20package/badge.svg)](https://github.com/MaastrichtU-IDS/translator-openpredict/actions?query=workflow%3A%22Publish+package%22)

**Translator OpenPredict** 🔮🐍 is an API to compute and serve predicted biomedical concepts associations using the [PREDICT method](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3159979/), for the [NCATS Translator project](https://ncats.nih.gov/translator/about). 

This service has been built from the [fair-workflows/openpredict](https://github.com/fair-workflows/openpredict) project.

# Install the package 📦

You might want to use a `virtualenv` if you are used to it, but this should not be necessary.

### From PyPI

Install the latest release published on [PyPI](https://pypi.org/project/openpredict) 🏷️

```bash
pip install openpredict
```

> PyPI link : [https://pypi.org/project/openpredict](https://pypi.org/project/openpredict)

### From GitHub

You can also install from the latest version of the source code on GitHub:

```bash
pip install git+https://github.com/MaastrichtU-IDS/translator-openpredict
```

---

# Run the API 🌐

After installing the `openpredict` package (except for docker).

### Run from Python script

```python
from openpredict import openpredict_api

port = 8808
debug = False
openpredict_api.start_api(port, debug)
```

> Access the Swagger UI at [http://localhost:8808](http://localhost:8808)

> Run by default in production, set `debug = True` to run in development mode. 

### Run from the command line

Run in production with [Tornado Web Server 🌪️](https://www.tornadoweb.org/en/stable/)

```bash
openpredict start-api
```

> Access the Swagger UI at [http://localhost:8808](http://localhost:8808)

Provide the port as arguments:

```bash
openpredict start-api --port 8808
```

Run in development with [Flask 🧪](https://flask.palletsprojects.com/en/1.1.x/). The API will reload automatically at each change 🔃

```bash
openpredict start-api --debug
```

Show help:

```bash
openpredict --help
```

### Run with Docker

Running using Docker can be convenient of you just want to run the API without installing the package, or to run in production, alongside other services.

Clone the [repository](https://github.com/MaastrichtU-IDS/translator-openpredict):

```bash
git clone https://github.com/MaastrichtU-IDS/translator-openpredict.git
cd translator-openpredict
```

Start the `openpredict-api` container with [docker-compose 🐳](https://docs.docker.com/compose/)

```bash
docker-compose up
```

> Access the Swagger UI at [http://localhost:8808](http://localhost:8808)

> We use [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) and [docker-letsencrypt-nginx-proxy-companion](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion) as reverse proxy for HTTP and HTTPS in production. You can change the proxy URL and port via environment variables `VIRTUAL_HOST`, `VIRTUAL_PORT` and `LETSENCRYPT_HOST` in the [docker-compose.yml](https://github.com/MaastrichtU-IDS/translator-openpredict/blob/master/docker-compose.yml) file.

Stop the container:

```bash
docker-compose down
```

---

# Compute the model 🤖

Run the pipeline to compute the model used by the OpenPredict API.

### From a Python script

```python
from openpredict.compute_similarities import get_drug_disease_classifier

get_drug_disease_classifier()
```

### From the command line

```bash
openpredict compute-similarities
```

---

# See also 👀

* **[Documentation to run in development 📝](docs/dev)**
* **[Documentation generated from the source code 📖](docs)**
* **[Code of Conduct 🤼](https://github.com/MaastrichtU-IDS/translator-openpredict/blob/master/CODE_OF_CONDUCT.md)**