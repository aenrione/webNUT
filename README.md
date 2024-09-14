webNUT
======

A simple web interface for NUT ([Network UPS Tools][1])
servers, built on Pyramid, Bootstrap, and
[python-nut2][2].

[1]: http://www.networkupstools.org/ "Network UPS Tools"
[2]: https://github.com/george2/python-nut2 "python-nut2"

## About
This porject is a fork of [webNUT](https://github.com/rshipp/webNUT) by [rshipp](https://github.com/rshipp) that tries to add some features to the original project. The original project is a simple web interface for NUT ([Network UPS Tools](http://www.networkupstools.org/)) servers, built on Pyramid, Bootstrap.

### Changes
- Added some UI elements:
    - navbar for easier navigation
    - charts to easily visualize the **load** and **battery.charge** values
- Added the ability to send notifications when the UPS goes on battery and when the battery differs from the last value by a certain percentage.


### Notifications

This fork adds the ability to send notifications.

Currently only the Email and Telgram part s implemented. This requires to set the variables in the config file. The notifications are sent when:
- the UPS goes on battery and changes status
- the battery differs from the last value by *BATTERY_DIFFERENCE* (default 20%)

## Setup

Rename `webnut/config.example.py` to `webnut/config.py` and set the
variables in that file to reflect your NUT server configuration. Then
serve webNUT as you would any Pyramid app, using `pserve` or through
your production-ready server of choice.

### VENV
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
pserve ../development.ini --reload
```

## Docker
To run the application in a docker container, you can use the provided `Dockerfile` and `docker-compose.yml` files. You can build the image with the following command:
```bash
docker compose build
```
In order to use the notifications feature, you need to set the variables in the webnut/config.py file to reflect your NUT server configuration. You can also set the 
variables inside a *webapp.env* file and run the following command:
```bash
docker compose up
```

## Screenshots

The index lists available UPS devices, along with their description,
status, and battery charge:

![Index](screenshots/ups_index.png "Index")

Clicking on a UPS's name takes you to a details view that shows a quick
status indicator, as well as the values of all variables set on the
device:

![UPS View](screenshots/ups_view.png "UPS View")
