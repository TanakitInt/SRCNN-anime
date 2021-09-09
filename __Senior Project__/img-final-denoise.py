import cv2
from matplotlib import pyplot as plt

INPUT_NAME = "output/denoise/1-enhanced-denoised.png"
OUTPUT_NAME = "output/denoise/1-enhanced-denoised-final.png"

# get filter settings from text file ---

# default "FINAL" fastNlMeans filter is 14
# default "FINAL" bilateral filter is 100
# default "FINAL" medianBlur filter is 1

try:
    f1 = open("settings/settings_final_fastNlMeans_filter.txt", "r")
    final_fastNlMeans_filter = f1.read()
    FINAL_FASTNLMEANS_FILTER = int(final_fastNlMeans_filter)            #stored in variable

    f2 = open("settings/settings_final_bilateral_filter.txt", "r")
    final_bilateral_filter = f2.read()
    FINAL_BILATERAL_FILTER = int(final_bilateral_filter)                #stored in variable

    f3 = open("settings/settings_final_medianblur_filter.txt", "r")
    final_medianblur_filter = f3.read()
    FINAL_MEDIANBLUR_FILTER = int(final_medianblur_filter)              #stored in variable
    
except Exception as e:
        print("Error occured. You might be misconfig the settings, please check the denoise settings again. Some filter (medianblur) may require only odd numbers.")
        print("Please make sure that all filter settings must be zero or interger." + '\n')
        print("Error! " + str(e) + '\n')


try:
    
    # read image
    img = cv2.imread(INPUT_NAME)

    print("FINAL_FASTNLMEANS_FILTER : " + str(FINAL_FASTNLMEANS_FILTER))
    print("FINAL_BILATERAL_FILTER : " + str(FINAL_BILATERAL_FILTER))
    print("FINAL_MEDIANBLUR_FILTER : " + str(FINAL_MEDIANBLUR_FILTER))

    # denoise
    denoise_0 = cv2.fastNlMeansDenoisingColored(img, dst=None, h=FINAL_FASTNLMEANS_FILTER, hColor=FINAL_FASTNLMEANS_FILTER, templateWindowSize=5, searchWindowSize=15)
    denoise_1 = cv2.bilateralFilter(denoise_0, 3, FINAL_BILATERAL_FILTER, FINAL_BILATERAL_FILTER, cv2.BORDER_DEFAULT)
    denoise_2 = cv2.medianBlur(denoise_1, FINAL_MEDIANBLUR_FILTER)

    # save denoise image
    cv2.imwrite(OUTPUT_NAME, denoise_2)

    print("Saved final denoised image...")

    # for denoise comparison
    # display images as subplots
    fig, axs = plt.subplots(1, 2, figsize=(16, 8))

    axs[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axs[0].set_title('Enhanced Denoised')
    axs[1].imshow(cv2.cvtColor(denoise_2, cv2.COLOR_BGR2RGB))
    axs[1].set_title('Enhanced Denoised Final')

    # remove the x and y ticks
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])

    # save in image result
    print('Saving result for "FINAL" image denoise comparison in image...' + '\n')

    fig.savefig('output/denoise/compare-denoise-final.png') 
    plt.close()

    print('Saving Done.' + '\n')

except Exception as e:
        print("Error! " + str(e) + '\n')

