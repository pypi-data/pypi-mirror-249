import os
import sys
import time
from pathlib import Path
from typing import Tuple, Dict, List, Callable, Any, Union, Optional
import yaml
import eventlet
from eventlet.greenthread import GreenThread
from pon.core import get_class_names
from pon.events import EventRunnerContext
from pon.timer.register import PON_TIMER_METHOD_ATTR_NAME


class EventletTimerRunner:
    amqp_uri: str

    def __init__(self) -> None:
        self.put_patch()

    def put_patch(self) -> None:
        import eventlet
        eventlet.monkey_patch()  # noqa (code before rest of imports)

    def load_service_cls_list(self, services: Tuple[str]) -> List[type]:
        BASE_DIR: Path = Path(os.getcwd())
        sys.path.append(str(BASE_DIR))

        service_cls_list: List[type] = []

        for service in services:
            items: List[str] = service.split(':')
            if len(items) == 1:
                module_name, service_class_name = items[0], None
            elif len(items) == 2:
                module_name, service_class_name = items
            else:
                raise Exception(f'错误的 service 格式: {service}')

            __import__(module_name)
            module = sys.modules[module_name]

            if service_class_name:
                service_class_names = [service_class_name]
            else:
                service_class_names = get_class_names(module_name)

            for service_class_name in service_class_names:
                service_cls = getattr(module, service_class_name)
                service_cls_list.append(service_cls)

        return service_cls_list

    def load_config(self, config_filepath: Path):
        with open(config_filepath, 'r', encoding='utf-8') as f:
            config: Dict[str, Dict] = yaml.safe_load(f)
            self.context = EventRunnerContext(config)
        self.amqp_uri = config['AMQP_URI']

    def run(self, services: Tuple[str], config_filepath: Path):
        self.load_config(config_filepath)

        service_cls_list: List[type] = self.load_service_cls_list(services)

        # 1. 去 rabbitmq 创建消息队列
        gts: List[GreenThread] = []
        for service_cls in service_cls_list:
            for item in dir(service_cls):
                cls_property: Callable = getattr(service_cls, item)
                if hasattr(cls_property, PON_TIMER_METHOD_ATTR_NAME):
                    timer_method = cls_property
                    gt = eventlet.spawn(
                        self.run_timer, service_cls, timer_method)
                    gts.append(gt)
        for gt in gts:
            gt.wait()

    def run_timer(self, service_cls: type, timer_method: Callable):
        pon_timer_func_config: Dict[str, Any] = getattr(
            timer_method, PON_TIMER_METHOD_ATTR_NAME)
        # 获取修饰器附加的参数

        interval: Union[int,
                        float] = pon_timer_func_config['interval']
        execute_before_sleep: bool = pon_timer_func_config['execute_before_sleep']
        timeout: Optional[float] = pon_timer_func_config['timeout'] or None
        wait: bool = pon_timer_func_config['wait']

        service_instance = service_cls()

        if execute_before_sleep:
            try:
                with eventlet.Timeout(timeout):
                    if wait:
                        timer_method(service_instance)
                    else:
                        eventlet.spawn_n(service_instance)
            except Exception:
                pass

        while True:
            time.sleep(interval)
            try:
                with eventlet.Timeout(timeout):
                    if wait:
                        timer_method(service_instance)
                    else:
                        eventlet.spawn_n(service_instance)
            except Exception:
                pass
