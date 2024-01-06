from bravado.client import SwaggerClient


def test_load_sdk():
    import gosdk  # pylint: disable=import-outside-toplevel

    sdk = gosdk.load_sdk(config={})
    assert sdk is not None
    assert isinstance(sdk, SwaggerClient)
