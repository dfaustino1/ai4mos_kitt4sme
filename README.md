KITT4SME ai4mos
-------------------
> Solves the job shop scheduling problem and estimates total energy consumption of the schedule.


### Hacking

Install Python (`>= 3.8`), Poetry (`>=1.1`) and the usual Docker
stack (Engine `>= 20.10`, Compose `>= 2.1`). 

`cd` into the root dir and install the Python dependencies

```console
$ cd kitt4sme.roughnator
$ poetry install
```

Finally drop into a virtual env shell to hack away

```bash
$ poetry shell
```


### Testing the solution

To start the simulation, run (Ctrl+C to stop)

```console
$ poetry shell
$ python tests/sim
```

Assuming that you have a running Docker engine, executing the command will 
initiate the Docker compose environment, connect Quantum Leap and the genetic 
algorithm to Orion, and begin sending production entities to Orion. When Orion 
receives these entities, it relays them to both the genetic algorithm and 
Quantum Leap. The algorithm is applied to each entity in order to generate a 
schedule and estimate energy consumption, then writing back to Orion. A grafana
instance is also initiated, providing a better view of the results.

Please note that the scheduling solution presented here was adapted from 
an example provided by the consortium, Roughnator. Therefore, some elements 
may still refer to Roughnator by name, even though they pertain to the 
scheduling solution itself.


If you browse to the CrateDB Web UI at:

- http://localhost:4200.

you should be able to query both the productions and schedule entity
tables to see data coming in from the simulator through Orion and
then Quantum Leap. 

Also, by connecting the grafana to the CrateDB, it is
possible to see the flow of messages that passing through the 
context broker, access the grafana Web UI at:

- http://localhost:3000.
