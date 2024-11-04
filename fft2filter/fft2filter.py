import argparse

import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(prog = "fft2filter",
                                     description = "A program that filters images using fft.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("-t", "--ftype", default = "high", help = "Low-pass(low) or High-pass(high) filter")
    parser.add_argument("-v", "--verbose", type = int, default = 0, help = "0 - show nothing; 1 - show input and output image; 2 - show everything")
    #verbose
    args = parser.parse_args()
    
    #image should have 1 channel
    img = cv2.imread(args.input, cv2.IMREAD_UNCHANGED)
    print(img.shape, img.dtype, np.min(img), np.max(img))

    img_dft = cv2.dft(img.astype(np.float32), flags = cv2.DFT_COMPLEX_OUTPUT)

    img_dft_shift = np.fft.fftshift(img_dft)

    r_div = 15
    if args.ftype == "high" :
    #High-pass
        mask = np.ones(img.shape, dtype = np.uint8)
        mask = cv2.circle(mask, (int(img.shape[1] / 2), int(img.shape[0] / 2)), int(img.shape[0] / r_div), 0, -1) 
    elif args.ftype == "low":
    #Low-pass
        mask = np.zeros(img.shape, dtype = np.uint8)
        mask = cv2.circle(mask, (int(img.shape[1] / 2), int(img.shape[0] / 2)), int(img.shape[0] / r_div), 1, -1) 
    else:
        print("Please specify the correct filter type.")
        return

    img_dft_shift_filtered = img_dft_shift * mask[..., np.newaxis]

    img_dft_ishift_filtered = np.fft.ifftshift(img_dft_shift_filtered)

    img_filtered = cv2.idft(img_dft_ishift_filtered)
    img_filtered = cv2.magnitude(img_filtered[..., 0], img_filtered[..., 1])
    print(img_filtered.shape, img_filtered.dtype, np.min(img_filtered), np.max(img_filtered))


    if args.verbose == 1:
        fig, (ax0, ax5) = plt.subplots(1, 2)
        fig.canvas.manager.set_window_title('FFT')
        ax0.imshow(img, cmap = "grey")
        ax5.imshow(img_filtered, cmap = "grey")

        plt.show()
    elif args.verbose == 2:
        dft_mag = cv2.magnitude(img_dft[..., 0], img_dft[..., 1])
        dft_mag2show = 20 * np.log(dft_mag)

        dft_shift_mag = cv2.magnitude(img_dft_shift[..., 0], img_dft_shift[..., 1])
        dft_shift_mag2show = 20 * np.log(dft_shift_mag)

        dft_shift_filtered_mag = cv2.magnitude(img_dft_shift_filtered[..., 0], img_dft_shift_filtered[..., 1])
        dft_shift_filtered_mag2show = 20 * np.log(np.where(dft_shift_filtered_mag > 0, dft_shift_filtered_mag, 0.1))

        dft_ishift_filtered_mag = cv2.magnitude(img_dft_ishift_filtered[..., 0], img_dft_ishift_filtered[..., 1])
        dft_ishift_filtered_mag2show = 20 * np.log(np.where(dft_ishift_filtered_mag > 0, dft_ishift_filtered_mag, 0.1))

        fig, (ax0, ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 6)
        fig.canvas.manager.set_window_title('FFT')
        ax0.imshow(img, cmap = "grey")
        ax1.imshow(dft_mag2show, cmap = "grey")
        ax2.imshow(dft_shift_mag2show, cmap = "grey")
        ax3.imshow(dft_shift_filtered_mag2show, cmap = "grey")
        ax4.imshow(dft_ishift_filtered_mag2show, cmap = "grey")
        ax5.imshow(img_filtered, cmap = "grey")
        plt.show()

    #cv2.normalize(img_filtered, img_filtered, 0, 2 ** 16 - 1, cv2.NORM_MINMAX)
    #cv2.imwrite(args.output, img_filtered.astype(np.uint16))
    cv2.normalize(img_filtered, img_filtered, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite(args.output, img_filtered.astype(np.uint8))

if __name__ == "__main__":
    main()


