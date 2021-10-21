import os
import csv
import shutil

class FileHandler:
    # Reference CSV file containing audited alfresco data
    csvPath = ''

    # Contains 'name', 'filename_local' and 'product' columns from csvPath
    # key: filename_local
    # value: an array containing the filename in .jpeg, and its product type
    files = {}

    # Enable print commands
    debug = False

    # Keep a copy of distinct products
    productType = set()

    def __init__(self, csvPath, **kwargs):
        self.csvPath = csvPath
        self.srcPath = kwargs.get('srcPath', None)
        self.debug = kwargs.get('debug', None)

    """
    Reads the contents of the audit file
    and save 'file' and 'filename_local' columns
    as a key-value pair using a dictionary.
    Returns the number of valid rows
    """
    def read_csv(self):
        with open(self.csvPath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0 and self.debug:
                    print(f'Headers are {", ".join(row)}')
                line_count += 1
                # Store data in key-value pairs
                # key: filename_local
                # value: an array containing the filename in .jpeg, and its product type
                self.files[row['filename_local']] = [ row['name'], row['product']]
                self.productType.add(row['product'])

            if self.debug:
                for key, value in self.files.items():
                    print(key, value)

            print(f'Recognized {line_count} items from audit file.')
            return line_count

    """
    Creates 'sorted' and 'output' directory based on distinct product types
    """
    def create_dir(self):
        # Print distinct products
        if self.debug:
            print(self.productType)

        if(os.path.exists('sorted') == False):
            os.mkdir('sorted')
        if(os.path.exists('output') == False):
            os.mkdir('output')

        for item in self.productType:
            if (self.debug is True) and (os.path.exists('sorted/'+item) is False):
                print(f'Created sorted/{item} directory')
            if (os.path.exists('sorted/'+item) == False):
                os.mkdir('sorted/' + item)

            if (self.debug is True) and (os.path.exists('output/'+item) is False):
                print(f'Created output/{item} directory')
            if (os.path.exists('output/'+item) == False):
                os.mkdir('output/' + item)

    """
    Renames filename_local to the file's actual name (.jpeg). 
    Segregates file to separete directories according to their product type
    """
    def segregate(self, **kwargs):
        srcPath = kwargs.get('srcPath', '')
        for key, value in self.files.items():
            if self.debug:
                print(f'src={srcPath}{key}  dst=sorted/{self.files.get(key)[1]}/{self.files.get(key)[0]}')
            # Rename and move file to appropriate product directory
            shutil.move(src= srcPath + key, dst='sorted/'+ self.files.get(key)[1] + '/' + self.files.get(key)[0])
