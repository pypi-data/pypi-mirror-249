# -*- encoding: utf-8 -*-
import eventlet

eventlet.monkey_patch()

from argparse import ArgumentParser
from nameko.containers import ServiceContainer

from zerocs.config import Config
from zerocs.logger import Logger
from zerocs.build import ServiceBuild
from zerocs.observer import ObserverBase


class MultiProcess:

    @staticmethod
    def container_start():
        Config.set_configs(config)
        ObserverBase.attach(Config, subject=Logger)
        ObserverBase.notify(Config)

        module = __import__(args.SERVICE_PATH, globals=globals(), locals=locals(), fromlist=['RpcFunction'])

        func = ServiceBuild.build(func=module.RpcFunction, rabbitmq_config=config.get("RABBITMQ_CONFIG"))
        container = ServiceContainer(service_cls=func, config={"AMQP_URI": config.get('RABBITMQ_CONFIG')})
        container.start()
        container.wait()


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--SERVICE_PATH', '-SERVICE_PATH', help='SERVICE_PATH')
    parser.add_argument('--RABBITMQ_CONFIG', '-RABBITMQ_CONFIG', help='RABBITMQ_CONFIG')
    parser.add_argument('--LOGS_PATH', '-LOGS_PATH', help='LOGS_PATH')

    args = parser.parse_args()
    config = {"RABBITMQ_CONFIG": args.RABBITMQ_CONFIG, "LOGS_PATH": args.LOGS_PATH}

    MultiProcess().container_start()
