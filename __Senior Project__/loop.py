import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model, Input, Model
from pathlib import Path
from skimage.metrics import structural_similarity as ssim

def main():

    command = str(input("Input anything to commence IQA (Leave blank for enlargement):"))

    # No input to enlarge images, Any input to test IQA
    if command != "":
        IQA()
        quit()

    # Read file input
    folder_p = Path('input/').rglob('*.png')
    folder_j = Path('input/').rglob('*.jpg')
    files_in = [x for x in folder_p] + [x for x in folder_j]

    print("\nTotal files:", len(files_in), "\n")

    # Load model
    model = load_model('my_model-srcnn-anime-tanakitint.h5')

    # Looping through files
    count = 1

    for i in files_in:

        interpol(str(i), model)
        print("Interpolation Progress: %d/%d" %(count, len(files_in)))
        count += 1

    print("Interpolation Success")


def interpol(file, model):

    DOWNSCALE = 0.5
    UPSCALE = 2

    INPUT_NAME = file
    OUTPUT_NAME = "output/" + str(file)[6:-4]

    # Read image
    img = cv2.imread(INPUT_NAME, cv2.IMREAD_COLOR)

    # Scale down image with bilinear interpolation method ---
    img_down = cv2.resize(img, None, fx=DOWNSCALE, fy=DOWNSCALE, interpolation=cv2.INTER_LINEAR)

    # Enlarge image with basic interpolation method ---
    img_nn = cv2.resize(img_down, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_NEAREST)
    img_bl = cv2.resize(img_down, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_LINEAR)
    img_bc = cv2.resize(img_down, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_CUBIC)

    # Model Prediction ---
    img = cv2.cvtColor(img_bl, cv2.COLOR_BGR2YCrCb)
    shape = img.shape
    Y_img = cv2.resize(img[:, :, 0], (shape[1], shape[0]), cv2.INTER_CUBIC)
    Y = np.zeros((1, img.shape[0], img.shape[1], 1), dtype=float)
    Y[0, :, :, 0] = Y_img.astype(float) / 255.

    # prediction
    pre = model.predict(Y, batch_size=1) * 255.
    pre[pre[:] > 255] = 255
    pre[pre[:] < 0] = 0
    pre = pre.astype(np.uint8)
    img[:, : ,0] = pre[0, :, :, 0]

    # convert from YCrCb to BGR and save image
    img_SRCNN = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)

    # write images
    cv2.imwrite(OUTPUT_NAME + "_nearest.png", img_nn)
    cv2.imwrite(OUTPUT_NAME + "_bilinear.png", img_bl)
    cv2.imwrite(OUTPUT_NAME + "_bicubic.png", img_bc)
    cv2.imwrite(OUTPUT_NAME + "_SRCNN.png", img_SRCNN)


def IQA():

    # Read file input
    folder_p = Path('input/').rglob('*.png')
    folder_j = Path('input/').rglob('*.jpg')
    folder_r = [x for x in folder_p] + [x for x in folder_j]
    folder_nn = Path('output/').rglob('*_nearest.png')
    folder_bl = Path('output/').rglob('*_bilinear.png')
    folder_bc = Path('output/').rglob('*_bicubic.png')
    folder_SRCNN = Path('output/').rglob('*_SRCNN.png')
    folder_waifu2x = Path('output/').rglob('*_waifu2x.png')

    # Sort files
    f_r = sorted([str(x) for x in folder_r])
    f_nn = sorted([str(x) for x in folder_nn])
    f_bl = sorted([str(x) for x in folder_bl])
    f_bc = sorted([str(x) for x in folder_bc])
    f_srcnn = sorted([str(x) for x in folder_SRCNN])
    f_w = sorted([str(x) for x in folder_waifu2x])

    # Integrity Check
    intcheck = [len(f_r), len(f_nn), len(f_bl), len(f_bc), len(f_srcnn), len(f_w)]
    print("Integrity Check: ", intcheck)
    total = max(intcheck)
    print("\nTotal files: ", total, "\n")

    # Export IQA to CSV
    results_nn = open("output_IQA/NN.csv", "w+", encoding = "utf-8")
    results_bl = open("output_IQA/BL.csv", "w+", encoding = "utf-8")
    results_bc = open("output_IQA/BC.csv", "w+", encoding = "utf-8")
    results_srcnn = open("output_IQA/SRCNN.csv", "w+", encoding = "utf-8")
    results_waifu2x = open("output_IQA/WAIFU2X.csv", "w+", encoding = "utf-8")
    results_nn.writelines("PSNR, SSIM\n")
    results_bl.writelines("PSNR, SSIM\n")
    results_bc.writelines("PSNR, SSIM\n")
    results_srcnn.writelines("PSNR, SSIM\n")
    results_waifu2x.writelines("PSNR, SSIM\n")

    # read every single image
    for i in range(0, total):

        REFERENCE = f_r[i]
        NEAREST = f_nn[i]
        BLLINEAR = f_bl[i]
        BICUBIC = f_bc[i]
        SRCNN = f_srcnn[i]
        WAIFU2X = f_w[i]

        ref = cv2.imread(REFERENCE)
        nn = cv2.imread(NEAREST)
        bl = cv2.imread(BLLINEAR)
        bc = cv2.imread(BICUBIC)
        sr = cv2.imread(SRCNN)
        waifu2x = cv2.imread(WAIFU2X)

        refs = ref.shape
        nns = nn.shape
        bls = bl.shape
        bcs = bc.shape
        srs = sr.shape
        waifu2xs = waifu2x.shape
        print("Size Check:", [refs, nns, bls, bcs, srs, waifu2xs])

        # file size detection and Automatic fix with nearest neighbors methods
        if refs != nns or refs != bls or refs != bcs or refs != srs or refs != waifu2xs:
            print("Size error detected. Automatic fix with nearest neighbors method.")

            base = min(refs, nns, bls, bcs, srs, waifu2xs)
            print("Applying base size:", base)
            ref = cv2.resize(ref, dsize=(base[1], base[0]), interpolation = cv2.INTER_NEAREST)
            nn = cv2.resize(nn, dsize=(base[1], base[0]), interpolation = cv2.INTER_NEAREST)
            bl = cv2.resize(bl, dsize=(base[1], base[0]), interpolation = cv2.INTER_NEAREST)
            bc = cv2.resize(bc, dsize=(base[1], base[0]), interpolation = cv2.INTER_NEAREST)
            sr = cv2.resize(sr, dsize=(base[1], base[0]), interpolation = cv2.INTER_NEAREST)
            waifu2x = cv2.resize(waifu2x, dsize=(base[1], base[0]), interpolation = cv2.INTER_NEAREST)

        # calculate score
        scores = []
        scores.append(compare_images(nn, ref))
        scores.append(compare_images(bl, ref))
        scores.append(compare_images(bc, ref))
        scores.append(compare_images(sr, ref))
        scores.append(compare_images(waifu2x, ref))

        # display images as subplots --- 
        # Reference
        fig, axs = plt.subplots(1, 6, figsize=(48, 8))
        axs[0].imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
        axs[0].set_title('Reference')

        # Nearest Neighbor
        axs[1].imshow(cv2.cvtColor(nn, cv2.COLOR_BGR2RGB))
        axs[1].set_title('Nearest Neighbor')
        axs[1].set(xlabel = """PSNR: %f
SSIM: %f""" %(scores[0][0], scores[0][1]))
        results_nn.writelines(str(scores[0][0]) + ", " + str(scores[0][1]) + "\n")

        # Bilinear
        axs[2].imshow(cv2.cvtColor(bl, cv2.COLOR_BGR2RGB))
        axs[2].set_title('Bilinear')
        axs[2].set(xlabel = """PSNR: %f
SSIM: %f""" %(scores[1][0], scores[1][1]))
        results_bl.writelines(str(scores[1][0]) + ", " + str(scores[1][1]) + "\n")

        # Bicubic
        axs[3].imshow(cv2.cvtColor(bc, cv2.COLOR_BGR2RGB))
        axs[3].set_title('Bicubic')
        axs[3].set(xlabel = """PSNR: %f
SSIM: %f""" %(scores[2][0], scores[2][1]))
        results_bc.writelines(str(scores[2][0]) + ", " + str(scores[2][1]) + "\n")

        # SRCNN
        axs[4].imshow(cv2.cvtColor(sr, cv2.COLOR_BGR2RGB))
        axs[4].set_title('SRCNN')
        axs[4].set(xlabel = """PSNR: %f
SSIM: %f""" %(scores[3][0], scores[3][1]))
        results_srcnn.writelines(str(scores[3][0]) + ", " + str(scores[3][1]) + "\n")

        # waifu2x
        axs[5].imshow(cv2.cvtColor(waifu2x, cv2.COLOR_BGR2RGB))
        axs[5].set_title('Waifu2x')
        axs[5].set(xlabel = """PSNR: %f
SSIM: %f""" %(scores[4][0], scores[4][1]))
        results_waifu2x.writelines(str(scores[4][0]) + ", " + str(scores[4][1]) + "\n")

        # remove the x and y ticks
        # for ax in axs:
        #     ax.set_xticks([])
        #     ax.set_yticks([])

        # save in image result
        fig.savefig('output_IQA/%s-IQA.png' %REFERENCE[6:-4])
        plt.close()

        print("IQA Progress: %d/%d" %(i+1, len(f_r)))

    print("IQA Success")

    # close files
    results_nn.close()
    results_bl.close()
    results_bc.close()
    results_srcnn.close()
    results_waifu2x.close()

def psnr(target, ref):

    # assume RGB Image
    target_data = target.astype(float)
    ref_data = ref.astype(float)

    diff = ref_data - target_data
    diff = diff.flatten('C')

    rmse = math.sqrt(np.mean(diff ** 2.))

    return 20 * math.log10(255. / rmse)

# define function that combined all three image quality metrics

def compare_images(target, ref):
    scores = []
    scores.append(psnr(target, ref))
    scores.append(ssim(target, ref, multichannel = True))

    return scores

if __name__ == "__main__":

    main()

