__version__ = "0.4.7"
__release__ = f"{__version__}.20240104"


import os
from loguru import logger
from myframe.util import Tool, ExceptionAuthFailed
from myframe._config import frame_init_project_config
from myframe._container import create_container


__CACHE = dict()
__PROJECT_CONFIG = None
__CONTAINER = None


def INIT(config_filename: str = None) -> None:
    """初始化：读取配置文件（可指定），根据配置文件初始化service，设置全局变量

    当不指定配置文件时，将自动寻找配置文件，规则：1.确定当前的包，按照约定当前包下存在{package-name}-config.json文件，并且当前包在sys.path中，
    2.在非windows系统下优先查看/etc/{package-name}-config.json文件。

    Args:
        config_filename: 配置文件

    """

    if config_filename:
        if not os.path.exists(config_filename) or not config_filename.endswith('-config.json'):
            raise Exception(f"unsupport config filename {config_filename}")

    global __CONTAINER
    global __PROJECT_CONFIG
    if __CACHE.get("auto_init"):
        return

    project_config = frame_init_project_config(config_filename)
    logger.debug(project_config)

    if project_config:
        __PROJECT_CONFIG = project_config
        __CONTAINER = create_container(project_config)
    __CACHE['auto_init'] = True


def get_container():
    """获取dependency_injector的container

    Usage:
        >>> from myframe import get_container
        >>> config = get_container().config()
        >>> service_mysql_db = get_container().service_mysql_db_name()

    """

    if not __CACHE.get("auto_inited", None):
        INIT()
    return __CONTAINER
