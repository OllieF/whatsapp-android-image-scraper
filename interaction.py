from dataclasses import dataclass

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
    """Geneic swipe left action for the full screen"""
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
        self.text = {}
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

    def search(self, search_text: str) -> Text | None:
        if search_text in self.keys:
            return self.text[search_text]
        return None

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
