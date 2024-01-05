# -*- encoding: utf-8 -*-
from zerocs.config import Config
from zerocs.logger import Logger
from zerocs.rabbit import RabbitMq
from zerocs.database import MongodbAPI
from zerocs.interface import Interface
from zerocs.observer import ObserverBase
from zerocs.utils import Utils, ZeroProxy, GetClusterRpcProxy
from zerocs.services import ServiceRegistration


@Interface
class _Interface:

    @staticmethod
    def run_service(configs: dict, services: list) -> None:
        Interface.set_configs(configs)
        for service in services:
            Interface.add_service_object(service)

        ObserverBase.attach(Config, subject=Logger)
        ObserverBase.attach(Config, subject=MongodbAPI)
        ObserverBase.attach(Config, subject=ServiceRegistration)
        ObserverBase.notify(Config)

    @staticmethod
    def init_config(configs) -> None:
        Interface.set_configs(configs)
        ObserverBase.attach(Config, subject=Logger)
        ObserverBase.attach(Config, subject=RabbitMq)
        ObserverBase.attach(Config, subject=MongodbAPI)
        ObserverBase.notify(Config)

    @staticmethod
    def init_proxy(configs: dict) -> None:
        Interface.set_configs(configs)
        ObserverBase.attach(Config, subject=RabbitMq)
        ObserverBase.attach(Config, subject=MongodbAPI)
        ObserverBase.notify(Config)

    @staticmethod
    def remote_call_by_name_and_ip(service_name: str, service_ip: str) -> object:
        service_id = MongodbAPI.get_service_id_by_name_and_ip(service_name, service_ip)
        _obj = GetClusterRpcProxy.get_cluster_rpc_proxy({"AMQP_URI": Config.get_configs().get('RABBITMQ_CONFIG')})
        ZeroProxy.init_rpc_proxy(_obj, service_id)
        return ZeroProxy

    @staticmethod
    def restart_service(service_name: str) -> None:
        ServiceRegistration.restart_service(service_name)

    @staticmethod
    def main_logger(message: str) -> None:
        Logger.logger('main').error(message)

    @staticmethod
    def init_mongodb(config: str) -> None:
        MongodbAPI.init(config)

    @staticmethod
    def init_rabbitmq(config: str) -> None:
        RabbitMq.rabbitmq_init(config)

    @staticmethod
    def send_message(queue: str, message: dict) -> None:
        RabbitMq.send_message(queue, message)

    @staticmethod
    def get_python_path() -> str:
        return Utils.get_python_path()

    @staticmethod
    def get_time_str(fmt: str, timezone: str) -> str:
        return Utils.get_time_str(fmt, timezone)

    @staticmethod
    def add_service_object(service: object) -> None:
        ServiceRegistration.add_service_object(service)

    @staticmethod
    def get_service_object() -> list:
        return ServiceRegistration.get_service_object()

    @staticmethod
    def set_config(key: str, value: str) -> None:
        Config.set_config(key, value)

    @staticmethod
    def set_configs(configs: dict) -> None:
        Config.set_configs(configs)

    @staticmethod
    def get_configs() -> dict:
        return Config.get_configs()

    @staticmethod
    def get_service_list(query: dict, field: dict, limit: int, skip_no: int) -> tuple[int, dict]:
        return MongodbAPI.get_service_list(query, field, limit, skip_no)

    @staticmethod
    def get_service_by_id(service_id: str) -> dict:
        return MongodbAPI.get_service_by_id(service_id)

    @staticmethod
    def update_max_work_by_name_and_ip(service_name: str, service_ip: str, max_work: int) -> None:
        MongodbAPI.update_max_work_by_name_and_ip(service_name, service_ip, max_work)

    @staticmethod
    def get_service_by_name_and_ip(service_name: str, service_ip: str) -> dict:
        return MongodbAPI.get_service_by_name_and_ip(service_name, service_ip)

    @staticmethod
    def get_service_by_name(service_name: str) -> list:
        return MongodbAPI.get_service_by_name(service_name)

    @staticmethod
    def update_service_by_service_id(service_id: str, data: dict) -> None:
        MongodbAPI.update_service_by_service_id(service_id, data)

    @staticmethod
    def update_run_task(service_name: str, service_ip: str, task_id: str) -> None:
        MongodbAPI.update_run_task(service_name, service_ip, task_id)

    @staticmethod
    def delete_run_task(service_name: str, service_ip: str, task_id: str) -> None:
        MongodbAPI.delete_run_task(service_name, service_ip, task_id)

    @staticmethod
    def update_service_by_name_and_ip(service_name: str, service_ip: str, data: dict) -> None:
        MongodbAPI.update_service_by_name_and_ip(service_name, service_ip, data)

    @staticmethod
    def insert_service(service_name: str, service_id: str, service_ip: str, max_work: int, run_work: int,
                       update_time: str, api_list: list, service_pid: int) -> None:
        MongodbAPI.insert_service(
            service_name, service_id, service_ip, max_work, run_work, update_time, api_list, service_pid)

    @staticmethod
    def get_stop_tasks_by_task_id(task_id: str) -> list:
        return MongodbAPI.get_stop_tasks_by_task_id(task_id)

    @staticmethod
    def insert_stop_tasks(task_id: str) -> None:
        MongodbAPI.insert_stop_tasks(task_id)

    @staticmethod
    def delete_stop_tasks(task_id: str) -> None:
        MongodbAPI.delete_stop_tasks(task_id)
