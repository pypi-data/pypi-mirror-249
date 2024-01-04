""" Spa class creates an Arctic Spa connection for Python calls """
from http import HTTPStatus
from typing import Optional

from arcticspas import Client
from arcticspas.api.spa_control import (
    v2_blower,
    v2_boost,
    v2_easy_mode,
    v2_filter,
    v2_fogger,
    v2_light,
    v2_pump,
    v2_spa,
    v2_temperature,
    v2sds,
    v2yess,
)
from arcticspas.models import V2BlowerBlower as Blower
from arcticspas.models import V2BlowerJsonBody
from arcticspas.models import V2BlowerJsonBodyState as BlowerState
from arcticspas.models import V2EasyModeJsonBody
from arcticspas.models import V2EasyModeJsonBodyState as EasyModeState
from arcticspas.models import V2FilterJsonBody
from arcticspas.models import V2FilterJsonBodyState as FilterState
from arcticspas.models import V2FoggerJsonBody
from arcticspas.models import V2FoggerJsonBodyState as FoggerState
from arcticspas.models import V2LightJsonBody
from arcticspas.models import V2LightJsonBodyState as LightState
from arcticspas.models import V2PumpJsonBody
from arcticspas.models import V2PumpJsonBodyState as PumpState
from arcticspas.models import V2PumpPump as Pump
from arcticspas.models import V2SDSJsonBody
from arcticspas.models import V2SDSJsonBodyState as SDSState
from arcticspas.models import V2SpaResponse200 as SpaResponse
from arcticspas.models import V2TemperatureJsonBody, V2YESSJsonBody
from arcticspas.models import V2YESSJsonBodyState as YESSState
from arcticspas.types import Response

from pyarcticspas.error import (
    ClientError,
    EmptyResponseError,
    InformationError,
    RedirectionError,
    ServerError,
    SpaHTTPException,
    TooManyRequestsError,
    UnauthorizedError,
)

from .const import _URL


def _filter_parsed(response: Response):
    """
    Filter out the parsed content from an API response.
    Raise an exception if an error is returned or there is no content.
    """
    if response.status_code == HTTPStatus.OK:  # 200
        return response.parsed
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:  # 429
        raise TooManyRequestsError(response.status_code)
    if response.status_code == HTTPStatus.UNAUTHORIZED:  # 401
        raise UnauthorizedError(response.status_code)
    if response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:  # 500
        raise ServerError(response.status_code)
    if response.status_code >= HTTPStatus.BAD_REQUEST:  # 400
        raise ClientError(response.status_code)
    if response.status_code >= HTTPStatus.MULTIPLE_CHOICES:  # 300
        raise RedirectionError(response.status_code)
    if response.status_code >= HTTPStatus.CREATED:  # 201
        if hasattr(response, "parsed"):
            return response.parsed
        raise EmptyResponseError(response.status_code)
    if response.status_code >= HTTPStatus.CONTINUE:  # 100
        raise InformationError(response.status_code)
    raise SpaHTTPException(418)  # I'm a teapot - this should never happen.


class Spa:
    """Spa class defines high-level functions using the Arctic Spa API."""

    def __init__(self, token: str):
        self.__client = Client(base_url=_URL, headers={"X-API-KEY": token})

    def status(self) -> SpaResponse:
        """Get ArcticSpa status object."""
        return _filter_parsed(v2_spa.sync_detailed(client=self.__client))

    async def async_status(self):
        """Get ArcticSpa status object in asynchronous code."""
        return _filter_parsed(await v2_spa.asyncio_detailed(client=self.__client))

    def set_temperature(self, setpoint_f: int):
        """Set ArcticSpa expected temperature."""
        json_body = V2TemperatureJsonBody()
        json_body.setpoint_f = setpoint_f
        return _filter_parsed(
            v2_temperature.sync_detailed(client=self.__client, json_body=json_body)
        )

    async def async_set_temperature(self, setpoint_f: int):
        """Set ArcticSpa expected temperature in asynchronous code."""
        json_body = V2TemperatureJsonBody()
        json_body.setpoint_f = setpoint_f
        return _filter_parsed(
            await v2_temperature.asyncio_detailed(client=self.__client, json_body=json_body)
        )

    def set_lights(self, state: LightState):
        """Turn ArcticSpa light on or off."""
        json_body = V2LightJsonBody()
        json_body.state = state
        return _filter_parsed(v2_light.sync_detailed(client=self.__client, json_body=json_body))

    async def async_set_lights(self, state: LightState):
        """Turn ArcticSpa light on or off in asynchronous code."""
        json_body = V2LightJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2_light.asyncio_detailed(client=self.__client, json_body=json_body)
        )

    def set_pumps(self, pump: Pump, state: PumpState):
        """Set ArcticSpa Pump state."""
        json_body = V2PumpJsonBody()
        json_body.state = state
        return _filter_parsed(
            v2_pump.sync_detailed(pump=pump, client=self.__client, json_body=json_body)
        )

    async def async_set_pumps(self, pump: Pump, state: PumpState):
        """Set ArcticSpa Pump state in asynchronous code."""
        json_body = V2PumpJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2_pump.asyncio_detailed(pump=pump, client=self.__client, json_body=json_body)
        )

    def set_easymode(self, state: EasyModeState):
        """Turn Easy mode on or off."""
        json_body = V2EasyModeJsonBody()
        json_body.state = state
        return _filter_parsed(v2_easy_mode.sync_detailed(client=self.__client, json_body=json_body))

    async def async_set_easymode(self, state: EasyModeState):
        """Turn Easy mode on or off in asynchronous code."""
        json_body = V2EasyModeJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2_easy_mode.asyncio_detailed(client=self.__client, json_body=json_body)
        )

    def set_sds(self, state: SDSState):
        """Turn SDS on or off."""
        json_body = V2SDSJsonBody()
        json_body.state = state
        return _filter_parsed(v2sds.sync_detailed(client=self.__client, json_body=json_body))

    async def async_set_sds(self, state: SDSState):
        """Turn SDS on or off in asynchronous code."""
        json_body = V2SDSJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2sds.asyncio_detailed(client=self.__client, json_body=json_body)
        )

    def set_yess(self, state: YESSState):
        """Turn YESS on or off."""
        json_body = V2YESSJsonBody()
        json_body.state = state
        return _filter_parsed(v2yess.sync_detailed(client=self.__client, json_body=json_body))

    async def async_set_yess(self, state: YESSState):
        """Turn YESS on or off in asynchronous code."""
        json_body = V2YESSJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2yess.asyncio_detailed(client=self.__client, json_body=json_body)
        )

    def boost(self):
        """Turn Boost on or off."""
        return _filter_parsed(v2_boost.sync_detailed(client=self.__client))

    async def async_boost(self):
        """Turn Boost on or off in asynchronous code."""
        return _filter_parsed(await v2_boost.asyncio_detailed(client=self.__client))

    def set_fogger(self, state: FoggerState):
        """Turn fogger on or off."""
        json_body = V2FoggerJsonBody()
        json_body.state = state
        return _filter_parsed(v2_fogger.sync_detailed(client=self.__client, json_body=json_body))

    async def async_set_fogger(self, state: FoggerState):
        """Turn fogger on or off in asynchronous code."""
        json_body = V2FoggerJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2_fogger.asyncio_detailed(client=self.__client, json_body=json_body)
        )

    def set_blowers(self, blower: Blower, state: BlowerState):
        """Turn blower on or off."""
        json_body = V2BlowerJsonBody()
        json_body.state = state
        return _filter_parsed(
            v2_blower.sync_detailed(blower=blower, client=self.__client, json_body=json_body)
        )

    async def async_set_blowers(self, blower: Blower, state: BlowerState):
        """Turn blower on or off in asynchronous code."""
        json_body = V2BlowerJsonBody()
        json_body.state = state
        return _filter_parsed(
            await v2_blower.asyncio_detailed(
                blower=blower, client=self.__client, json_body=json_body
            )
        )

    def set_filter(
        self,
        state: Optional[FilterState] = None,
        frequency: Optional[int] = None,
        duration: Optional[int] = None,
        suspension: Optional[bool] = None,
    ):
        """Set filter."""
        json_body = V2FilterJsonBody()
        if state is not None:
            json_body.state = state
        if frequency is not None:
            json_body.frequency = frequency
        if duration is not None:
            json_body.duration = duration
        if suspension is not None:
            json_body.suspension = suspension
        return _filter_parsed(v2_filter.sync_detailed(client=self.__client, json_body=json_body))

    async def async_set_filter(
        self,
        state: Optional[FilterState] = None,
        frequency: Optional[int] = None,
        duration: Optional[int] = None,
        suspension: Optional[bool] = None,
    ):
        """Set filter in asynchronous mode."""
        json_body = V2FilterJsonBody()
        if state is not None:
            json_body.state = state
        if frequency is not None:
            json_body.frequency = frequency
        if duration is not None:
            json_body.duration = duration
        if suspension is not None:
            json_body.suspension = suspension
        return _filter_parsed(
            await v2_filter.asyncio_detailed(client=self.__client, json_body=json_body)
        )
