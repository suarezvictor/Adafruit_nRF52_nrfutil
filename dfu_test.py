import sys
import traceback
from dfu_all.dfu import Dfu, DfuTransportSerial, DfuEvent

def dfu_update_progress(progress=0, done=False, log_message=""):
    print("progress...", progress, done, log_message)
  
def dfu_serial(package, port, baudrate, flowcontrol, singlebank, touch):
    """Program a device with bootloader that support serial DFU"""
    #com_port, baud_rate=DEFAULT_BAUD_RATE, flow_control=DEFAULT_FLOW_CONTROL, single_bank=False, touch=0, timeout=DEFAULT_SERIAL_PORT_TIMEOUT)
    serial_backend = DfuTransportSerial(port, baudrate, flowcontrol, singlebank, touch)
    serial_backend.register_events_callback(DfuEvent.PROGRESS_EVENT, dfu_update_progress)
    dfu = Dfu(package, dfu_transport=serial_backend)

    print("Upgrading target on {1} with DFU package {0}. Flow control is {2}, {3} bank, Touch {4}"
               .format(package, port, "enabled" if flowcontrol else "disabled", "Single" if singlebank else "Dual", touch if touch > 0 else "disabled"))

    try:
        dfu.dfu_send_images()

    except Exception as e:
        print("")
        print("Failed to upgrade target. Error is: {0}".format(e))
        traceback.print_exc(file=sys.stdout)
        print("")
        print("Possible causes:")
        print("- Selected Bootloader version does not match the one on Bluefruit device.")
        print("    Please upgrade the Bootloader or select correct version in Tools->Bootloader.")
        print("- Baud rate must be 115200, Flow control must be off.")
        print("- Target is not in DFU mode. Ground DFU pin and RESET and release both to enter DFU mode.")

        return False

    print("Device programmed.")

    return True

dfu_serial("/tmp/arduino_build_235216/proto_modbus.ino.zip", "/dev/ttyUSB0", 115200, False, True, 0)
