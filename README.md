# joycontrol_rest

A rest client in python for joycontrol. Exposes the joycontrol pro-controller emulation as a restful service. This was tested on an Raspberry PI zero W

This script also needs **root** to run, as it is a requirement of joycontrol



# Package requirements

In addition to the joycontrol packages you also need fastapi and uvicorn.

```bash
sudo pip install fastapi
sudo pip install uvicorn
```

# How to run

- Clone this repo including all submodules
- Since we have a git-submodule on joycontrol we need to expose the folder to pythons module path and then we can run it.

```bash
export PYTHONPATH=./joycontrol
sudo python3 rest.py
```

# Rest api notes

To see the api just run the script and navigate to <ip>:8000. The documentation will be shown
The base64 encoded data for spi firmware or nfc data should not contain line breaks. You can achieve this with the sample below.

```bash
base64 -w 0 spi_firm.bin > spi_firm_base64.txt
```

## Connection example jsons

### Pair with a switch (be on the change grip/ order screen)

```json
{
  "controller_type": "PRO_CONTROLLER"
}
```

### Reconnect to an already paired switch

In this example the MAC of the switch is E1:3F:54:0B:DE:BB

```json
{
  "controller_type": "PRO_CONTROLLER",
  "reconnect_address": "E1:3F:54:0B:DE:BB"
}
```

### All connection attempts also (optionally) take a spi_firmware as base64 encoded string

```json
{
  "controller_type": "PRO_CONTROLLER",
  "spi_firm" : "<very long base64 encoded string>",
}
```

## Responses

The response of every API method is a status response like the one below.

```json
{
  "connected": "true",
  "peer": "AA:BB:CC:DD:EE:FF",
  "controller_type": "PRO_CONTROLLER",
  "buttons": {
    "up": false,
    "a": false,
    "b": false,
    "minus": false,
    "home": false,
    "l_stick": false,
    "zr": false,
    "r": false,
    "zl": false,
    "right": false,
    "capture": false,
    "r_stick": false,
    "y": false,
    "plus": false,
    "left": false,
    "x": false,
    "l": false,
    "down": false
  },
  "nfc_active": false,
  "left_stick": {
    "x_axis": 1987,
    "y_axis": 1912,
    "is_center": true
  },
  "right_stick": {
    "x_axis": 2017,
    "y_axis": 2005,
    "is_center": true
  }
}
```

# Requirements for joycontrol

```bash
sudo apt install python3-dbus libhidapi-hidraw0
sudo pip install hid aioconsole dbus-python crc8
```

In order to do that, change the following line in /lib/systemd/system/bluetooth.service from

```bash
ExecStart=/usr/lib/bluetooth/bluetoothd
```

to

```bash
ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=input
```

and restart Bluetooth with

```bash
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```
