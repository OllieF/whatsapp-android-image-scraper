from dataclasses import dataclass
from time import sleep
from typing import Optional, Callable
import cv2
import pytesseract


def swipe(device: any, x_1: int, y_1: int, x_2: int, y_2: int, speed: int = None):
    """Executes a swipe motion from x_1, y_1 to x_2, y_2.
    Optionally: speed in ms (1000 default)
    """
    cmd = f"input swipe {x_1} {y_1} {x_2} {y_2} {speed}"
    device.shell(cmd)


def tap(device: any, x: int, y: int):
    """Generic tap action"""
    cmd = f"input tap {x} {y}"
    device.shell(cmd)


def swipe_left(device: any):
    """Generic swipe left action for the full screen"""
    swipe(device, 250, 1000, 850, 1000, 100)


def open_menu(device: any):
    """Opens the three-dot menu on WhatsApp"""
    tap(device, 1000, 150)


@dataclass
class Text:
    text: str
    x: int
    y: int
    w: int
    h: int
    confidence: float

    @property
    def location(self) -> tuple[float, float]:
        return self.x + (0.5 * self.w), self.y + (0.5 * self.h)

    @property
    def xy_location(self) -> dict[str, float]:
        loc = self.location
        return {"x": loc[0], "y": loc[1]}

    def __repr__(self) -> str:
        return f"<interaction.Text text={self.text} x={self.x} y={self.y}>"


class Screenshot:
    def __init__(self, device) -> None:
        screenshot_loc = "screen"
        self.text: dict[str, any] = {}
        self.take_store_screenshot(device, screenshot_loc)
        self.data = pytesseract.image_to_data(
            f"{screenshot_loc}.png", config=r"--oem 3 --psm 4", lang="eng"
        )
        self._extract_text()
        self.keys = self.text.keys()

    def take_store_screenshot(self, device: any, loc: str = "screen"):
        image = device.screencap()

        with open(f"{loc}.png", "wb") as f:
            f.write(image)

    def _extract_text(self):
        for i, line in enumerate(self.data.splitlines()):
            if i == 0:
                # ignore header line
                continue

            el = line.split()
            if len(el) > 11:
                # If there is text that has been identified
                text = el[11]
                if text:
                    self.text[text] = Text(
                        text=el[11],
                        x=int(el[6]),
                        y=int(el[7]),
                        w=int(el[8]),
                        h=int(el[9]),
                        confidence=float(el[10]),
                    )

    def search(self, search_text: str, norm: bool=False) -> Text | None:
        if search_text in self.keys:
            return self.text[search_text]
        if norm:
            lower_text = dict((k.lower(), v) for k, v in self.text.iteritems())
            if search_text.lower() in lower_text.keys():
                return lower_text[search_text.lower()]
        return None

    @property
    def contact_text(self) -> str:
        return "-".join(self.keys)

class CroppedScreenshot(Screenshot):
    def __init__(self, device: any, x: float, y: float, w: float, h: float) -> None:
        screenshot_loc = "screen"
        cropped_loc = "crop"
        self.text = {}
        self.take_store_screenshot(device, screenshot_loc)
        self.crop(screenshot_loc, cropped_loc, x, y, w, h)
        self.data = pytesseract.image_to_data(
            f"{cropped_loc}.png", config=r"--oem 3 --psm 4", lang="eng"
        )
        self._extract_text()
        self.keys = self.text.keys()

    def crop(
        self,
        screenshot_loc: str,
        cropped_loc: str,
        x: float,
        y: float,
        w: float,
        h: float,
    ):
        img = cv2.imread(f"{screenshot_loc}.png")
        crop_img = img[y : y + h, x : x + w]
        cv2.imwrite(f"{cropped_loc}.png", crop_img)

@dataclass
class Context:
    device: any
    name: str
    number: int = 1

@dataclass
class StepContext:
    device: any
    name: str

class Step:
    """A step in the overall workflow. Each step is made up of 3 components:
    
    1. `action` - a callable that performs some action on the screen
    2. `wait` - amount of time to wait before validating
    3. `validate` - [optional] a callable that validates whether the action was
    successful 
    """

    def __init__(
        self,
        name: str,
        action: callable,
        validate: Optional[Callable[...,bool]] = None,
        wait: float = 2
    ) -> None:
        self.name = name
        self.action = action
        self.validate = validate
        self.wait = wait

    
    def run_actions(self) -> None:
        """Run the action function"""
        self.action(
            data=self.data,
            context=self.context,
            store=self.store
        )
        print("✏️", end=" ")

    def validate_step(self) -> bool:
        """Run the validation function"""
        print("🔍", end=" ")
        return self.validate(
            data=self.data,
            context=self.context,
            store=self.store
        )

    def run(self, data: dict, workflow_context: Context, store: dict):
        """Runs the action, wait and validation"""
        self.context = StepContext(
            device=workflow_context.device,
            name=self.name
        )
        self.data = data
        self.store = store
        executions = 1
        print(f"{self.name}", end=" ")
        while True:
            self.run_actions()
            if not self.validate:
                print("✅")
                return True
            while executions < 3:
                sleep(self.wait)
                if self.validate_step():
                    print("✅")
                    return True
                print("🔄", end=" ")
                executions += 1
            raise RuntimeError(f"Failed step {self.context.name}. Fix and retry")

class Workflow:

    def __init__(self, name: str, device: any) -> None:
        self.context = Context(device=device, name=name)
        self.store = {}
        self.result = {}
    
    def step(self, step: Step):
        print(f"Step {self.context.number}", end=" ")
        step.run(self.result, self.context, self.store)
        self.context.number += 1
        return self
