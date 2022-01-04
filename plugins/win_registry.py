# python-3/python
import os
from zipfile import ZipFile


class artefactplugin:
    def run(self, inputDirectory, zipFile):
        regFiles = []
        basepath = os.path.join('Windows','System32','config')
        regFiles.append(os.path.join(basepath, 'SAM'))
        regFiles.append(os.path.join(basepath, 'SOFTWARE'))
        regFiles.append(os.path.join(basepath, 'SYSTEM'))

        for regFile in regFiles:
            regFullPath = os.path.join(inputDirectory, regFile)
            if os.path.exists(regFullPath):
                print("Found: " + regFullPath)
                zipFile.write(regFullPath)
