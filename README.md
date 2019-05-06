# Train your own OpenCV Haar classifier

This repo includes a trained classifier to detect european license plates.
It is based on the a repo by mrnugget which can be found [here](https://github.com/mrnugget/opencv-haar-classifier-training).

**Important**: This guide assumes you work with OpenCV 2.4.x or 3.4.x and a recent macOS version.
The `opencv_createsamples` comand has not been ported to openCV 4.x as of this writing.

This repository aims to provide tools and information on training your own
OpenCV Haar classifier.  Use it in conjunction with this blog post: [Train your own OpenCV Haar
classifier](http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html).



## Instructions

1. Install OpenCV 3

        brew install opencv@3

    And add it to your PATH
        
        echo 'export PATH="/usr/local/opt/opencv@3/bin:$PATH"' >> ~/.bash_profile
        
   Now restart your Terminal.

2. Clone this repository

        git clone git@github.com:Xaaris/opencv-haar-classifier-training.git

3. Put your positive images in the `./positive_images` folder and create a list
of them:

        find ./positive_images -iname "*.png" > positives.txt
   All images should have the same size (80 x 30 px in my case). 
   You can adapt the `resizeImages.py` script to do so.
    
4. Put the negative images in the `./negative_images` folder and create a list of them:

        find ./negative_images -iname "*.png" > negatives.txt
   All images should have the same size (1920 x 1080 px in my case). 
   You can again adapt the `resizeImages.py` script to do so.
   
5. Create positive samples with the `bin/createsamples.pl` script and save them
to the `./samples` folder:

        perl bin/createsamples.pl positives.txt negatives.txt samples 2000\
        "opencv_createsamples -bgcolor 0 -bgthresh 0 -maxxangle 1.1\
        -maxyangle 1.1 -maxzangle 0.0 -maxidev 10 -w 80 -h 30"
        
    Add `-show` in the end (before the closing ") to see what's going on

6. Use `tools/mergevec.py` to merge the samples in `./samples` into one .vec file called `samples.vec`:

        python ./tools/mergevec.py -v samples/ -o samples.vec

   Note: If you get the error `struct.error: unpack requires a string argument of length 12`
   then go into your **samples** directory and delete all files of length 0.

7. Start training the classifier with `opencv_traincascade`, which comes with
OpenCV, and save the results to `./classifier`:

         opencv_traincascade -data classifier -vec samples.vec -bg negatives.txt\
        -numStages 20 -minHitRate 0.995 -maxFalseAlarmRate 0.5 -numPos 1500\
        -numNeg 800 -w 80 -h 30 -mode ALL -precalcValBufSize 4096\
        -precalcIdxBufSize 4096 -featureType LBP -numThreads 8

    After starting the training program it will print back its parameters and then start training. Each stage will print out some analysis as it is trained:

      ```
      ===== TRAINING 0-stage =====
      <BEGIN
      POS count : consumed   1000 : 1000
      NEG count : acceptanceRatio    600 : 1
      Precalculation time: 11
      +----+---------+---------+
      |  N |    HR   |    FA   |
      +----+---------+---------+
      |   1|        1|        1|
      +----+---------+---------+
      |   2|        1|        1|
      +----+---------+---------+
      |   3|        1|        1|
      +----+---------+---------+
      |   4|        1|        1|
      +----+---------+---------+
      |   5|        1|        1|
      +----+---------+---------+
      |   6|        1|        1|
      +----+---------+---------+
      |   7|        1| 0.711667|
      +----+---------+---------+
      |   8|        1|     0.54|
      +----+---------+---------+
      |   9|        1|    0.305|
      +----+---------+---------+
      END>
      Training until now has taken 0 days 3 hours 19 minutes 16 seconds.
      ```

    Each row represents a feature that is being trained and contains some output about its HitRatio (HR) and FalseAlarm ratio (FA). If a training stage only selects a few features (e.g. N = 2) then its possible something is wrong with your training data.

    At the end of each stage the classifier is saved to a file and the process can be stopped and restarted. This is useful if you are tweaking a machine/settings to optimize training speed.

8. Wait until the process is finished (which takes a long time — a couple of hours probably, depending on the computer you have and how big your images are).

9. Use your finished classifier!

10. To get some visualization use:

        opencv_visualisation --image=in/example.png --model=classifier/lp-classifier.xml --data=out/result_


## Acknowledgements

A huge thanks goes to Naotoshi Seo, who wrote the `mergevec.cpp` and
`createsamples.cpp` tools and released them under the MIT licencse.

## References & Links:

- [Naotoshi Seo - Tutorial: OpenCV haartraining (Rapid Object Detection With A Cascade of Boosted Classifiers Based on Haar-like Features)](http://note.sonots.com/SciSoftware/haartraining.html)
- [Material for Naotoshi Seo's tutorial](https://code.google.com/p/tutorial-haartraining/)
- [OpenCV Documentation - Cascade Classifier Training](http://docs.opencv.org/doc/user_guide/ug_traincascade.html)
