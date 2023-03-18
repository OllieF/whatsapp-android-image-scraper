from ppadb.client import Client as AdbClient
import interaction as ia
import locs
from time import sleep

client = AdbClient(host="127.0.0.1", port=5037)
print("Select device:")
for i, device in enumerate(client.devices()):
    print(f"({i})", device.serial, sep="\t")

choice = input("> Select device number: ")
try:
    serial_choice = client.devices()[int(choice)].serial
    device = client.device(serial_choice)
    print(f"Attached to device {device.serial}")
except Exception as e:
    print("Unable to select device")
    print(e)
    exit()

input("Press enter when on first image to commence script")

while True:
    # 1. Open image menu
    while True:
        header = ia.CroppedScreenshot(device, **locs.WHATSAPP_IMAGE_HEADER)
        print(header.contact_text())
        # Action
        ia.tap(device, **locs.WHATSAPP_MENU)
        # Wait
        sleep(1)
        # Collect
        shot = ia.Screenshot(device)
        share_text = shot.search("Share")
        # Validate
        if share_text:
            break
        input("Fix and continue")

    # 2. Select Share > OCR
    while True:
        # Action
        ia.tap(device, **share_text.xy_location)
        # Wait
        sleep(1)
        # Collect
        shot = ia.Screenshot(device)
        dropbox_text = shot.search("Dropbox")
        # Validate
        if dropbox_text:
            break
        input("Fix and continue")
    
    # 3. Select Dropbox > OCR
    while True:
        # Action
        ia.tap(device, **dropbox_text.xy_location)
        # Wait
        sleep(1)
        # Collect
        shot = ia.Screenshot(device)
        add_text = shot.search("Add")
        # Validate
        if add_text:
            break
        input("Fix and continue")

    # 4. Select "Add" from > OCR
    while True:
        # Action
        ia.tap(device, **add_text.xy_location)
        # Wait
        sleep(2)
        # Collect
        shot = ia.Screenshot(device)
        upload_text = shot.search("Upload")
        # Validate
        if upload_text:
            break
        input("Fix and Continue")

    # 5. Select "Upload here" > 850 2250
    while True:
        # Action
        ia.tap(device, **locs.DROPBOX_UPLOAD_BUTTON)
        # Wait
        sleep(3)
        # Collect
        shot = ia.Screenshot(device)
        replace_text = shot.search("Replace")
        if replace_text:
            print("Already Exists, replace")
            while True:
                #Action
                ia.tap(device, **replace_text.xy_location)
                # Wait
                sleep(3)
                # Collect
                shot = ia.Screenshot(device)
                replace_text = shot.search("Replace")
                if not replace_text:
                    break
                input("Fix and Continue")
        uploaded_text = shot.search("Uploaded")
        if uploaded_text:
            break
        input("Fix and Continue")
            
    # 7. Close Dropbox
    while True:
        # Action
        ia.tap(device, **locs.DROPBOX_CLOSE_BUTTON)
        # Wait 
        sleep(1)
        shot = ia.Screenshot(device)
        uploaded_text = shot.search("Uploaded")
        if not uploaded_text:
            break
        input("Fix and Continue")

    # 8. Swuipe to next image
    ia.swipe_left(device)
    sleep(1)
