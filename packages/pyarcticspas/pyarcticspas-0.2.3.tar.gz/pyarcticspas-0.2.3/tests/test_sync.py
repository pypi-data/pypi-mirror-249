""" Synchronous tests """
import os
import time

from pyarcticspas import LightState, Spa
from pyarcticspas.error import UnauthorizedError


def get_spa():
    """Get the Spa object"""
    token = os.environ.get("ARCTICSPAS_TOKEN")
    assert token is not None
    return Spa(token)


def test_authentication_error():
    """Test: No token should lead to Unauthorized error."""
    spa = Spa("")
    try:
        spa.status()
    except UnauthorizedError:
        pass


def test_connected():
    """Test: Check if API is reachable by polling for the current status."""
    spa = get_spa()
    status = spa.status()
    assert status.connected is True


def test_lights():
    """Test: Switch Arctic Spa light."""
    # Query light status
    spa = get_spa()
    spa_status = spa.status()
    assert spa_status.lights in (LightState["ON"], LightState["OFF"])

    # Create expected new state
    new_light_state = LightState["ON"]
    if spa_status.lights == LightState["ON"]:
        new_light_state = LightState["OFF"]

    # Send expected new state
    spa.set_lights(new_light_state)

    # Query light status again
    time.sleep(2)
    new_spa_status = spa.status()
    assert new_spa_status.lights == new_light_state.value
