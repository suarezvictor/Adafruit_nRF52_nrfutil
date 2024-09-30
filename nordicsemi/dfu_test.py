from dfu.dfu import Dfu
from dfu.dfu_transport_serial import DfuTransportSerial
from dfu.dfu_transport import DfuEvent

def update_progress(progress=0, done=False, log_message=""):
    print("progress...", progress, done, log_message)
  
def serial(package, port, baudrate, flowcontrol, singlebank, touch):
    """Program a device with bootloader that support serial DFU"""
    serial_backend = DfuTransportSerial(port, baudrate, flowcontrol, singlebank, touch)
    serial_backend.register_events_callback(DfuEvent.PROGRESS_EVENT, update_progress)
    dfu = Dfu(package, dfu_transport=serial_backend)

    print("Upgrading target on {1} with DFU package {0}. Flow control is {2}, {3} bank, Touch {4}"
               .format(package, port, "enabled" if flowcontrol else "disabled", "Single" if singlebank else "Dual", touch if touch > 0 else "disabled"))

    try:
        dfu.dfu_send_images()

    except Exception as e:
        click.echo("")
        click.echo("Failed to upgrade target. Error is: {0}".format(e))
        traceback.print_exc(file=sys.stdout)
        click.echo("")
        click.echo("Possible causes:")
        click.echo("- Selected Bootloader version does not match the one on Bluefruit device.")
        click.echo("    Please upgrade the Bootloader or select correct version in Tools->Bootloader.")
        click.echo("- Baud rate must be 115200, Flow control must be off.")
        click.echo("- Target is not in DFU mode. Ground DFU pin and RESET and release both to enter DFU mode.")

        return False

    print("Device programmed.")

    return True

serial("/tmp/arduino_build_235216/proto_modbus.ino.zip", "/dev/ttyUSB0", 115200, False, True, False)
