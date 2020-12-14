import cv2

def bicubic():

    BICUBIC_SCALE = 0.5

    INPUT_NAME = "output/1-bicubic-enhanced.png"
    OUTPUT_NAME = "output/1-bicubic-enhanced-downscaled.png"

    # Read image
    img = cv2.imread(INPUT_NAME, cv2.IMREAD_COLOR)

    # Enlarge image with Bicubic interpolation method
    img = cv2.resize(img, None, fx=BICUBIC_SCALE, fy=BICUBIC_SCALE, interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(OUTPUT_NAME, img)

    # print success!
    print("Bicubic enlargement with factor " + str(BICUBIC_SCALE) + " success!")

bicubic()

