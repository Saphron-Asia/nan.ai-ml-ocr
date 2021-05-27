# Functionalities
from file_handler import FileHandler
from roi import RegionsOfInterest as RoI


if __name__ == '__main__':
    # Initialize variables and classes

    # Path to csv file containing alfresco data audit
    csv_path = 'raw copy/roi-third-batch-again.csv'

    # Path to jpeg files, leave blank ('') if running from the same dir
    raw_files_path = 'raw/filtered/'

    # Path to the template of the forms
    # The directory should contain a jpg file for each product
    # i.e. Cardcare.jpg, Kabuklod.jpg, Sagip.jpg
    templates_path = 'raw copy/templates'

    loader = FileHandler(csvPath=csv_path, debug=False)
    roi = RoI(files=loader.files)

    # --------------------------------------
    # --------- PREPROCESSING
    # --------------------------------------
    # Load csv file and extract 'file' and 'filename_local' columns
    # Store the number of identified rows
    total_objects = loader.read_csv()
    loader.create_dir()
    loader.segregate(srcPath=raw_files_path)

    # --------------------------------------
    # --------- RoI Extraction
    # --------------------------------------
    # For every file stored in the dictionary, extract RoI
    counter = 0
    for key, value in loader.files.items():
        roi.extract_ROI(file=loader.files.get(key)[0],
                        productType=loader.files.get(key)[1],
                        templatesPath=templates_path)
        counter += 1
        print(f'Progress: {"%.2f" % (counter/total_objects * 100) }%\t  Processed {counter}/{total_objects} files. ')
