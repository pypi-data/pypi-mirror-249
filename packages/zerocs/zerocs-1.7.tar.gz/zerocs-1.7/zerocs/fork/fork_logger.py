import json

from argparse import ArgumentParser
from zerocs.rabbit import RabbitMq
from zerocs.logger import Logger


def mq_callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    task_data = json.loads(body.decode())
    Logger.logs_path = args.LOGS_PATH

    level = task_data['level']
    message = task_data['message']
    service_name = task_data['service_name']

    if level == 'info':
        Logger.logger(service_name).info(f"{message}")

    if level == 'error':
        Logger.logger(service_name).error(f"{message}")

    if level == 'warning':
        Logger.logger(service_name).warning(f"{message}")


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--RABBITMQ_CONFIG', '-RABBITMQ_CONFIG', help='RABBITMQ_CONFIG')
    parser.add_argument('--LOGS_PATH', '-LOGS_PATH', help='LOGS_PATH')
    parser.add_argument('--SERVICE_IP', '-SERVICE_IP', help='SERVICE_IP')

    args = parser.parse_args()
    RabbitMq.rabbitmq_init(args.RABBITMQ_CONFIG)

    queue_name = f"AsynchronousLog_{args.SERVICE_IP}"
    RabbitMq.get_message(queue_name, mq_callback)
