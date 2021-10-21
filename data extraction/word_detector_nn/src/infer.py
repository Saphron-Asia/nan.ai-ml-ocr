import argparse

import torch
from path import Path

from dataloader import DataLoaderImgFile
from eval import evaluate
from net import WordDetectorNet
from visualization import visualize_and_plot
from visualization import visualize_and_save

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cuda')
    parser.add_argument('--data_dir', help='directory containing dataset', type=Path, required=True)
    parser.add_argument('--output_dir', help='directory where the output files will be saved, must be an absolute path',
                        type=Path, required=True)

    args = parser.parse_args()

    net = WordDetectorNet()
    # net.load_state_dict(torch.load('../model/weights', map_location=args.device))
    net.load_state_dict(torch.load('../model/weights', map_location='cpu'))
    # net.load_state_dict(torch.load('OCR/word_detector_nn/model/weights', map_location=args.device))
    net.eval()
    net.to(args.device)

    # loader = DataLoaderImgFile(Path('../data/Cardcare'), net.input_size, args.device)
    loader = DataLoaderImgFile(args.data_dir, net.input_size, args.device)
    res = evaluate(net, loader, max_aabbs=1000)
    # For progress tracking
    total_imgs = len(res.batch_imgs)

    print(f'total_imgs {total_imgs}')
    for i, (img, aabbs) in enumerate(zip(res.batch_imgs, res.batch_aabbs)):
        f = loader.get_scale_factor(i)
        aabbs = [aabb.scale(1 / f, 1 / f) for aabb in aabbs]
        img = loader.get_original_img(i)

        # Get NANAI form type and filename (refactor)
        # Windows
        # form_type = loader.fn_imgs[i].split("\\")[0]
        # form_type = form_type.split("/")[2]
        # filename = loader.fn_imgs[i].split("\\")[1]

        # Ubuntu OS
        # OCR/word_detector_nn/data/Cardcare/*.jpg
        form_type = loader.fn_imgs[i].split("/")[-2]
        filename = loader.fn_imgs[i].split("/")[-1]

        # Create the path for the output files
        folder_name = filename.split(".jpeg")[0]
        print("Saving to dir:" + args.output_dir + "/output/" + form_type + "/" + filename)

        print("Progress: " + str(i+1) + "/" + str(total_imgs))

        # Save detected words into separate images
        visualize_and_save(img, aabbs, form_type, folder_name, args.output_dir)

        # See bounding boxes on original image via matplotlib pyplot
        # visualize_and_plot(img, aabbs)


if __name__ == '__main__':
    main()
