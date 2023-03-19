from ppadb.client import Client as AdbClient
import interaction as ia
import locs
from time import sleep


def Stage(func: callable, *args, **kwargs):
    pass

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
        print("  1. Open Image Menu", end=" ")
        ia.tap(device, **locs.WHATSAPP_MENU)
        # Wait
        sleep(0.5)
        # Collect
        shot = ia.Screenshot(device)
        share_text = shot.search("Share")
        # Validate
        if share_text:
            print("✔️")
            break
        input("  1. Fix and continue")

    # Stage("Open image menu", sleep=5).action(ia.CroppedScreenshot).collect().verify()

    # Stage("Open image menu", sleep 5, action=Step(), collect=Step(), verify=Step())
    # 2. Select Share > OCR
    while True:
        # Action
        print("  2. Select Share", end=" ")
        ia.tap(device, **share_text.xy_location)
        # Wait
        sleep(1.5)
        # Collect
        shot = ia.Screenshot(device)
        dropbox_text = shot.search("Dropbox")
        # Validate
        if dropbox_text:
            print("✔️")
            break
        input("  2. Fix and continue")
    
    # 3. Select Dropbox > OCR
    while True:
        # Action
        print("  3. Select Dropbox", end=" ")
        ia.tap(device, **dropbox_text.xy_location)
        # Wait
        sleep(1)
        # Collect
        shot = ia.Screenshot(device)
        add_text = shot.search("Add")
        # Validate
        if add_text:
            print("✔️")
            break
        input("  3. Fix and continue")

    # 4. Select "Add" from > OCR
    while True:
        # Action
        print("  4. Select 'Add'", end=" ")
        ia.tap(device, **add_text.xy_location)
        # Wait
        sleep(1.5)
        # Collect
        shot = ia.Screenshot(device)
        upload_text = shot.search("Upload")
        # Validate
        if upload_text:
            print("✔️")
            break
        input("  4. Fix and Continue")

    # 5. Select "Upload here" > 850 2250
    while True:
        # Action
        print("  5. Select 'Upload here'", end=" ")
        ia.tap(device, **locs.DROPBOX_UPLOAD_BUTTON)
        # Wait
        sleep(5)
        # Collect
        shot = ia.Screenshot(device)
        replace_text = shot.search("Replace")
        if replace_text:
            print("  replacing ", end="")
            while True:
                #Action
                ia.tap(device, **replace_text.xy_location)
                # Wait
                sleep(4)
                # Collect
                shot = ia.Screenshot(device)
                replace_text = shot.search("Replace")
                if not replace_text:
                    break
                input("Fix and Continue")
        uploaded_text = shot.search("Uploaded")
        if uploaded_text:
            print("✔️")
            break
        input("Fix and Continue")
            
    # 6. Close Dropbox
    while True:
        # Action
        print("  6. Close Dropbox", end=" ")
        ia.tap(device, **locs.DROPBOX_CLOSE_BUTTON)
        # Wait 
        sleep(0.5)
        shot = ia.Screenshot(device)
        uploaded_text = shot.search("Uploaded")
        if not uploaded_text:
            print("✔️")
            break
        input("  6. Fix and Continue")

    # 7. Swuipe to next image
    print("  7. Next Image")
    ia.swipe_left(device)
    sleep(0.5)
