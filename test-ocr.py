import cv2
import pytesseract
import sys

# img = cv2.imread('screen.png')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

config = r'--oem 3 --psm 4'
# data = pytesseract.image_to_data(img, config=config, lang='eng')
data = pytesseract.image_to_data(sys.argv[1], config=config, lang='eng')

# print(data)
for i, line in enumerate(data.splitlines()):
    if i == 0:
        # ignore header line
        continue

    el = line.split()
    x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
    if len(el) > 11:
        # If there is text that has been identified
        text = el[11]
        if text:
            print(f"{text} x={x+(0.5*w)} y={y+(0.5*h)}")
            # # only draw box if text was found
            # a = cv2.rectangle(img, (x,y), (w + x, h + y), (0, 0, 255), 2)
            # font = cv2.FONT_HERSHEY_COMPLEX

            # cv2.putText(img, text, (x, y), font, 1, (0,0,0), 3)
            # cv2.putText(img, text, (x, y), font, 1, (255, 255, 255), 2)

# cv2.imwrite('boxes.png', img)