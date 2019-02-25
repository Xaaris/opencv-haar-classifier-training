import glob

import cv2.cv2 as cv2

if __name__ == "__main__":
    path_to_xml_classifier_file = "../classifier/cascade.xml"
    path_to_test_images = "../../Hauptprojekt/debugImages/found_vehicles/"

    files = glob.glob('{0}/*.png'.format(path_to_test_images))
    for file in files:
        image = cv2.imread(file)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        classifier = cv2.CascadeClassifier(path_to_xml_classifier_file)

        lps = classifier.detectMultiScale(gray_image)
        for (x, y, w, h) in lps:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('img', image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
