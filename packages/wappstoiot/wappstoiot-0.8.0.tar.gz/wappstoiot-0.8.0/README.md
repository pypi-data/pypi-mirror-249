Wappsto IoT
===============================================================================
[![versions](https://img.shields.io/pypi/pyversions/wappstoiot.svg)](https://github.com/wappsto/python-wappsto-iot)
[![Test Status](https://github.com/Wappsto/python-wappsto-iot/actions/workflows/test.yml/badge.svg)](https://github.com/Wappsto/python-wappsto-iot/actions/workflows/test.yml)
[![Lint Status](https://github.com/Wappsto/python-wappsto-iot/actions/workflows/lint.yml/badge.svg)](https://github.com/Wappsto/python-wappsto-iot/actions/workflows/lint.yml)
[![Coverage](https://codecov.io/github/wappsto/python-wappsto-iot/branch/main/graph/badge.svg)](https://codecov.io/github/wappsto/python-wappsto-iot)
[![pypi](https://img.shields.io/pypi/v/wappstoiot.svg)](https://pypi.python.org/pypi/wappstoiot)
[![license](https://img.shields.io/github/license/wappsto/python-wappsto-iot.svg)](https://github.com/wappsto/python-wappsto-iot/blob/main/LICENSE)
[![SeluxitA/S](https://img.shields.io/badge/Seluxit_A/S-1f324d.svg?logo=data:image/x-icon;base64,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)](https://seluxit.com)
[![Wappsto](https://img.shields.io/badge/Wappsto-1f324d.svg?logo=data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAEuAAABLgF7cRpNAAAEM0lEQVR4nO1bwY3bMBCcyysBEpw6sDo4P4LgflEHUQm6DlyCSrgOTiU43yAPpgOVoOtATh55bh6iHJm3uyJFOQxwGmCB2CR3h0tyuVxfbogIrxlvUhNIjc0BqQmkxuaA1ARSY3NAagKpsTkgNYHU2BwgfF8BOAIgRloABwD59el5I8fAqQXP+YhhTi9BRFPZE1FL/miIKHN0/EvJLAdftHaOZx3u5PsAZSN6V+k/klX4jsryhcqmqALIx0oVybWnYc5nB4RsIw0l/f+TH9EQEW6I6C2A30Jw+QqgAdDbz4UNJjuh/8n2af3jVxD2AAyAW6H9GQNfYz9nGPh+Efq/G7c/h1pZhaPi2WvFhLkzfyQ5INfCmBxEVAiNMVuxU8gskbkY5RN/OBQxiVAD4EFo29ltmEXoH5FhuMelbf9guSwDEd0L3vFdwUdlZY6RKw/S8xLtmE4lE8bfazEgJKI3Cslm4cTX1FsKOnLtfDwGkjUKWZ8z6spB0RfqVGmXQiPfBRrJSN+uRYCuStHTUniA7Rg9ZuoAydt5oKGc5Gjtez1q1123YPK5oOtAROfXoBFiZBEYUzs75sS03WKI5trNkEFOdE4ASvxNynxRCN8bABePIc7roWfNZwsbZdxaR2gqDaOrH9unHbnsrqdlRrVjRcQ7liM6oorgwS3s+Xr2WbWYtNZ3UmtG/Kns52x7B4sImdvWhdKuHZeYXZiPfdwB3RVIZCRH9V9E9FNoW3LduWIYvd20j/sWODLR8nNg1HXRQ74Z3gP4wHx/wvCMDY34LjjuF3N0HWAERWUkkbGQ6osK8TUFibO5+MRsGw6habEktaB/inolW2L6O5VF5yZSvimT/76iHa94xtUDuDiwwzq/A2QAPintH7FODSEHX7Z7MTfOAUZQWiymc6lbKmzAtkn2Q1Ao9i/AOaAFH7FjA2ED4M6j3x1iKjwDOK4ncIFVOD8Nc35i0uJKOfcSqgh73u8aqSZomO9uMZSlQ7EH8CS0/bDC4SnCHnfMDNc5xAFA+DEYn7ccnq2+0v5b4hEaFP3u/xHKNuJy+DZwK0rvALc4ohVB1rAp6tAUSYmEb37OxZER3PnW4gR7fhmRqr9iIqcpKwRlPtVibTJaVqmV2H2ComS3kMbMKeQwtxqS44j8XpZGGS9OhPRdJ46ZI8NViTql/xoFzYz4NJZovrDKjVN/nJn7aYyLnDvwmVaJdQqave0rFVYN+EhfgE9/jWptZjVyZSUONGzJmvRtS7QsqdHiCFmbteVwIHnn5ZodHyJzk5tD7WFDkjrS9mzM8SFRRBBoPPTPSRNhv5jTf00SaxVRQPr1KMHL+dcg0dF1/laoJPl2cOHt/FASOQ2edYn0NFw31RUm7kplbblBr7Pc8hB9N0Tbf5p61dgckJpAamwOSE0gNTYHpCaQGpsDUhNIjVfvgD9WFsGCdX/VsgAAAABJRU5ErkJggg==)](https://wappsto.com)

The wappstoiot module provide a simple python interface to [wappsto.com](https://wappsto.com/) for easy prototyping.


## Prerequisites

A [wappsto.com](https://wappsto.com/) Account, that the unit can connect to.

The wappsto module requires a set of certificates for authentication. The certificates can be downloaded from [wappsto.com](https://wappsto.com/), or with the build-in CLI tool: `python3 -m wappstoiot`.
The certificates provides the unit with the secure connection to wappsto.com.

To read more about how the Wappsto IoT inner workings, go [here](https://documentation.wappsto.com).

## The Basics

To understand how to use Wappsto IoT, there is some terms that need to be known.
* Control
    - Change request value.
* Report
    - The current value.
* Refresh
    - Value Update request.
* Delete
    - inform that a delete have happened.
* network -> device -> value
    - ...

## Getting Started


## Installation using pip

The wappsto module can be installed using PIP (Python Package Index) as follows:

```bash
$ pip install -U wappstoiot
```


Working examples of usage can be found in the [example folder](./example).

The needed certificates can be downloaded with [IoT Certificate Manager](https://wappsto.com/store/application/iot_certificate_manager).
Where path is the path to the config-folder, given in the following code example.


### Echo example

The following explains the example code found in [echo.py](./example/echo.py).


```python
wappstoiot.config(
    config_Folder="echo"
)
```

```python
network = wappstoiot.createNetwork(
    name="echo",
)
```

```python
device = network.createDevice(
    name="EchoDevice"
)
```

```python
value = device.createValue(
    name="Moeller",
    permission=wappstoiot.PermissionType.READWRITE,
    value_template=wappstoiot.ValueTemplate.STRING
)
```

```python
value.onControl(
    callback=lambda obj, new_value: obj.report(new_value)
)
```

```python
value.onRefresh(
    callback=lambda obj: obj.report(f"{obj.data} Refreshed!")
)
```

```python
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    wappstoiot.close()
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

