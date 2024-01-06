import logging
import shelve
from enum import StrEnum
import dbm.dumb

import bravado_core.model
import mock
from bravado.testing.response_mocks import BravadoResponseMock

_logger = logging.getLogger(__name__)


class CacheMode(StrEnum):
    c = 'record'
    r = 'replay'


class MockSwaggerClient(object):
    def __init__(self, client, cache_file, cache_flag='r'):
        if cache_flag in ['c', 'n']:
            with dbm.dumb.open(cache_file, cache_flag):
                pass

        self.client = client
        self.cache = shelve.open(cache_file, cache_flag)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __getattr__(self, name):
        return MockResource(self.client, self.cache, name)

    def sync(self):
        self.cache.sync()

    def close(self):
        self.cache.close()

    def get_model(self, model_name):
        return self.client.get_model(model_name)


class MockResource(object):
    def __init__(self, client, cache, resource_name):
        self.client = client
        self.cache = cache
        self.resource_name = resource_name

    def __getattr__(self, name):
        return MockOperation(self.client, self.cache, self.resource_name, name)


class MockOperation(object):
    def __init__(self, client, cache, resource_name, operation_name):
        self.client = client
        self.cache = cache
        self.resource_name = resource_name
        self.operation_name = operation_name

    def __call__(self, **kwargs):
        key = f'{self.resource_name}.{self.operation_name}({str(kwargs)})'

        if key not in self.cache:
            resource = getattr(self.client, self.resource_name)
            operation = getattr(resource, self.operation_name)
            result = operation(**kwargs).response().result
            if isinstance(result, bravado_core.model.Model):
                self.cache[key] = (result.__class__.__name__, result._as_dict())
            else:
                self.cache[key] = ('', result)
        else:
            model_name, model_dict = self.cache[key]
            if model_name:
                result = self.client.get_model(model_name)(**model_dict)
            else:
                result = model_dict

        return_value = mock.Mock()
        return_value.response = BravadoResponseMock(result=result)
        return return_value
