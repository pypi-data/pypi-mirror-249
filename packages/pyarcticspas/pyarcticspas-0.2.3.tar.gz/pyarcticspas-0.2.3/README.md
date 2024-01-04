# pyarcticspas
A high-level python client library for accessing Arctic Spas API.

## Usage

Example:
```python
from pyarcticspas import Spa, LightState, Blower, BlowerState


token = "(Token received from https://myarcticspa.com/spa/SpaAPIManagement.aspx)"
spa = Spa(token)

status=spa.status()
print(status.connected) #True
print(status.lights.value) #off
print(status.blower1.value) #off

spa.set_lights(LightState["ON"])
spa.set_blowers(Blower["VALUE_0"],BlowerState["ON"])

status=spa.status()
print(status.lights.value) #on
print(status.blower1.value) #on
```

If you are using asynchronous calls, use the `async_` version of the calls.
