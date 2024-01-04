""" Async tests """
import pytest

from pyarcticspas import Pump, PumpState

from .test_sync import get_spa

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_async_connected():
    """Test: Check if the code connected to the remote Arctic API."""
    spa = get_spa()
    status = await spa.async_status()
    assert status.connected is True


@pytest.mark.asyncio
async def test_async_pump_turn_off():
    """Test: Turn off pump if it's on."""
    spa = get_spa()
    spa_status = await spa.async_status()
    assert spa_status.connected is True

    if spa_status.pump1 == PumpState["ON"]:
        await spa.async_set_pumps(Pump["VALUE_0"], PumpState["OFF"])

        spa_new_status = await spa.async_status()
        assert spa_new_status.pump1 == PumpState["OFF"]
