import base64  # noqa: D100
import json

from PIL import Image
import requests


class InvalidPixooResponse(Exception):
    """
    Raised when an email address is invalid
    """

    pass


class Pixoo:  # noqa: D101
    ### proxy to communicate with a DIVOOM PIXOO. ###
    __timeout = 10
    __pic_id = 0
    __text_id = 0
    __refresh_pic_id_limit = 32
    debug = False

    def __init__(  # noqa: D107
        ### constructor... ###
        self,
        address,
        size=64,
        debug=False,
        auto_pic_id_reset=True,
        load_counter=True,
        timeout=10,
    ) -> None:
        assert size in [16, 32, 64], (
            "Invalid screen size (pixels). " "Valid options are 16, 32, and 64"
        )

        self.auto_pic_id_reset = auto_pic_id_reset
        self.address = address
        self.debug = debug
        self.size = size

        # Generate URL
        self.__url = "http://{0}/post".format(address)
        self.__timeout = timeout

        if load_counter:
            # Retrieve the counter
            self.__load_counter()

            # Resetting if needed
            if self.auto_pic_id_reset and self.__pic_id > self.__refresh_pic_id_limit:
                self.reset_pic_id()

    def send_images(self, images: [Image], speed=60) -> None:
        self.__increment_pic_id()

        offset = 0
        json_data = {"Command": "Draw/CommandList", "CommandList": []}

        for frame in images:
            json_data["CommandList"].append(
                {
                    "Command": "Draw/SendHttpGif",
                    "PicNum": len(images),
                    "PicWidth": 64,
                    "PicOffset": offset,
                    "PicID": self.__pic_id,
                    "PicSpeed": speed,
                    "PicData": str(
                        base64.b64encode(
                            bytearray(frame.tobytes("raw", "RGB"))
                        ).decode()
                    ),
                }
            )

            offset += 1

        self.__request(json_data)

    def send_image(self, image: Image):
        self.__increment_pic_id()

        self.__request(
            {
                "Command": "Draw/SendHttpGif",
                "PicNum": 1,
                "PicWidth": 64,
                "PicOffset": 0,
                "PicID": self.__pic_id,
                "PicSpeed": 1000,
                "PicData": str(
                    base64.b64encode(bytearray(image.tobytes("raw", "RGB"))).decode()
                ),
            }
        )

    def __reset_text_id(self):
        self.__text_id = 1

    def clear_text(self):
        self.__reset_text_id()
        self.__request({"Command": "Draw/ClearHttpText"})

    def send_text(
        self,
        text,
        speed=10,
        xy=(0, 0),
        dir=0,
        font=0,
        align=1,
        color="#FFFF00",
    ):
        assert len(xy) == 2, "Invalid xy. " "xy must be a list of len 2"

        self.__text_id += 1
        if self.__text_id >= 20:
            self.__reset_text_id()

        self.__request(
            {
                "Command": "Draw/SendHttpText",
                "TextId": self.__text_id,
                "x": xy[0],
                "y": xy[1],
                "dir": dir,
                "font": font,
                "TextWidth": 64 - xy[0],
                "speed": speed,
                "TextString": text,
                "color": color,
                "align": align,
            }
        )

    def set_visualizer(self, equalizer_position):
        ### set visualizer. ###
        self.__request(
            {"Command": "Channel/SetEqPosition", "EqPosition": equalizer_position}
        )

    def set_clock(self, clock_id):
        ### set clock face. ###
        self.__request(
            {"Command": "Channel/SetClockSelectId", "ClockId": int(clock_id)},
        )

    def set_custom_channel(self, index):
        self.set_custom_page(index)
        self.set_channel(3)

    def set_custom_page(self, index):
        self.__request(
            {"Command": "Channel/SetCustomPageIndex", "CustomPageIndex": index}
        )

    def set_screen(self, on=True):
        ### set screen on/off. ###
        self.__request({"Command": "Channel/OnOffScreen", "OnOff": 1 if on else 0})

    def set_temperature_in_celsius(self, on=True):
        ### set screen on/off. ###
        self.__request({"Command": "Device/SetDisTempMode", "Mode": 0 if on else 1})

    def set_timer(self, minute, second=0, start=True):
        ### set screen on/off. ###
        self.__request(
            {
                "Command": "Tools/SetTimer",
                "Minute": minute,
                "Second": second,
                "Status": 1 if start else 0,
            }
        )

    def get_all_conf(self):
        return self.__request({"Command": "Channel/GetAllConf"})

    def get_state(self):
        data = self.get_all_conf()
        if data["LightSwitch"] == 1:
            return True
        else:
            return False

    def set_system_time(self, utc_time):
        return self.__request({"Command": "Device/SetUTC", "Utc": utc_time})

    def set_24_hour_mode(self, on=True):
        return self.__request(
            {"Command": "Device/SetTime24Flag", "Mode": 1 if on else 0}
        )

    def get_system_time(self):
        response = self.__request({"Command": "Device/GetDeviceTime"})
        return response["UTCTime"]

    def set_rotation_angle(self, angle=0):
        ### set rotation angle in degree ###
        assert angle in [0, 90, 180, 270], (
            "Invalid angle. " "Valid options are 0, 90, 180 and 270"
        )
        mode = 0
        if angle == 90:
            mode = 1
        elif angle == 180:
            mode = 2
        elif angle == 270:
            mode = 3

        return self.__request(
            {"Command": "Device/SetScreenRotationAngle", "Mode": mode}
        )

    def set_brightness(self, brightness):
        ### set brightness value ###
        return self.__request(
            {"Command": "Channel/SetBrightness", "Brightness": brightness}
        )

    def get_brightness(self):
        data = self.get_all_conf()
        return data["Brightness"]

    def reset_pic_id(self):
        if self.debug:
            print("[.] Resetting counter remotely")

        self.__request({"Command": "Draw/ResetHttpGifId"})

    def __load_counter(self):
        data = self.__request({"Command": "Draw/GetHttpGifId"})
        self.__pic_id = int(data["PicId"])
        if self.debug:
            print("[.] Counter loaded and stored: " + str(self.__pic_id))

    def __increment_pic_id(self):
        # Add to the internal counter
        self.__pic_id = self.__pic_id + 1

        # Check if we've passed the limit and reset the counter for the animation remotely
        if self.auto_pic_id_reset and self.__pic_id >= self.__refresh_pic_id_limit:
            self.reset_pic_id()
            self.__pic_id = 1

    def __request(self, data: list):
        response = requests.post(self.__url, json.dumps(data), timeout=self.__timeout)
        response.raise_for_status()

        json_response = response.json()

        if json_response["error_code"] != 0:
            raise InvalidPixooResponse(
                "Pixoo Error code: {0}".format(json_response["error_code"])
            )

        return json_response
