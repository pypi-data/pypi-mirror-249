import asyncio
import configparser
import json
import os
from importlib.resources import files
from pathlib import Path
import logging

import backoff
import requests.adapters
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from bravado.exception import HTTPServerError

# these are really noisy at debug
logging.getLogger('swagger_spec_validator.ref_validators').setLevel(logging.INFO)
logging.getLogger('bravado_core.model').setLevel(logging.INFO)

_logger = logging.getLogger(__name__)

TIMEOUT = 300
HEADERS = {}

DEFAULT_CONFIG = {
    "validate_responses": False,
    "validate_requests": False,
    "validate_swagger_spec": False
}


def load_sdk(config=None):  # pylint: disable=redefined-outer-name
    spec_file = files('gosdk') / 'spec.json'
    spec = json.loads(spec_file.read_text())
    http_client = RequestsClient()
    config = config or DEFAULT_CONFIG

    return SwaggerClient.from_spec(spec, http_client=http_client, config=config)


def setup_sdk(**kwargs):
    '''Defer SDK setup until after logging has been initialized'''

    config_parser = configparser.ConfigParser()
    if config_files := config_parser.read(Path("~/.gocli.ini").expanduser()):
        _logger.debug('loaded configuration files %s', config_files)
        config = config_parser["gocli-options"]
    else:
        _logger.debug('no configuration files found')
        config = {}

    host = (
        kwargs.get('host')
        or os.getenv("KMS_HOST")
        or config.get("host")
        or kwargs.get('fallback_host')
    )
    if host:
        sdk.swagger_spec.spec_dict['host'] = host
    else:
        _logger.critical('missing required configuration value: host')
        exit(1)

    if value := (
        kwargs.get('schemes')
        or os.getenv("KMS_SCHEMES")
        or config.get("schemes")
    ):
        schemes = value.split(",")
        sdk.swagger_spec.spec_dict['schemes'] = schemes
        for scheme in schemes:
            adapter = requests.adapters.HTTPAdapter(pool_maxsize=25)
            sdk.swagger_spec.http_client.session.mount(f'{scheme}://', adapter)

    token = (
        kwargs.get('token')
        or os.getenv("KMS_TOKEN")
        or config.get("token")
    )
    if host and token:
        sdk.swagger_spec.http_client.set_api_key(
            host, f'Token {token}',
            param_name='Authorization', param_in='header'
        )

    global TIMEOUT  # pylint: disable=global-statement
    if value := (
        kwargs.get('timeout')
        or os.getenv("KMS_TIMEOUT")
        or config.get("timeout")
    ):
        TIMEOUT = int(value)
    else:
        TIMEOUT = 300

    global HEADERS  # pylint: disable=global-statement
    if value := (
        kwargs.get('headers')
        or os.getenv("KMS_CUSTOM_HEADER_OPTION")
        or config.get("custom_header_option")
    ):
        HEADERS = dict([v.split(":", 1) for v in value.split(" ")])
    else:
        HEADERS = {}

    if value := (
        kwargs.get('ssl_verify')
        or os.getenv("KMS_SSL_VERIFY")
        or config.get("ssl_verify")
    ):
        if value.lower() == 'false':
            sdk.swagger_spec.http_client.ssl_verify = False

    sdk.swagger_spec.build()


sdk = load_sdk()


@backoff.on_exception(
    backoff.expo,
    (HTTPServerError, ConnectionError, TimeoutError),
    max_time=600,
    max_tries=12,
)
def call_with_retry(f, **kwargs):
    return f(
        **kwargs,
        _request_options={"headers": HEADERS}
    ).response(timeout=TIMEOUT).result


@backoff.on_exception(
    backoff.expo,
    (HTTPServerError, ConnectionError, TimeoutError),
    max_time=600,
    max_tries=12,
)
async def async_call_with_retry(f, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: f(
            **kwargs,
            _request_options={"headers": HEADERS}
        ).response(timeout=TIMEOUT).result
    )
