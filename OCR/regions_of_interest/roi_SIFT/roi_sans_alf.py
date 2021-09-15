# Utilities
from path import Path

# Functionalities
from file_handler import FileHandler
from roi import RegionsOfInterest as RoI


def main(path, form_type, outpath):
    print(f'path: {path} form_type: {form_type}')
    path = Path('/Users/joshuavillanueva/Data Analyst/UNICEF/unicef-innovations-analytics/SAMPLE/Sagip')
    data = path.files('*.jpg')
    tmp = '/Users/joshuavillanueva/Data Analyst/UNICEF/unicef-innovations-analytics/SAMPLE/templates'

    loader = FileHandler(csvPath=path, debug=False)
    roi = RoI(files=loader.files)
    total_objects = len(data)
    loader.create_dir()
    # roi = RoI(files=data)
    counter = 0

    for image in data:
        roi.extract_ROI(file=image,
                        productType='Sagip_1',
                        templatesPath=tmp,
                        outpath=outpath)
        counter += 1
        print(f'Progress: {"%.2f" % (counter/total_objects * 100) }%\t  Processed {counter}/{total_objects} files. ')

if __name__ == '__main__':
    main("testPath", "myFormType", "myOutpath")