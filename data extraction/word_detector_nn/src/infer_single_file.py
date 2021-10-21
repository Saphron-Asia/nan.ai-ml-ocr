import torch

from dataloader import DataLoaderImgFile
from eval import evaluate
from net import WordDetectorNet
from visualization import visualize_and_save
from path import Path

"""
@param file_path (String) - path to input image
@param output_dir (String) - path where the output will be saved
@param device (String) - cpu or cuda
"""


def main(file_path, output_dir, device):
    net = WordDetectorNet()
    net.load_state_dict(torch.load('../model/weights', map_location=device))
    net.eval()
    net.to(device)

    loader = DataLoaderImgFile(file_path, net.input_size, device)
    res = evaluate(net, loader, max_aabbs=1000)

    for i, (img, aabbs) in enumerate(zip(res.batch_imgs, res.batch_aabbs)):
        f = loader.get_scale_factor(i)
        aabbs = [aabb.scale(1 / f, 1 / f) for aabb in aabbs]
        img = loader.get_original_img(i)

        # Get NANAI form type and filename
        form_type = loader.fn_img.split("/")[-2]
        filename = loader.fn_img.split("/")[-1]

        # Create the path for the output files
        folder_name = filename.split(".jpeg")[0]
        print("Saving to dir:" + output_dir + "/" + form_type + "/" + filename)

        # Save detected words into separate images
        visualize_and_save(img, aabbs, form_type, folder_name, output_dir)


if __name__ == '__main__':
    main(file_path='/Users/harlenemanlapaz/Desktop/projects/nanai_type_identifier/sagip2.jpg',
         output_dir='/Users/harlenemanlapaz/Desktop/projects/unicef-innovations-analytics/OCR/service/media/output_wnn',
         device='cpu')
