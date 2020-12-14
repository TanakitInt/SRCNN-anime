# import specific necessary packages

from skimage.metrics import structural_similarity as ssim
from matplotlib import pyplot as plt
import cv2
import numpy as np
import math
import os
import glob

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

def ref_test():

    print("This is a manual image reference test (IQA)")
    print("")
    print("Please make sure that all image extension has been renamed to PNG and placed at each folder.")
    print("Please enter the image configuration below : ")

    reference_name = str(input("Reference image (1-ref) : "))
    secondImage_name = str(input("Second image (2) : "))
    thirdImage_name = str(input("Third image (3) : "))
    fourthImage_name = str(input("Fourth image (4) : "))

    print("")

    dir_1 = 'in-test/1-ref/*.png'
    dir_2 = 'in-test/2/*.png'
    dir_3 = 'in-test/3/*.png'
    dir_4 = 'in-test/4/*.png'

    REFERENCE = glob.glob(dir_1)
    for i in REFERENCE:
        REFERENCE = str(i)

    COMPARE_1 = glob.glob(dir_2)
    for i in COMPARE_1:
        COMPARE_1 = str(i)

    COMPARE_2 = glob.glob(dir_3)
    for i in COMPARE_2:
        COMPARE_2 = str(i)

    COMPARE_3 = glob.glob(dir_4)
    for i in COMPARE_3:
        COMPARE_3 = str(i)

    # open target and reference images
    ref = cv2.imread(REFERENCE)
    compare_1 = cv2.imread(COMPARE_1)  
    compare_2 = cv2.imread(COMPARE_2)      
    compare_3 = cv2.imread(COMPARE_3)

    # calculate score
    scores = []
    scores.append(compare_images(compare_1, ref))
    scores.append(compare_images(compare_2, ref))
    scores.append(compare_images(compare_3, ref))

    # print image quality assessment
    assessment_compare_1 = "> Image quality assessment (IQA) for manual reference." + '\n' + \
        "For 2 vs Reference ---" + '\n' + \
        "Target : " + COMPARE_1 + '\n' + \
        "Reference : " + REFERENCE + '\n' + \
        "PSNR (Peak signal-to-noise ratio) : " + str(scores[0][0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[0][1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[0][2]) + '\n'

    assessment_compare_2 = '\n' + \
        "For 3 vs Reference ---" + '\n' + \
        "Target : " + COMPARE_2 + '\n' + \
        "Reference : " + REFERENCE + '\n' + \
        "PSNR (Peak signal-to-noise ratio) : " + str(scores[1][0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[1][1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[1][2]) + '\n'

    assessment_compare_3 = '\n' + \
        "For 4 vs Reference ---" + '\n' + \
        "Target : " + COMPARE_3 + '\n' + \
        "Reference : " + REFERENCE + '\n' + \
        "PSNR (Peak signal-to-noise ratio) : " + str(scores[2][0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[2][1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[2][2]) + '\n'

    print(assessment_compare_1)
    print(assessment_compare_2)
    print(assessment_compare_3)
        
    # display images as subplots
    fig, axs = plt.subplots(1, 4, figsize=(32, 8))
    axs[0].imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
    axs[0].set_title(reference_name)
    axs[1].imshow(cv2.cvtColor(compare_1, cv2.COLOR_BGR2RGB))
    axs[1].set_title(secondImage_name)
    axs[1].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[0][0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[0][1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[0][2]) + '\n')
    axs[2].imshow(cv2.cvtColor(compare_2, cv2.COLOR_BGR2RGB))
    axs[2].set_title(thirdImage_name)
    axs[2].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[1][0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[1][1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[1][2]) + '\n')
    axs[3].imshow(cv2.cvtColor(compare_3, cv2.COLOR_BGR2RGB))
    axs[3].set_title(fourthImage_name)
    axs[3].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[2][0]) + '\n' + \
        "MSE (Mean squared error) : " + str(scores[2][1]) + '\n' + \
        "SSIM (Structural similarity) : " + str(scores[2][2]) + '\n')

    # remove the x and y ticks
    # for ax in axs:
    #     ax.set_xticks([])
    #     ax.set_yticks([])

    # save in image result
    print('Saving result for IQA manual reference in image...' + '\n')

    fig.savefig('out-fig/manual-reference-test.png') 
    plt.close()

    print('Saving Done.' + '\n')


if __name__ == "__main__":

    ref_test()

