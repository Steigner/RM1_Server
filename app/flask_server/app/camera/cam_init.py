import pyrealsense2 as rs
import time
import json


class Camera_Init(object):
    @classmethod
    def find_device_that_supports_advanced_mode(cls):
        DS5_product_ids = [
            "0AD1",
            "0AD2",
            "0AD3",
            "0AD4",
            "0AD5",
            "0AF6",
            "0AFE",
            "0AFF",
            "0B00",
            "0B01",
            "0B03",
            "0B07",
            "0B3A",
        ]
        ctx = rs.context()
        devices = ctx.query_devices()
        info = []

        for dev in devices:
            if (
                dev.supports(rs.camera_info.product_id)
                and str(dev.get_info(rs.camera_info.product_id)) in DS5_product_ids
            ):
                if dev.supports(rs.camera_info.name):
                    info = str(dev.get_info(rs.camera_info.name))

                return dev, info

    @classmethod
    def inicialize(cls, c=False):
        dev, info = cls.find_device_that_supports_advanced_mode()

        if dev is None:
            return "Camera status: not pluged-in compatible device"

        else:
            try:
                advnc_mode = rs.rs400_advanced_mode(dev)

                # Loop until we successfully enable advanced mode
                while not advnc_mode.is_enabled():
                    advnc_mode.toggle_advanced_mode(True)
                    # At this point the device will disconnect and re-connect.
                    time.sleep(5)
                    # The 'dev' object will become invalid and we need to initialize it again
                    advnc_mode = rs.rs400_advanced_mode(dev)

                if c is True:
                    json_f = json.load(open("app/camera/settings/camera_settings.json"))
                    json_string = str(json_f).replace("'", '"')
                    advnc_mode.load_json(json_string)
                    print("Camera is set up")

                return "Camera status: " + info + " is pluged-in"

            except Exception as e:
                print(e)
                pass
