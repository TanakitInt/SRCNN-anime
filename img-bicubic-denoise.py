import cv2
import numpy as np
import math
import os
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim

######## for denoise IQA comparison function ########

# define function for Peak signal-to-noise ratio (PSNR)

def psnr(target, ref):

    # assume RGB Image
    target_data = target.astype(float)
    ref_data = ref.astype(float)

    diff = ref_data - target_data
    diff = diff.flatten('C')

    rmse = math.sqrt(np.mean(diff ** 2.))

    return 20 * math.log10(255. / rmse)

# define function for mean square error (MSE)

def mse(target, ref):

    # MSE is the sum of the squared difference between the two images

    err = np.sum((target.astype('float') - ref.astype('float')) ** 2)
    err /= float(target.shape[0] * target.shape[1])
    
    return err

# define function that combined all three image quality metrics

def compare_images(target, ref):
    scores = []
    scores.append(psnr(target, ref))
    scores.append(mse(target, ref))
    scores.append(ssim(target, ref, multichannel = True))

    return scores


######## for denoising function ########

#INPUT_NAME = "output/1-enhanced.png"
#OUTPUT_NAME = "output/denoise/1-enhanced-denoised.png"
#REFERECE = "input/1.png"

INPUT_NAME = "output/1-bicubic-enhanced.png"
OUTPUT_NAME = "output/denoise/1-bicubic-enhanced-denoised.png"
REFERECE = "output/1-bicubic.png"

reference = REFERECE
reference = cv2.imread(reference)

# get filter settings from text file ---

# default fastNlMeans_filter is 7
# default bilateral_filter is 50

try:
    f1 = open("settings/settings_fastNlMeans_filter.txt", "r")
    fastNlMeans_filter = f1.read()
    FASTNLMEANS_FILTER = int(fastNlMeans_filter)        #stored in variable

    f2 = open("settings/settings_bilateral_filter.txt", "r")
    bilateral_filter = f2.read()
    BILATERAL_FILTER = int(bilateral_filter)            #stored in variable

except Exception as e:
        print("Error occured. You might be misconfig the settings, please check the denoise settings again. Some filter (medianblur) may require only odd numbers.")
        print("Please make sure that all filter settings must be zero or interger." + '\n')
        print("Error! " + str(e) + '\n')


try:

    # read image
    img = cv2.imread(INPUT_NAME)

    print("FASTNLMEANS_FILTER : " + str(FASTNLMEANS_FILTER))
    print("BILATERAL_FILTER : " + str(BILATERAL_FILTER))

    # denoise
    denoise_0 = cv2.fastNlMeansDenoisingColored(img, dst=None, h=FASTNLMEANS_FILTER, hColor=FASTNLMEANS_FILTER, templateWindowSize=3, searchWindowSize=9)
    denoise_1 = cv2.bilateralFilter(denoise_0, 3, BILATERAL_FILTER, BILATERAL_FILTER, cv2.BORDER_DEFAULT)
    denoise_2 = denoise_1   #add more filter if available

    # save denoise image
    cv2.imwrite(OUTPUT_NAME, denoise_2)

    print("Saved denoised image...")

    # for denoise comparison ----

    # open target and reference images
    target = cv2.imread(OUTPUT_NAME)
    ref = cv2.imread(REFERECE)
    
    # calculate score
    scores = compare_images(target, ref)

    # print image quality assessment
    assessment = "> Image quality assessment (IQA) for denoising (Bicubic *x)" + '\n' + \
        "Target : " + OUTPUT_NAME + '\n' + \
        "Reference : " + REFERECE + '\n' + \
        "PSNR (Peak signal-to-noise ratio) : " + str(scores[0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[2]) + '\n'

    print(assessment)


    # display images as subplots
    fig, axs = plt.subplots(1, 2, figsize=(16, 8))

    axs[0].imshow(cv2.cvtColor(reference, cv2.COLOR_BGR2RGB))
    axs[0].set_title('Bicubic')
    axs[1].imshow(cv2.cvtColor(denoise_2, cv2.COLOR_BGR2RGB))
    axs[1].set_title('Bicubic Enhanced Denoised')
    axs[1].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2]) + '\n')

    # remove the x and y ticks
    # for ax in axs:
    #     ax.set_xticks([])
    #     ax.set_yticks([])

    # save in image result
    print('Saving result for scaled bicubic image denoise comparison in image...' + '\n')

    fig.savefig('output/denoise/compare-bicubic-denoise.png') 
    plt.close()

    print('Saving Done.' + '\n')

except Exception as e:
        print("Error! " + str(e) + '\n')

