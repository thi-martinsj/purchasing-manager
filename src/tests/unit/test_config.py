from unittest.mock import Mock

import pytest

from purchasing_manager.application.exceptions import ConfigurationNotValid
from purchasing_manager.config import set_app_config


def test_app_config_must_raises_exception_when_mode_is_not_found():
    with pytest.raises(ConfigurationNotValid):
        set_app_config(Mock(), "Xpto")
