# -*- encoding: utf-8 -*-
from zerocs.common import BaseSetattr


class Interface(BaseSetattr):

    @staticmethod
    def run_service(configs: dict, services: list) -> None:
        """
        Run Service
        """

    @staticmethod
    def init_mongodb(config: str) -> None:
        """
        init mongodb
        """

    @staticmethod
    def init_config(configs: dict) -> None:
        """
        Init Config Boj
        """

    @staticmethod
    def init_proxy(configs: dict) -> None:
        """
        Init proxy Boj
        """

    @staticmethod
    def get_python_path() -> str:
        """
        get python bin path
        """

    @staticmethod
    def restart_service(service_name: str) -> None:
        """
        Restart the node service. If the service is running on multiple nodes,
        only the current node will be restarted
        """

    @staticmethod
    def main_logger(message: str) -> None:
        """
        logger
        """

    @staticmethod
    def init_rabbitmq(config: str) -> None:
        """
        init rabbitmq
        """

    @staticmethod
    def get_time_str(fmt: str, timezone: str) -> str:
        """
        get time
        """

    @staticmethod
    def remote_call_by_name_and_ip(service_name: str, service_ip: str) -> object:
        """
        remote call rpc Interface
        """

    @staticmethod
    def add_service_object(cls: object) -> None:
        """
        add service
        """

    @staticmethod
    def get_service_object() -> list:
        """
        get services
        """

    @staticmethod
    def set_config(key: str, value: str) -> None:
        """
        Set Config
        """

    @staticmethod
    def set_configs(configs: dict) -> None:
        """
        Set Configs
        """

    @staticmethod
    def get_configs() -> dict:
        """
        Get Configs
        """

    @staticmethod
    def send_message(queue: str, message: dict) -> None:
        """
        Send Queue Message
        """

    @staticmethod
    def get_service_list(query: dict, field: dict, limit: int, skip_no: int) -> tuple[int, dict]:
        """
        get service list
        """

    @staticmethod
    def get_service_by_id(service_id: str) -> dict:
        """
        Get Service BY ServiceID
        """

    @staticmethod
    def get_service_by_name_and_ip(service_name: str, service_ip: str) -> dict:
        """
        Get Service BY ServiceID And ServiceIP
        """

    @staticmethod
    def get_service_by_name(service_name: str) -> list:
        """
        Get Service BY service name
        """

    @staticmethod
    def update_service_by_service_id(service_id: str, data: dict) -> None:
        """
        Update service
        """

    @staticmethod
    def update_run_task(service_name: str, service_ip: str, task_id: str) -> None:
        """
        update running task list
        """

    @staticmethod
    def delete_run_task(service_name: str, service_ip: str, task_id: str) -> None:
        """
        Remove from running task list
        """

    @staticmethod
    def update_max_work_by_name_and_ip(service_name: str, service_ip: str, max_work: int) -> None:
        """
        Update service max work
        """

    @staticmethod
    def update_service_by_name_and_ip(service_name: str, service_ip: str, data: dict) -> None:
        """
        Update service
        """

    @staticmethod
    def insert_service(service_name: str, service_id: str, service_ip: str, max_work: int, run_work: list,
                       update_time: str, api_list: list, service_pid: int) -> None:
        """
        insert service
        """

    @staticmethod
    def get_stop_tasks_by_task_id(task_id: str) -> list:
        """
        get stop task list
        """

    @staticmethod
    def insert_stop_tasks(task_id: str) -> None:
        """
        stop task
        """

    @staticmethod
    def delete_stop_tasks(task_id: str) -> None:
        """
        del stop task
        """
