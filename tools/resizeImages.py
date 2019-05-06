import glob

import cv2.cv2 as cv2

if __name__ == "__main__":

    directory = "../positive_images"
    desired_resolution = (80, 30)

    files = glob.glob('{0}/*.png'.format(directory))
    for file in files:
        image = cv2.imread(file)
        resized_image = cv2.resize(image, desired_resolution)
        cv2.imwrite(file, resized_image)
        print("Resized " + file + " from " + str(image.shape) + " to " + str(resized_image.shape))
