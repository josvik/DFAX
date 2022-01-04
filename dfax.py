# python-3/python
import re
import sys
import os
import logging
import time
import argparse
import tempfile
import subprocess
from zipfile import ZipFile

pluginsToRun = {}
unmountAndDetachCommands = []
tmpFolders = []

def LoadEwfInput(inputPath):
    inputDirectories = []
    tmpFolder = tempfile.TemporaryDirectory()
    tmpFolders.append(tmpFolder)

    ewfMountPoint = os.path.join(tmpFolder.name, "ewfmount")
    os.makedirs(ewfMountPoint)
    # Create temp mountpoint and mount ewf-file.
    ewfMountProcess = subprocess.run(["ewfmount", inputPath, ewfMountPoint],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    if ewfMountProcess.returncode and ewfMountProcess.returncode != 0:
        logging.error("Error in ewfmount.")
        logging.error(ewfMountProcess.returncode)
        logging.error(ewfMountProcess.stderr.read())
        logging.error(ewfMountProcess.stdout.read())
        exit(1)
    unmountAndDetachCommands.append(["umount", ewfMountPoint])
    logging.info("Mounted EWF file to tmp folder. ewfmount %s %s", inputPath, ewfMountPoint)

    # Get the next loop device for mounting
    nextLoopProcess = subprocess.run(["losetup", "-f"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    loopDevice = nextLoopProcess.stdout.decode("utf-8").strip()
    unmountAndDetachCommands.append(["losetup", "-d", loopDevice])

    # Mount the internal ewf1 file to loop device.
    internalEwf1File = os.path.join(ewfMountPoint, "ewf1")
    mountLoopProcess = subprocess.run(["losetup", "-P", loopDevice, internalEwf1File],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    logging.info("Mounted internal ewf1 file to loop device. losetup -P %s %s", loopDevice, internalEwf1File)
    unmountAndDetachCommands.append(["umount", internalEwf1File])

    # Get the mounted partitions   sudo fdisk -l /dev/loop29 | grep -e "^/dev/loop29"
    mountedPartProcess = subprocess.run(["fdisk", "-l", loopDevice],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
    mountedPartOutput = mountedPartProcess.stdout.decode("utf-8")
    partitionsResult = re.finditer("^(" + loopDevice + "p\d+)", mountedPartOutput, flags=re.MULTILINE)
    for partRes in partitionsResult:
        partLoopDevice = partRes.group(1)
        partNum = partLoopDevice[len(loopDevice):]
        partMountPoint = os.path.join(tmpFolder.name, partNum)
        os.makedirs(partMountPoint)
        subprocess.run(["mount", "-o", "ro", partLoopDevice, partMountPoint],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        logging.info("Mounted partition to tmpfolder. mount -o ro %s %s", partLoopDevice, partMountPoint)
        unmountAndDetachCommands.append(["umount", partMountPoint])
        inputDirectories.append(partMountPoint)
    return inputDirectories

def LoadInput(inputPath):
    inputDirectories = []
    if os.path.isdir(inputPath):
        inputDirectories.append(inputPath)
        logging.info("Input is folder.")
    elif os.path.isfile(inputPath):
        logging.info("Input is file.")
        if inputPath[-4:] == ".e01" or inputPath[-4:] == ".E01":
            logging.info("Input is EWF-file.")
            inputDirectories = LoadEwfInput(inputPath)
    else:
        logging.error("Input not exists.")
        print("Error: Input not exists.")
    return inputDirectories



def UnmountAndDelete():
    unmountAndDetachCommands.reverse()
    for command in unmountAndDetachCommands:
        subprocess.run(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        logging.info("UnmountAndDelete cleanup command: " + " ".join(command))

    for tmpFolder in tmpFolders:
        tmpFolder.cleanup()
        logging.info("TempFolder cleanup. %s", tmpFolder.name)

def LoadPlugins(pluginfolder, pluginstoload=""):
    pluginpath = os.path.join(os.path.dirname(__file__), pluginfolder)
    sys.path.append(pluginpath)
    for pluginfile in os.listdir(pluginpath):
        if pluginfile[0] != "_" and pluginfile[-3:] == ".py":
            pluginname = pluginfile[:-3]
            if pluginstoload != "" and pluginname not in pluginstoload:
                continue
            pluginmodule = __import__(pluginname)
            try:
                pluginsToRun[pluginname] = pluginmodule.artefactplugin()
                del pluginmodule
                logging.info("Plugin loaded: %s", pluginname)
            except AttributeError:
                logging.debug("Plugin load failed (%s) Not a valid plugin, missing class", pluginname)


def RunPlugins(inputDirectory, zipFile):
    for pluginname in pluginsToRun:
        print("Running plugin:", pluginname, "(" + os.path.basename(inputDirectory) + ")")
        logging.info("Running plugin: %s (%s)", pluginname, os.path.basename(inputDirectory))
        try:
            pluginsToRun[pluginname].run(inputDirectory, zipFile)
        except TypeError:
            logging.debug(pluginname + " - Not a valid module. TypeError in run()")

def CreateLogger(outputdir):
    logging.basicConfig(filename=os.path.join(args.output, "log.txt"),
                        format="%(asctime)s (%(levelname)s) %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DFAX - Digital Forensics Artifact eXtractor")
    parser.add_argument('plugins', help='plugins to run. Comma separated list')
    parser.add_argument('input', help='File or path to run extractor against')
    parser.add_argument('output', help='Path for result of extraction')
    args = parser.parse_args()

    try:
        outputdir = os.path.join(args.output, time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(outputdir, exist_ok=True)
        CreateLogger(outputdir)
        logging.info("Running DFAX script agains: %s output to %s", args.input, outputdir)
        inputDirectories = LoadInput(args.input)
        LoadPlugins("plugins", args.plugins)
        for inputDirectory in inputDirectories:
            zipfilename = os.path.basename(inputDirectory) + ".zip"
            with ZipFile(os.path.join(outputdir, zipfilename), "w") as zipFile:
                logging.info("Created zipfile: %s", zipFile.filename)
                RunPlugins(inputDirectory, zipFile)
    except Exception as e:
        logging.error("Major crash!")
        logging.error(e)
    UnmountAndDelete()
