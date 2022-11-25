from http import HTTPStatus
from unittest.mock import Mock, mock_open, patch
from urllib.error import HTTPError

import pytest


@pytest.mark.parametrize("endpoint", ["/api/", "/api/healthz"])
def test_health_endpoint_must_return_200(api_client, app, endpoint):
    response = api_client.get(endpoint)

    expected_response = dict(service="Purchasing Manager", version=app.config["VERSION"])

    assert HTTPStatus.OK == response.status_code
    assert expected_response == response.json


@pytest.mark.parametrize("endpoint", ["/api/", "/api/healthz"])
@patch("purchasing_manager.presentation.views.api.Index.get")
def test_health_must_return_500(mock_get, api_client, endpoint):
    fp = mock_open()
    fp.close = Mock()

    mock_get.side_effect = HTTPError(Mock(), Mock(), "Some error", Mock(), fp)
    expected_response = dict(message="Internal Server Error")

    response = api_client.get(endpoint)

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code
    assert expected_response == response.json
