from time import sleep

from ppadb.client import Client as AdbClient

import interaction as ia
import locs


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

workflow = ia.Workflow("WhatsApp Automation", device=device)

# Step 0
def print_header(data: dict, context: ia.StepContext, store: dict) -> dict | None:
    header = ia.CroppedScreenshot(context.device, **locs.WHATSAPP_IMAGE_HEADER)
    data["name"] = header.contact_text

step_0 = ia.Step(
    "Get Header",
    action=print_header
)

# Step 1
def open_menu(data: dict, context: ia.StepContext, store: dict) -> dict | None:
    ia.tap(context.device, **locs.WHATSAPP_MENU)

def validate_open(data: dict, context: ia.StepContext, store: dict) -> bool:
    share_text = ia.Screenshot(context.device).search("Share")
    if share_text:
        data["share_loc"] = share_text
        return True
    else:
        return False

step_open_menu = ia.Step(
    "Open Image Menu",
    action=open_menu,
    validate=validate_open,
    wait=0.5
) 

# Step 2
def select_share(data: dict, context: ia.StepContext, **kwargs):
    ia.tap(context.device, **data["share_loc"].xy_location)

def validate_share(data: dict, context: ia.StepContext, **kwargs) -> bool:
    dropbox_text = ia.Screenshot(context.device).search("Dropbox")
    if dropbox_text:
        data["dropbox_loc"] = dropbox_text
        return True
    else:
        return False

step_select_share = ia.Step(
    "Select Share",
    action=select_share,
    validate=validate_share,
    wait=1.5
)

# Step 3
def select_dropbox(data: dict, context: ia.StepContext, **kwargs):
    ia.tap(context.device, **data["dropbox_loc"].xy_location)

def validate_add(data: dict, context: ia.StepContext, **kwargs) -> bool:
    add_text = ia.Screenshot(context.device).search("Add")
    if add_text:
        data["add_loc"] = add_text
        return True
    else:
        return False

step_select_dropbox = ia.Step(
    "Select Dropbox",
    action=select_dropbox,
    validate=validate_add,
    wait=1
)

# Step 4
def select_add(data: dict, context: ia.StepContext, **kwargs):
    ia.tap(context.device, **data["add_loc"].xy_location)

def validate_upload(data: dict, context: ia.StepContext, **kwargs) -> bool:
    upload_text = ia.Screenshot(context.device).search("Upload")
    if upload_text:
        data["upload_loc"] = upload_text
        return True
    else:
        return False

step_select_add = ia.Step(
    "Select Add",
    action=select_add,
    validate=validate_upload,
    wait=1.5
)

# Step 5
def select_upload(data: dict, context: ia.StepContext, **kwargs):
    ia.tap(context.device, **data["upload_loc"].xy_location)

def validate_upload_pressed(data: dict, context: ia.StepContext, **kwargs) -> bool:
    replace_text = ia.Screenshot(context.device).search("Replace")
    uploaded_text = ia.Screenshot(context.device).search("Uploaded")
    if replace_text or uploaded_text:
        if replace_text:
            data["replace_loc"] = replace_text
        return True
    else:
        return False

step_select_upload = ia.Step(
    "Select Upload",
    action=select_upload,
    validate=validate_upload_pressed,
    wait=4
)

# Step 6
def select_replace(data: dict, context: ia.StepContext, **kwargs):
    if "replace_loc" in data.keys():
        ia.tap(context.device, **data["replace_loc"].xy_location)
        print("♻️", end=" ")

def validate_uploaded(data: dict, context: ia.StepContext, **kwargs) -> bool:
    if "replace_loc" not in data.keys():
        return True
    uploaded_text = ia.Screenshot(context.device).search("Uploaded")
    if uploaded_text:
        return True
    else:
        return False

step_select_replace = ia.Step(
    "Check replace",
    action=select_replace,
    validate=validate_uploaded,
    wait=4
)

# Step 7
def select_close(data: dict, context: ia.StepContext, **kwargs):
    ia.tap(context.device, **locs.DROPBOX_CLOSE_BUTTON)

def validate_closed(data: dict, context: ia.StepContext, **kwargs) -> bool:
    uploaded_text = ia.Screenshot(context.device).search("Uploaded")
    if not uploaded_text:
        return True
    else:
        return False

step_close = ia.Step(
    "Close Pop-up",
    action=select_close,
    validate=validate_closed,
    wait=0.5
)

# Step 8
def swipe_left(**kwargs):
    ia.swipe_left(device)
    sleep(0.5)

step_swipe_left = ia.Step(
    "Swipe Left",
    action=swipe_left
)

last_header = ""
repeats = 0
runs = 1
while True:
    print(f"Run {runs}")
    workflow.context.number = 0
    try:
        workflow = workflow.step(
            step_0
        ).step(
            step_open_menu
        ).step(
            step_select_share
        ).step(
            step_select_dropbox
        ).step(
            step_select_add
        ).step(
            step_select_upload
        ).step(
            step_select_replace
        ).step(
            step_close
        ).step(
            step_swipe_left
        )
    except RuntimeError as e:
        print(f" > {e}")
        print(" > Fix and go back to the image")
        input(" > Press enter")
    runs += 1
    print(f"Completed {workflow.result.get('name')}")
    if last_header == workflow.result.get("name"):
        repeats += 1
        if repeats > 4:
            print("Completed")
            break
    last_header = workflow.result.get("name")
    repeats = 0