# import specific necessary packages

from skimage.metrics import structural_similarity as ssim
from matplotlib import pyplot as plt
import cv2
import numpy as np
import math
import os

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

def iqa_enhancement():

    try:
        # for image enhancement only
        TARGET = 'output/1-enhanced.png'
        REFERENCE = 'input/1.png'

        # open target and reference images
        target = cv2.imread(TARGET)
        ref = cv2.imread(REFERENCE)

        # calculate score
        scores = compare_images(target, ref)

        # print image quality assessment
        assessment = "> Image quality assessment (IQA) for enhancement only" + '\n' + \
            "Target : " + TARGET + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2]) + '\n'

        print(assessment)

        # display images as subplots
        fig, axs = plt.subplots(1, 2, figsize=(16, 8))
        axs[0].imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
        axs[0].set_title('Original')
        axs[1].imshow(cv2.cvtColor(target, cv2.COLOR_BGR2RGB))
        axs[1].set_title('Enhanced')
        axs[1].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2]) + '\n')

        # remove the x and y ticks
        # for ax in axs:
        #     ax.set_xticks([])
        #     ax.set_yticks([])

        # save in image result
        print('Saving result for IQA for enhancement only in image...' + '\n')

        fig.savefig('output/IQA-enhancement.png') 
        plt.close()

        print('Saving Done.' + '\n')

    except Exception as e:
        print("Skipping test.")
        print("Error! " + str(e) + '\n')


def iqa_enlargement():

    try:
        # for image enlargement and enhancement
        TARGET = 'output/1-bicubic-enhanced.png'
        REFERENCE = 'output/1-bicubic.png'

        # open target and reference images
        target = cv2.imread(TARGET)
        ref = cv2.imread(REFERENCE)

        # calculate score
        scores = compare_images(target, ref)

        # print image quality assessment
        assessment = "> Image quality assessment (IQA) for enlargement and enhancement" + '\n' + \
            "Target : " + TARGET + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2]) + '\n'

        print(assessment)
        
        # display images as subplots
        fig, axs = plt.subplots(1, 2, figsize=(16, 8))
        axs[0].imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
        axs[0].set_title('Bicubic')
        axs[1].imshow(cv2.cvtColor(target, cv2.COLOR_BGR2RGB))
        axs[1].set_title('Bicubic Enhanced')
        axs[1].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2]) + '\n')

        # remove the x and y ticks
        # for ax in axs:
        #     ax.set_xticks([])
        #     ax.set_yticks([])

        # save in image result
        print('Saving result for IQA for enlargement and enhancement in image...' + '\n')

        fig.savefig('output/IQA-enlargement-enhancement.png') 
        plt.close()

        print('Saving Done.' + '\n')

    except Exception as e:
        print("Skipping test.")
        print("Error! " + str(e) + '\n')


def iqa_original_compare():

    try:
        # for degraded vs srcnn
        REFERENCE = 'input/1-ref.png'
        DEGRADED = 'input/1.png'
        SRCNN = 'output/1-enhanced.png'

        # open target and reference images
        srcnn = cv2.imread(SRCNN)
        degraded = cv2.imread(DEGRADED)
        ref = cv2.imread(REFERENCE)

        # calculate score
        scores = []
        scores.append(compare_images(degraded, ref))
        scores.append(compare_images(srcnn, ref))

        # print image quality assessment
        assessment_degraded = "> Image quality assessment (IQA) for degraded and SRCNN" + '\n' + \
            "For Original (Degraded) image vs Reference ---" + '\n' + \
            "Target : " + DEGRADED + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[0][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[0][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[0][2]) + '\n'

        assessment_srcnn = '\n' + \
            "For SRCNN vs Reference ---" + '\n' + \
            "Target : " + SRCNN + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[1][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[1][2]) + '\n'

        print(assessment_degraded)
        print(assessment_srcnn)
        
        # display images as subplots
        fig, axs = plt.subplots(1, 3, figsize=(24, 8))
        axs[0].imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
        axs[0].set_title('Reference')
        #axs[0].set_title('Reference - Bicubic 2x')
        axs[1].imshow(cv2.cvtColor(degraded, cv2.COLOR_BGR2RGB))
        axs[1].set_title('Original (Degraded)')
        #axs[1].set_title('1 Pass')
        axs[1].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[0][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[0][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[0][2]) + '\n')
        axs[2].imshow(cv2.cvtColor(srcnn, cv2.COLOR_BGR2RGB))
        axs[2].set_title('SRCNN')
        #axs[2].set_title('2 Passes')
        axs[2].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[1][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[1][2]) + '\n')

        # remove the x and y ticks
        # for ax in axs:
        #     ax.set_xticks([])
        #     ax.set_yticks([])

        # save in image result
        print('Saving result for IQA for Original (Degraded) vs SRCNN in image...' + '\n')

        fig.savefig('output/IQA-original-compare.png') 
        plt.close()

        print('Saving Done.' + '\n')

    except Exception as e:
        print("No reference file!, Skipping reference test.")
        print("Error! " + str(e) + '\n')


def iqa_waifu2x_compare():

    try:
        # for waifu2x vs srcnn
        REFERENCE = 'input/1-ref.png'
        DEGRADED = 'input/1.png'
        SRCNN = 'output/1-enhanced.png'
        WAIFU2X = 'input/1-waifu2x.png'

        # open target and reference images
        srcnn = cv2.imread(SRCNN)
        degraded = cv2.imread(DEGRADED)
        ref = cv2.imread(REFERENCE)
        waifu2x = cv2.imread(WAIFU2X)

        # calculate score
        scores = []
        scores.append(compare_images(degraded, ref))
        scores.append(compare_images(srcnn, ref))
        scores.append(compare_images(waifu2x, ref))

        # print image quality assessment
        assessment_degraded = "> Image quality assessment (IQA) for degraded, SRCNN and waifu2x" + '\n' + \
            "For Original (Degraded) image vs Reference ---" + '\n' + \
            "Target : " + DEGRADED + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[0][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[0][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[0][2]) + '\n'

        assessment_srcnn = '\n' + \
            "For SRCNN vs Reference ---" + '\n' + \
            "Target : " + SRCNN + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[1][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[1][2]) + '\n'

        assessment_waifu2x = '\n' + \
            "For waifu2x vs Reference ---" + '\n' + \
            "Target : " + WAIFU2X + '\n' + \
            "Reference : " + REFERENCE + '\n' + \
            "PSNR (Peak signal-to-noise ratio) : " + str(scores[2][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[2][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2][2]) + '\n'

        print(assessment_degraded)
        print(assessment_srcnn)
        print(assessment_waifu2x)
        
        # display images as subplots
        fig, axs = plt.subplots(1, 4, figsize=(32, 8))
        axs[0].imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
        axs[0].set_title('Reference')
        axs[1].imshow(cv2.cvtColor(degraded, cv2.COLOR_BGR2RGB))
        axs[1].set_title('Original (Degraded)')
        axs[1].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[0][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[0][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[0][2]) + '\n')
        axs[2].imshow(cv2.cvtColor(srcnn, cv2.COLOR_BGR2RGB))
        axs[2].set_title('SRCNN')
        axs[2].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[1][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[1][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[1][2]) + '\n')
        axs[3].imshow(cv2.cvtColor(waifu2x, cv2.COLOR_BGR2RGB))
        axs[3].set_title('waifu2x')
        axs[3].set(xlabel = "PSNR (Peak signal-to-noise ratio) : " + str(scores[2][0]) + '\n' + \
            "MSE (Mean squared error) : " + str(scores[2][1]) + '\n' + \
            "SSIM (Structural similarity) : " + str(scores[2][2]) + '\n')

        # remove the x and y ticks
        # for ax in axs:
        #     ax.set_xticks([])
        #     ax.set_yticks([])

        # save in image result
        print('Saving result for IQA for Original (Degraded) vs SRCNN vs waifu2x in image...' + '\n')

        fig.savefig('output/IQA-waifu2x-compare.png') 
        plt.close()

        print('Saving Done.' + '\n')

    except Exception as e:
        print("No waifu2x reference file!, Skipping waifu2x reference test.")
        print("Error! " + str(e) + '\n')


if __name__ == "__main__":

    iqa_enhancement()
    iqa_enlargement()

    # for having reference
    iqa_original_compare()

    # for having reference and waifu2x
    iqa_waifu2x_compare()

