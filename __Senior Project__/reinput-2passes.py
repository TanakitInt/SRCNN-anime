# reinput
#
# file to get :
#
# (nX) output/1-bicubic-enhanced.png
# --- OR ---
# (nX) output/denoise/1-bicubic-enhanced-denoised.png

import os
#import cv2
#from glob import glob
#from os import path
from shutil import copyfile

# Get user settings
try:
    settings = open("settings/settings_2-passes-denoise-as-input.txt", "r")
    denoise_as_input = settings.read()
    DENOISE_AS_INPUT = float(denoise_as_input)        #stored in variable

except Exception as e:
    print("Error occured. You might be misconfig the settings, please check the denoise as input settings again.")
    print("Please make sure that denoise as input settings must be 0 or 1 (False or True)." + '\n')
    print("Error! " + str(e) + '\n')

# copy files ---

try:
    # (nX) output/1-bicubic-enhanced.png
    if DENOISE_AS_INPUT == 0:

        original_file = "output/1-bicubic-enhanced.png"
    
    # (nX) output/denoise/1-bicubic-enhanced-denoised.png
    elif DENOISE_AS_INPUT == 1:

        original_file = "output/denoise/1-bicubic-enhanced-denoised.png"

    else:

        print("You might be misconfig the settings, check denoise as input settings again.")
    
    new_file = "input/1.png"

    copyfile(original_file, new_file)

    print("File copied : " + original_file + '\n')
    print("Re-input file copy for \"2 passes\" Done!" + '\n')
    

except Exception as e:
    print("Error! " + str(e) + '\n')

