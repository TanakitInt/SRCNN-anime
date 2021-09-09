import os
import cv2
from glob import glob
from os import path

# rename user file name to fixed name ("1.png")
file = "input/1.png"
user_file = "user-input/*"

print("========================" + '\n')
print("Program started.")
print("Your file will be temporary stored at \"input\" folder." + '\n')
print("Manual denoise settings available, please go to \"settings\" folder to set the desired value.")
print("Manual bicubic scale available, please go to \"settings\" folder to set the desired value." + '\n')
print("========================" + '\n')

# get user file name
try:
    for name in glob(user_file):
        
        user_file = str(name)
        print(user_file)

        f = open('settings/user_filename.txt', 'w', encoding="utf-8")
        
        name = name.lower()
        name = name.replace("user-input\\", "")
        #name = name.replace(".png", "")

        f.write(name)
        f.close()

        print("Get user file name!")

        name = ""

except Exception as e:
    print("Error! " + str(e) + '\n')

# remove user old file if new user file exist
if path.exists(file)==True and path.exists(user_file)==True:

    os.remove(file)
    
    path = user_file
    glb = glob(path)

    for image in glb:
        new_path = file
        print("Renaming done!" + '\n')
        e = os.rename(image, new_path)

# if new user file exist and no old file, rename it
elif path.exists(file)==False and path.exists(user_file)==True:

    path = user_file
    glb = glob(path)

    for image in glb:
        new_path = file
        print("Renaming done!" + '\n')
        e = os.rename(image, new_path)

# old file exist but no user file input
elif path.exists(file)==True and path.exists(user_file)==False:

    print("File exist!" + '\n')

# old file doesn't exist and no user file input
elif path.exists(file)==False and path.exists(user_file)==False:

    print("Please input PNG image file!" + '\n')


try:
    # read image
    # convert to color image automatically if grayscale image
    img = cv2.imread(file, cv2.IMREAD_COLOR)
   
    # get dimensions of image
    dimensions = img.shape
        
    # height, width, number of channels in image
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    print("Grayscale image will be converted to color image automatically.")
    print("Image will be convert to RGB color system, PNG format automatically at the outputs.")
    print("If input is not an image, an error will occured.")
    print("")
    print("Image Dimension    : ", dimensions)
    print("Image Height       : ", height)
    print("Image Width        : ", width)
    print("Number of Channels : ", channels)
    print("")

    print("Image Pixels : " + str(height * width))

    if height * width > 12250000:
        # 3500 * 3500 Image
        print("Image for \"Enhancement only\" exceed computational time limit! (3500 * 3500)" + '\n' + \
             "Width = " + str(width) + '\n' + \
             "Height = " + str(height) + '\n')
        
    elif height * width > 3062500:
        # 1750 * 1750 Image
        print("Image for \"Enlargement and Enhancement\" exceed computational time limit! (1750 * 1750)" + '\n' + \
             "Width = " + str(width) + '\n' + \
             "Height = " + str(height) + '\n')

    elif height * width >= 1:
        # higher than 1 * 1 Image
        print("Dimensions OK!" + '\n')
        
    #elif height * width >= 1:
    #    # super low resolution
    #    print("Dimensions too low (<128 * <128) Output image might not be satisfied." + '\n')

except Exception as e:
    print("Error! " + str(e) + '\n')
    
