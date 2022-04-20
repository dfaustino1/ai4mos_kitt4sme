KITT4SME Roughnator
-------------------
> Estimates surface roughness of manufacturing parts.


### Hacking

Install Python (`>= 3.8`), Poetry (`>=1.1`) and the usual Docker
stack (Engine `>= 20.10`, Compose `>= 2.1`). If you've got Nix, you
get a dev shell with the right Python and Poetry versions simply by
running

```console
$ nix shell github:c0c0n3/kitt4sme.roughnator?dir=nix
```

Otherwise, install the usual way you do on your platform. Then clone
this repo, `cd` into its root dir and install the Python dependencies

```console
$ git clone https://github.com/c0c0n3/kitt4sme.roughnator.git
$ cd kitt4sme.roughnator
$ poetry install
```

Finally drop into a virtual env shell to hack away

```bash
$ poetry shell
$ charm .
# ^ Pycharm or whatever floats your boat
```

Run all the test suites:

```console
$ pytest tests
```

or just the unit tests

```console
$ pytest tests/unit
```

Measure global test coverage and generate an HTML report

```console
$ coverage run -m pytest -v tests
$ coverage report html
```

Build and run the Docker image:

```bash
$ docker build -t kitt4sme/roughnator .
$ docker run -p 8000:8000 kitt4sme/roughnator
```


### Live simulator

We've whipped together a test bed to simulate a live environment similar
to that of the KITT4SME cluster. In the `tests/sim` directory, you'll find
a Docker compose file with

* Orion LD connected to MongoDB
* Quantum Leap with a CrateDB backend
* Our Roughnator service
* KITT4SME Dazzler configured with a dashboard to display Roughnator's
  estimates

To start the show, run (Ctrl+C to stop)

```console
$ poetry shell
$ python tests/sim
```

This will bring up the Docker compose environment (assuming you've
got a Docker engine running already), subscribe Quantum Leap and
Roughnator to Orion and then will start sending machine entities to
Orion. On receiving those entities, Orion forwards them to Roughnator
and Quantum Leap. For each entity Orion sends on, Roughnator comes
up with a surface roughness estimate that then writes back to Orion.
Since Quantum Leap got subscribed to all entity changes, it'll
collect both machine and estimate entities in their own time series.
And here's what's actually going on under the bonnet:

![Live simulator.][dia.sim]

In fact, if you browse to the CrateDB Web UI at:

- http://localhost:4200.

you should be able to query both the machine and estimate entity
tables to see data coming in from the simulator through Orion and
then Quantum Leap. Now browse to the Roughnator Dazzler dashboard
at:

- http://localhost:8080/dazzler/csic/-/

You should see the dashboard with an explanation of what it is and
how it works. Load the available estimate entity IDs, then select
one to plot the data. The dashboard fetches new data from Quantum
Leap every few seconds, so as the simulator sends entities you should
be able to see the new data points reflected in the plot.

Notice that all those entities belong to a tenant named `csic`. So
you should be able to see Orion and Quantum Leap using a separate
DB/schema for that tenant. Also the tenant's name is part of the
Dazzler dashboard URL and is also shown on the dashboard. (KITT4SME
relies on this arrangement to silo tenant data and enforce security
policies.)




[dia.sim]: ./roughnator-sim.svg
