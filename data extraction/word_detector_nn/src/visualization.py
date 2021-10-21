import cv2
import matplotlib.pyplot as plt
import numpy as np
import os


def visualize_and_save(img, aabbs, form_type, folder_name, output_dir):
    img = ((img + 0.5) * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # cv2.imshow("visualize", img)
    # cv2.waitKey()
    i = 0

    # Create output dir
    if not os.path.exists(output_dir + "/output"):
        os.mkdir(output_dir + "/output")
    if not os.path.exists(output_dir + "/output/" + form_type):
        os.mkdir(output_dir + "/output/" + form_type)
    if not os.path.exists(output_dir + "/output/" + form_type + "/" + folder_name):
        os.mkdir(output_dir + "/output/" + form_type + "/" + folder_name)

    for aabb in aabbs:
        aabb = aabb.enlarge_to_int_grid().as_type(int)
        # cv2.rectangle(img, (aabb.xmin, aabb.ymin), (aabb.xmax, aabb.ymax), (255, 0, 255), 2)

        crop_region = img[aabb.ymin:aabb.ymax, aabb.xmin:aabb.xmax]
        # TO DO: Output image w/ padding then feed that to HTR model
        # Compute image padding. This size is fixed for 128x32 pixel image

        if crop_region.shape[1] > 128:
            x_padding = 0
        else:
            x_padding = 128 - crop_region.shape[1]

        if crop_region.shape[0] > 32:
            y_padding = 0
        else:
            y_padding = (32 - crop_region.shape[0])/2

        crop_region = cv2.copyMakeBorder(crop_region, int(y_padding), int(y_padding),
                                         None, int(x_padding), cv2.BORDER_CONSTANT, None, (255, 255, 255))

        # For testing, see padded image
        # print("Shape: " + str(crop_region.shape))
        # cv2.imshow("padded", crop_region)
        # cv2.waitKey()

        cv2.imwrite(output_dir + "/output/" + form_type + "/" + folder_name + "/" + str(i) + ".jpeg", crop_region)
        i += 1

    # cv2.imshow("Plot", img)
    # cv2.waitKey()

    return img


def visualize_and_plot(img, aabbs):
    plt.imshow(img, cmap='gray')
    # print(type(aabbs))
    print(type(img))
    # Plot the bounding boxes one-by-one
    for aabb in aabbs:
        plt.plot([aabb.xmin, aabb.xmin, aabb.xmax, aabb.xmax, aabb.xmin],
                 [aabb.ymin, aabb.ymax, aabb.ymax, aabb.ymin, aabb.ymin])
    plt.show()

def visualize(img, aabbs):
    img = ((img + 0.5) * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for aabb in aabbs:
        aabb = aabb.enlarge_to_int_grid().as_type(int)
        cv2.rectangle(img, (aabb.xmin, aabb.ymin), (aabb.xmax, aabb.ymax), (255, 0, 255), 2)

    return img