# Utils
from __future__ import print_function
import imutils
# Func
import cv2
import numpy as np
from matplotlib import pyplot as plt

class RegionsOfInterest:
    # Pointer to dictionary from FileHandler class
    files = {}

    def __init__(self, files):
        self.files = files

    def extract_ROI(self, file, productType, templatesPath, outputPath):
        template_string = templatesPath + '/' + productType + '.jpg'
        tmp_image = self.normalize_image(template_string)

        outpath = outputPath + productType + '/' + str(file).split('/')[-1]
        path = file

        print("Processing: " + path + " out: " + str(outpath))

        # Normalize source image
        src_image = self.normalize_image(path)
        # Perform RoI extraction using SIFT & RANSAC algorithm
        warped = self.identify_kp_sift(source_filename=file, source=src_image, template=tmp_image)
        # Save image
        cv2.imwrite(outpath, warped)

    """
    Normalize image before extracting Regions of Interest
    @param image (String) - the filename/path to the image
    Returns a resized and grayscale-d np.ndarray object (image)
    """

    def normalize_image(self, image):
        # Load image in grayscale
        image_org = cv2.imread(image)
        image_org = imutils.resize(image_org, 700, 700)
        grayscale = cv2.imread(image, 0)
        grayscale = imutils.resize(grayscale, 700, 700)
        return grayscale

    """
    Function to extract Regions of Interest
    1. Identify keypoints from source and template image (SIFT)
    2. Match those keypoints (FLANN matcher)
    3. Compute the homography matrix
    4. Perform perspective transform based on #3.
    @param source_filename (String) - the filename/path to the image
    @param source (numpy.ndarray)   - Normalized source image
    @param template (numpy.ndarray) - Normalized template image
    Returns source image if computation fails
    Returns warped image otherwise
    """

    def identify_kp_sift(self, source_filename, source, template):
        # Minimum number of keypoint matches to qualify for homography matrix computation
        MIN_MATCH_COUNT = 10
        FLANN_INDEX_KDTREE = 1

        # -- Step 1: Detect the keypoints and descriptors using SIFT Detector
        sift = cv2.SIFT_create()
        keypoints_tmp, desc_tmp = sift.detectAndCompute(template, None)
        keypoints_src, desc_src = sift.detectAndCompute(source, None)

        # -- Draw keypoints
        # img_keypoints_tmp = np.empty((template.shape[0], template.shape[1], 3), dtype=np.uint8)
        # cv2.drawKeypoints(template, keypoints_tmp, img_keypoints_tmp)
        # cv2.imshow('SIFT Keypoints Template', img_keypoints_tmp)
        #
        # img_keypoints_src = np.empty((source.shape[0], source.shape[1], 3), dtype=np.uint8)
        # cv2.drawKeypoints(source, keypoints_src, img_keypoints_src)
        # cv2.imshow('SIFT Keypoints Source', img_keypoints_src)
        # cv2.waitKey()

        # -- Step 2: Find keypoint matches
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(desc_tmp, desc_src, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            tmp_pts = np.float32([keypoints_tmp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            src_pts = np.float32([keypoints_src[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(srcPoints=src_pts, dstPoints=tmp_pts, method=cv2.RANSAC,
                                         ransacReprojThreshold=5.0)
            matchesMask = mask.ravel().tolist()

            h, w = template.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

            # Catch empty homography matrix
            # https://answers.opencv.org/question/183108/assertion-failed-scn-1-mcols-in-perspectivetransform/
            if M is None:
                print("Empty homography matrix on source file " + source_filename)
                self.logToCSV(source_filename)
                return source
            else:
                dst = cv2.perspectiveTransform(pts, M)

            # Draw polygon on object of interest
            # source = cv2.polylines(source, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
            matchesMask = None
            return source

        # -- Step 3: Draw inliers (if successfully found the object) or matching keypoints (if failed).
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        # img3 = cv2.drawMatches(template, keypoints_tmp, source, keypoints_src, good, None, **draw_params)
        # plt.imshow(img3, 'gray'), plt.show()

        warped = cv2.warpPerspective(source, M, (w, h))
        # plt.imshow(warped, 'gray'), plt.show()
        return warped

    """
    Create/write to  a .csv containing the filename/s that produced an error
    i.e. Empty homography matrix
    @param filename (String)
    """

    def logToCSV(self, filename):
        with open('error_log.csv', 'a') as file:
            file.write(filename)

    def test_cases(self):
        # --------------------------------------------
        # --  Use Case 1 Kabuklod, 1575 images
        # --------------------------------------------

        # Template 1: Kabuklod
        # x- template_string = 'Nanai forms jpg/KABUKLOD_CROPPED_FULL.jpg'
        # template_string = 'nanai_cropped_forms/kabuklod_1.jpg'

        # -- Test Case 1: Low quality
        # src_string = '../KABUKLOD/KABUKLODSTUB1-PN0000040-2020-01-31-1580447450.jpeg'

        # -- Test Case 2: Rotated 45 deg. counterclockwise; Low quality
        # src_string = '../KABUKLOD/KABUKLODSTUB1-PN-2020-01-18.jpeg'

        # -- Test Case 3: Blurred, image included a shadow (FAILED)
        # src_string = '../KABUKLOD/KABUKLODSTUB1-PN-2020-01-20.jpeg'

        # -- Test Case 4: Form obstructed (finger); Low quality
        # src_string = '../KABUKLOD/KABUKLODSTUB1-PN0000094-2020-01-17.jpeg'

        # -- Test Case 5: Slanted angle
        # src_string = '../KABUKLOD/KABUKLODSTUB1-PN000567-2020-01-21.jpeg'

        # -- Test Case 6: Form slightly on the right; Light source at the top
        # src_string = '../KABUKLOD/KABUKLODSTUB1-PN0001116-2020-01-06.jpeg'

        # -- Test Case 7: Irregular angle; Cluttered background
        # src_string ='KabuklodStub1-PN0004083-2019-12-09.jpeg'

        # --------------------------------------------
        # -- Use Case 2 Sagip, 6842 images
        # --------------------------------------------
        # template_string = 'nanai_cropped_forms/sagip_1.jpg'

        # -- Test Case 1: Low quality;
        # src_string = '../SAGIP/SAGIPSTUB1-PN0015269-2019-12-23.jpeg'

        # -- Test Case 2: High angle shot; Patterned background
        # src_string = '../SAGIP/SAGIPSTUB1-PN0015168-2020-01-29-1580314945.jpeg'

        # -- Test Case 3: Dim lighting
        # src_string = '../SAGIP/SAGIPSTUB1-PN0015140-2020-01-29-1580312465.jpeg'

        # -- Test Case 4: Rotated 45 deg. clockwise
        # src_string = '../SAGIP/SAGIPSTUB1-PN0014185-2020-01-30-1580395091.jpeg'

        # -- Test Case 5: Form obstructed by shadow; Rotated 45 deg. clockwise
        # src_string = '../SAGIP/SAGIPSTUB1-PN0013663-2020-01-20.jpeg'

        # -- Test Case 6: Low quality; Insufficient keypoints detected
        # src_string = '../SAGIP_STUB_1/SAGIPSTUB1-PN-2019-12-17.jpeg'

        # --------------------------------------------
        # -- Use Case 3: Card Care, 6485 images
        # --------------------------------------------
        # template_string = 'nanai_cropped_forms/card_care_1.jpg'

        # -- Test Case 1:
        # src_string = '../CARDCARE/CARDCARESTUB1-PN0009247-2020-02-06-1580966905.jpeg'

        # -- Test Case 2: Form obstructed by a shadow
        # src_string = '../CARDCARE/CARDCARESTUB1-PN-2019-12-09.jpeg'

        # -- Test Case 3: Rotated 45 deg clockwise
        # src_string = '../CARDCARE/CARDCARESTUB1-PN-2019-12-17.jpeg'

        # -- Test Case 4: Cluttered background; Form is held on hand
        # src_string = '../CARDCARE/CARDCARESTUB1-PN0019522-2020-01-10.jpeg'

        # -- Test Case 5: Low-angle shot; Irregular; Cropped
        # src_string = '../CARDCARE/CARDCARESTUB1-PN0036381-2020-02-02-1580603115.jpeg'

        # -- Test Case 6: Caused error: (-215:Assertion failed) scn + 1 == m.cols in function 'perspectiveTransform'
        # Blurred image; noise detected at the background
        # src_string = '../CARDCARE/CARDCARESTUB1-PN0004247-2020-01-31-1580450823.jpeg'

        # src_image = normalize_image(src_string)
        # tmp_image = normalize_image(template_string)
        return None
