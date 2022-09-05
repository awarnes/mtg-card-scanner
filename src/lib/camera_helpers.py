import json
import platform
import subprocess

import cv2

from utils import (
    is_mac,
    is_windows,
    logger
)

class CameraNotFound(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

        logger(errors)

class OSNotSupported(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

        logger(errors)

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    test_port = 0

    non_working_ports = []
    working_ports = []
    available_ports = []

    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(test_port)

        if not camera.isOpened():
            non_working_ports.append(test_port)
            logger(f"Port {test_port} is not working.")
        else:
            is_reading, img = camera.read()
            width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

            if is_reading:
                logger(f"Port {test_port} is working and reads images ({height} x {width})")
                working_ports.append(test_port)
            else:
                logger(f"Port {test_port} for camera ({height} x {width}) is present but cannot read.")
                available_ports.append(test_port)

        test_port += 1

    return working_ports, available_ports, non_working_ports

def list_system_cameras():
    """
    macOS return example:
    {
        "SPCameraDataType" : [
            {
                "_name" : "FaceTime HD Camera (Built-in)",
                "spcamera_model-id" : "UVC Camera VendorID_1452 ProductID_34304",
                "spcamera_unique-id" : "0x1420000005ac8600"
            }
        ]
    }
    """
    
    if is_windows():
        import wmi

        c = wmi.WMI()
        wql = "SELECT * FROM Win32_USBControllerDevice"
        cameras = []

        for item in c.query(wql):
            item_class = item.Dependent.PNPClass
            item_name = item.Dependent.Name.upper()
            if (item_class.upper() == 'MEDIA' or item_class.upper() == 'CAMERA') and 'AUDIO' not in item_name:
                cameras.append(item.Dependent.Name)
        
        return cameras

    elif is_mac():
        result = subprocess.run([
            'system_profiler',
            '-json',
            'SPCameraDataType'
        ], stdout=subprocess.PIPE)

        return [camera['_name'] for camera in json.loads(result)['SPCameraDataType']]

    else:
        raise OSNotSupported(f"{platform.system()} is not supported at this time")

def get_cameras():
    working, available, not_working = list_ports()
    cameras = list_system_cameras()

    if len(cameras) > 0 and len(working) > 0:
        return list(zip(working, cameras))
    else:
        raise CameraNotFound(f"No cameras found connected to system")