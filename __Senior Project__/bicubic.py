import cv2

def bicubic():

    # get scale settings from text file ---

    # default bicubic scale is 2

    try:
        settings = open("settings/settings_bicubic.txt", "r")
        bicubic_scale = settings.read()
        BICUBIC_SCALE = float(bicubic_scale)        #stored in variable

    except Exception as e:
        print("Error occured. You might be misconfig the settings, please check the bicubic settings again.")
        print("Please make sure that bicubic setting must not a zero or negative numbers." + '\n')
        print("Error! " + str(e) + '\n')

    INPUT_NAME = "input/1.png"
    OUTPUT_NAME = "output/1-bicubic.png"

    # Read image
    img = cv2.imread(INPUT_NAME, cv2.IMREAD_COLOR)

    # Enlarge image with Bicubic interpolation method
    img = cv2.resize(img, None, fx=BICUBIC_SCALE, fy=BICUBIC_SCALE, interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(OUTPUT_NAME, img)

    # print success!
    print("Bicubic enlargement with factor " + str(BICUBIC_SCALE) + " success!")

bicubic()

