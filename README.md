# Python GUI for running QMini Spectrometers

Requires libusb as a backend

## Setting up on macOS
I recommend running everything through homebrew.

```brew install libusb```

```brew install python3```

## Setting up on Windows
I downloaded the libusb windows binaries (https://libusb.info/), unzipped the folder then copied MinGW64/dll/libusb-1.0.dll to your C:/Windows/System32 folder. 

Regardless of how you install python/libusb then you'll want to go to the spectrometer folder and 

```python3 -m pip install -r requirements.txt``` 

which will install all the python packages required (recommend doing this in a venv!)
Plug in your spectrometer and run

```python main.py```
