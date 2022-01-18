# --------------------- In progress !! -----------------------

import pyrealsense2 as rs
import time
import json

class Camera_Init(object):
    @classmethod
    def find_device_that_supports_advanced_mode(cls):
        DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03", "0B07","0B3A"]
        ctx = rs.context()
        ds5_dev = rs.device()
        devices = ctx.query_devices()
        for dev in devices:
            if dev.supports(rs.camera_info.product_id) and str(dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
                if dev.supports(rs.camera_info.name):
                    info = str("Found device that supports advanced mode:" + dev.get_info(rs.camera_info.name))
                return dev
                
        #raise Exception("No device that supports advanced mode was found")
    
    @classmethod
    def inicialize(cls):
        dev = cls.find_device_that_supports_advanced_mode()
        
        cls.dev = dev

        if dev == None:
            return "Camera status: not pluged-in compatible device"
            
        else:
            try:
                advnc_mode = rs.rs400_advanced_mode(dev)
                #info_1 = str("Advanced mode is enabled!")
                
                # Loop until we successfully enable advanced mode
                while not advnc_mode.is_enabled():
                    advnc_mode.toggle_advanced_mode(True)
                    # At this point the device will disconnect and re-connect.
                    time.sleep(5)
                    # The 'dev' object will become invalid and we need to initialize it again
                    dev = find_device_that_supports_advanced_mode()
                    advnc_mode = rs.rs400_advanced_mode(dev)
                
                json_f = json.load(open("app/camera/settings/camera_settings.json"))
                json_string= str(json_f).replace("'", '\"')
                advnc_mode.load_json(json_string)

                #return info_1 + str(" Everything set up succesfully!")
                return "Camera status: device is pluged-in"

            except Exception as e:
                print(e)
                pass