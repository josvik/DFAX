# python-3/python
import os
from zipfile import ZipFile


class artefactplugin:
    def run(self, inputDirectory, zipFile):
        filetofind = "template_file_to_find.txt"
        
        fullPath = os.path.join(inputDirectory, filetofind)
        if os.path.exists(fullPath):
            print("Found: " + fullPath)
            zipFile.write(fullPath)
