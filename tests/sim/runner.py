from fipy.docker import DockerCompose

from tests.util.fiware import wait_on_orion, create_subscriptions
from tests.util.sampler import MachineSampler


docker = DockerCompose(__file__)


def bootstrap():
    docker.build_images()
    docker.start()

    wait_on_orion()

    create_subscriptions()


def send_machine_entities():
    sampler = MachineSampler(pool_size=2)
    try:
        sampler.sample(samples_n=1000, sampling_rate=2.5)
    except Exception as e:
        print(e)


def run():
    services_running = False
    try:
        bootstrap()
        services_running = True

        print('>>> sending machine entities to Orion...')
        while True:
            send_machine_entities()

    except KeyboardInterrupt:
        if services_running:
            docker.stop()
