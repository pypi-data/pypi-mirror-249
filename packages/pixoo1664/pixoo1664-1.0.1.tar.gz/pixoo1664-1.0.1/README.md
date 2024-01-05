# PIXOO1664

Unofficial Divoom pixoo REST library, beer not included.

To install
```bash
pip install pixoo1664
```

To use:
```python
from pixoo1664 import Pixoo

pixoo = Pixoo("192.168.16.64")
```
## Text

To send text:
```python
pixoo.send_text("Hello there !")
```

To clear text:
```python
pixoo.clear_text()
```

## Image
To create and send an image:
```python
from PIL import Image, ImageDraw

img = Image.new("RGB", size=(64,64))

draw = ImageDraw.Draw(img)
draw.text(text="Who's the", xy=(3, 10), fill=(255, 43, 43, 255))
draw.text(text="BOSS NOW ??", xy=(3, 20), fill=(43, 255, 43, 255))
draw.line(xy=((0, 20), (64, 20)))

pixoo.send_image(img)
```

Send gif frames in one call (60ms btw frames)
```python
# list of Image
pixoo.send_images(images, speed=60)
```

## Brightness

Get brightness 0~100
```python
pixoo.get_brightness() # -> 80
```

Set brightness 0~100
```python
pixoo.set_brightness(90)
```

Set screen on/off
```python
pixoo.set_screen(True)
pixoo.set_screen(False)
```

## Time

Set system time
```python
pixoo.set_system_time(1672416000)
```

Get system time
```python
pixoo.get_system_time() # -> 1672416000
```

Set 24 hour mode (reset when the device power off)
```python
pixoo.set_24_hour_mode(True)
```

Set 12 hour mode (reset when the device power off)
```python
pixoo.set_24_hour_mode(False)
```

## Temperature mode

Set temperature in Celsius
```python
pixoo.set_temperature_in_celsius(True)
```

Set temperature in Fahrenheit
```python
pixoo.set_temperature_in_celsius(False)
```

## Screen rotation

Set rotation angle in degree 0, 90, 180 and 270
```python
pixoo.set_rotation_angle(90)
```

## Configuration

Get all settings (https://doc.divoom-gz.com/web/#/12?page_id=243)
```python
pixoo.get_all_conf()
#   {
#     "Brightness":100,
#     "RotationFlag":1,
#     "ClockTime":60,
#     "GalleryTime":60,
#     "SingleGalleyTime":5,
#     "PowerOnChannelId":1,
#     "GalleryShowTimeFlag":1,
#     "CurClockId":1,
#     "Time24Flag":1,
#     "TemperatureMode":1,
#     "GyrateAngle":1,
#     "MirrorFlag":1,
#     "LightSwitch":1
#   }
```

## Page

Set a timer
```python
pixoo.set_timer(minute=1, second=3, start=True)
```
