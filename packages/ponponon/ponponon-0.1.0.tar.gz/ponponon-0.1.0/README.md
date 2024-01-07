# ponponon

<p align="center">
    <!-- <a href="https://github.com/ponponon/ponponon/actions/workflows/tests.yml" target="_blank">
        <img src="https://github.com/ponponon/ponponon/actions/workflows/tests.yml/badge.svg" alt="Tests coverage"/>
    </a>
    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/lancetnik/ponponon" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/lancetnik/ponponon.svg" alt="Coverage">
    </a> -->
    <a href="https://pypi.org/project/ponponon" target="_blank">
        <img src="https://img.shields.io/pypi/v/ponponon?label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pepy.tech/project/ponponon" target="_blank">
        <img src="https://static.pepy.tech/personalized-badge/ponponon?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="downloads"/>
    </a>
    <br/>
    <a href="https://pypi.org/project/ponponon" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/ponponon.svg" alt="Supported Python versions">
    </a>
    <a href="https://github.com/ponponon/pon/blob/master/LICENSE" target="_blank">
        <img alt="GitHub" src="https://img.shields.io/github/license/ponponon/pon?color=%23007ec6">
    </a>
</p>

## Introduce

ponponon(pon) an advanced message queue framework, derived from [nameko](https://github.com/nameko/nameko)

⭐️ 🌟 ✨ ⚡️ ☄️ 💥

## Installation

Package is uploaded on PyPI.

You can install it with pip:

```shell
pip install ponponon
```

## Requirements

Python -- one of the following:

- CPython : 3.8 and newer ✅
- PyPy : Software compatibility not yet tested ❓

## Features

- Support for concurrent processes: eventlet, gevent
- Support amqp protocol
- Support for http protocol
- Support for grpc protocol
- Support typing hints, like Fastapi

### Create it

```python
from typing import Optional
from loguru import logger
from pon.events.entrance import event_handler


class DNACreateService:
    name = 'dna_create_service'

    @event_handler(source_service='ye', event_name='take')
    def auth(self, src_dna: str, content_type: Optional[str] = None) -> None:
        logger.debug(f'src_dna: {src_dna}')

    @event_handler(source_service='ye', event_name='to_decode')
    def decode(self, src_dna: str) -> None:
        logger.debug(f'src_dna: {src_dna}')


class SampleSearchService:
    name = 'sample_search_service'

    @event_handler(source_service='ye', event_name='take')
    def search(self, url: str) -> None:
        logger.debug(f'url: {url}')
```

### Run it

```shell
pon run --config config.yaml services
```

### Check it

## Resources

![](https://www.rabbitmq.com/img/logo-rabbitmq.svg)

## License

pon is released under the MIT License. See LICENSE for more information.
