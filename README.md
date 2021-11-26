# kitt4sme.roughnator
Estimates surface roughness of manufacturing parts.


### Hacking

Install [Pipenv][pipenv] and Docker. Then clone this repo and `cd`
into the repo root dir

```bash
$ git clone https://github.com/c0c0n3/kitt4sme.roughnator.git
$ cd kitt4sme.roughnator
```

Then use Pipenv to create a Python virtual environment with all
the source and test deps

```bash
$ pipenv install --dev
```

Finally drop into a virtual env shell and hack away

```bash
$ pipenv shell
$ charm .
# ^ Pycharm or whatever floats your boat
```

Run all tests:

```bash
$ PYTHONPATH=".:.roughnator/" pytest tests
```

Build and run the Docker image:

```bash
$ docker build -t kitt4sme/roughnator .
$ docker run -p 8000:8000 kitt4sme/roughnator
```




[pipenv]: https://pipenv.pypa.io/en/latest/