from pydantic import BaseModel, Field
from pon.constants import DEFAULT_MAX_WORKERS
from pon.constants import DEFAULT_PROJECT_NAME
from pon.constants import DEFAULT_FRAMEWORK, DEFAULT_FRAMEWORK_GITHUB
from pon.constants import RABBIT_HOST, RABBIT_PORT, RABBIT_USER, RABBIT_PASSWORD, RABBIT_VHOST

max_workers_description = """
Used to set the maximum number of worker threads for a service. 
Each service can run in a separate thread, 
and the max workers parameter is used to control the number 
of threads that each service can execute concurrently
"""


class PonConfig(BaseModel):
    framework: str = Field(DEFAULT_FRAMEWORK)
    framework_github: str = Field(DEFAULT_FRAMEWORK_GITHUB)
    project_name: str = Field(DEFAULT_PROJECT_NAME)
    max_workers: int = Field(
        DEFAULT_MAX_WORKERS, description=max_workers_description)
    rabbitmq_host: str = Field(RABBIT_HOST)
    rabbitmq_port: int = Field(RABBIT_PORT)
    rabbitmq_user: str = Field(RABBIT_USER)
    rabbitmq_password: str = Field(RABBIT_PASSWORD)
    rabbitmq_vhost: str = Field(RABBIT_VHOST)
    amqp_uri: str = Field(
        f'{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/{RABBIT_VHOST}')
