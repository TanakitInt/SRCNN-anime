import os
import cv2

directory = "input/"

count = 1

for filename in os.listdir(directory):

    if filename.endswith(".png") or filename.endswith(".PNG"):

        file_location = directory + filename

        # Read Image
        img = cv2.imread(file_location, cv2.IMREAD_COLOR)

        # Resize
        img = cv2.resize(img, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)

        out_location = "output/irl-test_" + str(count) + ".png"

        cv2.imwrite(out_location, img)

        count = count + 1

