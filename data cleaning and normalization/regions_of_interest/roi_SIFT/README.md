**Python version**: 3.8 <br>
**OpenCV-Contrib**: 4.5.1.48

## Run the script
1. Provide a template that will be extracted from a given image. The template could be of a form or a page layout, etc.
1. Update the variables: `path`, `data`, `tmp`, `productType`
    1. `path`: the directory where the input files are located. The program will look for all *.jpg (by default and can be changed with the `data` variable) files and extract the Regions of Interest (RoI) from each one. 
    1. `data`: the file extension that the RoI will look for.
    1. `tmp`: path to the directory where the templates are stored. Takes .jpg images.
    1. `productType`: refers to the filename of the template image that will be used (sans the extension). The file is assumed to be in the `tmp` directory.
1. Run the script with:
    ```
    python roi_sans_alf.py
   ``` 
