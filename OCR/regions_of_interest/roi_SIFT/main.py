# Utilities
import os

# Functionalities
from roi import RegionsOfInterest as RoI


def create_dir(outPath, formType):
    if not os.path.exists(outPath + '/output'):
        os.mkdir(outPath + '/output')
    if not os.path.exists(outPath + '/output/' + formType):
        os.mkdir(outPath + '/output/' + formType)
        print(f'Created {outPath}/output/{formType} directory')


"""
@param imgPath (String) - the filename/path to the image
@param outPath (String)   - directory where 'output/<form_type>/<filename>.jpg' will be saved
@param templatePath (String) - directory where templates of forms are saved
@param formType (String) - should match the filename of saved form templates on 'templatePath'
"""


def main(imgPath, outPath, templatePath, formType):
    roi = RoI(files=imgPath)
    create_dir(outPath, formType)
    roi.extract_ROI(file=imgPath,
                    productType=formType,
                    templatesPath=templatePath,
                    outPath=outPath)


if __name__ == '__main__':
    img_path = '/Users/joshuavillanueva/Data Analyst/Github/SAMPLE/Sagip/9.jpg'
    outpath = '/Users/joshuavillanueva/Data Analyst/Github/SAMPLE'
    tmp = '/Users/joshuavillanueva/Data Analyst/Github/SAMPLE/templates'
    form_type = 'Sagip_2'

    main(imgPath=img_path, outPath=outpath, templatePath=tmp, formType=form_type)
