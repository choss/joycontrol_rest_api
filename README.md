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

The base64 encoded data for spi firmware or nfc data should not contain line breaks. You can achieve this with the sample below.

```bash
base64 -w 0 spi_firm.bin > spi_firm_base64.txt
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