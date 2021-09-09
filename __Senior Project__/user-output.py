# file to get :
#
# ENLARGEMENT / ENHANCEMENT ---
# (1X) output/1-enhanced.png
# (nX) output/1-bicubic.png
# (nX) output/1-bicubic-enhanced.png
# 
# DENOISE ---
# (1X) output/denoise/1-enhanced-denoised.png
# (nX) output/denoise/1-bicubic-enhanced-denoised.png
#
# REINPUT-DENOISE-FINAL_DENOISE ---
# (nX - reinput) output/denoise/1-enhanced-denoised-final.png
#
# REINPUT-UPDOWN ---
# (nX - 2X - 0.5X) output/1-bicubic-enhanced-downscaled.png
# (nX - 2X - 0.5X) output/denoise/1-bicubic-enhanced-downscaled-denoised.png

import os
import cv2
from glob import glob
from os import path
from shutil import copyfile

# # remove file if old file exist ---
# old_file = "user-output/*.png"

# try:
#     for name in glob(old_file):
        
#         os.remove(name)
#         print("Old file removed.")

# except Exception as e:
#     print("Error! " + str(e) + '\n')

# Get user file name ---

f = open("settings/user_filename.txt", "r", encoding="utf-8")
user_filename = f.read()
USER_FILENAME= str(user_filename)              #stored in variable

print("User file name : " + USER_FILENAME + '\n')

# Get Bicubic scale ---

try:
    settings = open("settings/settings_bicubic.txt", "r")
    bicubic_scale = settings.read()
    BICUBIC_SCALE = float(bicubic_scale)        #stored in variable

except Exception as e:
    print("Error occured. You might be misconfig the settings, please check the bicubic settings again.")
    print("Please make sure that bicubic setting must not a zero or negative numbers." + '\n')
    print("Error! " + str(e) + '\n')

# Get 2 Passes settings ---

try:
    settings = open("settings/settings_2-passes.txt", "r")
    two_pass_setting = settings.read()
    TWO_PASS_SETTING = int(two_pass_setting)    #stored in variable

except Exception as e:
    print("Error occured. You might be misconfig the settings, please check the 2 passes settings again.")
    print("Please make sure that 2 passes settings must be 0 or 1 (False or True)." + '\n')
    print("Error! " + str(e) + '\n')

# Get UPDOWN settings ---

try:
    settings = open("settings/settings_updown.txt", "r")
    up_down_setting = settings.read()
    UP_DOWN_SETTING = int(up_down_setting)      #stored in variable

except Exception as e:
    print("Error occured. You might be misconfig the settings, please check the updown settings again.")
    print("Please make sure that updown settings must be 0 or 1 (False or True)." + '\n')
    print("Error! " + str(e) + '\n')

# Copy files ---

try:
    # (1X) output/1-enhanced.png
    if TWO_PASS_SETTING == 0:

        new_file_1 = "user-output/" + USER_FILENAME + "_srcnn-anime-1x-enhanced.png"
        
    elif TWO_PASS_SETTING == 1:

        new_file_1 = "user-output/" + USER_FILENAME + "_srcnn-anime_2-PASSES_" + str(BICUBIC_SCALE) + "x-enhanced.png"

    else:

        print("You might be misconfig the settings, check 2 passes settings again.")

    copyfile("output/1-enhanced.png", new_file_1)
    print("File copied : " + new_file_1)

except Exception as e:
    print("Error! " + str(e) + '\n')

try:
    # (nX) output/1-bicubic.png
    if UP_DOWN_SETTING == 0:

        new_file_2 = "user-output/" + USER_FILENAME + "_srcnn-anime-bicubic-" + str(BICUBIC_SCALE) + "x.png"
        
        
    elif UP_DOWN_SETTING == 1:

        new_file_2 = "user-output/" + USER_FILENAME + "_srcnn-anime_UPDOWN-2x_bicubic-" + str(BICUBIC_SCALE) + "x.png"

    else:

        print("You might be misconfig the settings, check updown settings again.")

    copyfile("output/1-bicubic.png", new_file_2)
    print("File copied : " + new_file_2)

except Exception as e:
    print("Error! " + str(e) + '\n')

try:  
    # (nX) output/1-bicubic-enhanced.png
    if UP_DOWN_SETTING == 0:

        new_file_3 = "user-output/" + USER_FILENAME + "_srcnn-anime-bicubic-" + str(BICUBIC_SCALE) + "x-enhanced.png"
        
        
    elif UP_DOWN_SETTING == 1:

        new_file_3 = "user-output/" + USER_FILENAME + "_srcnn-anime_UPDOWN-2x_bicubic-" + str(BICUBIC_SCALE) + "x-enhanced.png"

    else:

        print("You might be misconfig the settings, check updown settings again.")

    copyfile("output/1-bicubic-enhanced.png", new_file_3)
    print("File copied : " + new_file_3)

except Exception as e:
    print("Error! " + str(e) + '\n')

try: 
    # (1X) output/denoise/1-enhanced-denoised.png
    if TWO_PASS_SETTING == 0:

        new_file_4 = "user-output/" + USER_FILENAME + "_srcnn-anime-1x-enhanced-denoised.png"

    elif TWO_PASS_SETTING == 1:

        new_file_4 = "user-output/" + USER_FILENAME + "_srcnn-anime_2-PASSES_" + str(BICUBIC_SCALE) + "x-enhanced-denoised.png"

    else:

        print("You might be misconfig the settings, check 2 passes settings again.")

    copyfile("output/denoise/1-enhanced-denoised.png", new_file_4)
    print("File copied : " + new_file_4)

except Exception as e:
    print("Error! " + str(e) + '\n')

try: 
    # (nX) output/denoise/1-bicubic-enhanced-denoised.png
    new_file_5 = "user-output/" + USER_FILENAME + "_srcnn-anime-bicubic-" + str(BICUBIC_SCALE) + "x-enhanced-denoised.png"
    copyfile("output/denoise/1-bicubic-enhanced-denoised.png", new_file_5)
    print("File copied : " + new_file_5)

except Exception as e:
    print("Error! " + str(e) + '\n')

try:
    # (nX - reinput) output/denoise/1-enhanced-denoised-final.png
    new_file_10 = "user-output/" + USER_FILENAME + "_srcnn-anime_2-PASSES_" + str(BICUBIC_SCALE) + "x-enhanced-denoised-final.png"
    copyfile("output/denoise/1-enhanced-denoised-final.png", new_file_10)
    print("File copied : " + new_file_10)

except Exception as e:
    print("Error! " + str(e) + '\n')

try:
    # (nX - 2X - 0.5X) output/1-bicubic-enhanced-downscaled.png
    new_file_20 = "user-output/" + USER_FILENAME + "_srcnn-anime_UPDOWN-2x_" + str(BICUBIC_SCALE) + "x-enhanced-downscaled.png"
    copyfile("output/1-bicubic-enhanced-downscaled.png", new_file_20)
    print("File copied : " + new_file_20)

except Exception as e:
    print("Error! " + str(e) + '\n')

try:
    # (nX - 2X - 0.5X) output/denoise/1-bicubic-enhanced-downscaled-denoised.png
    new_file_21 = "user-output/" + USER_FILENAME + "_srcnn-anime_UPDOWN-2x_" + str(BICUBIC_SCALE) + "x-enhanced-downscaled-denoised.png"
    copyfile("output/denoise/1-bicubic-enhanced-downscaled-denoised.png", new_file_21)
    print("File copied : " + new_file_21)

except Exception as e:
    print("Error! " + str(e) + '\n')

    
print("Files Copy Done!" + '\n')

print("========================" + '\n')
print("All process done! check your output at \"user-output\" folder.")
print("Ready to input new file." + '\n')
print("========================" + '\n')

