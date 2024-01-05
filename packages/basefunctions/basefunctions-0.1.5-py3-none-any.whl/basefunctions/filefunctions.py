# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  filefunctions provide basic functionality for file handling stuff
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import os
import shutil
import fnmatch

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


def checkIfFileExists(fileName):
    """
    Check if a file exists.

    Parameters
    ----------
    fileName : str
        The name of the file to be checked.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    if fileName:
        return _checkIfExists(fileName, fileType="FILE")
    else:
        return False


def checkIfDirExists(dirName):
    """
    Check if directory exists.

    Parameters
    ----------
    dirName : str
        Directory name to be checked.

    Returns
    -------
    bool
        True if directory exists, False otherwise.
    """
    if dirName:
        return _checkIfExists(dirName, fileType="DIRECTORY")
    else:
        return False


def _checkIfExists(fileName, fileType="FILE"):
    """
    Check if a specific file or directory exists.

    Parameters
    ----------
    fileName : str
        Name of the file or directory to be checked.
    fileType : str, optional
        Type of file or directory to be checked, by default "FILE".

    Returns
    -------
    bool
        True if the file or directory exists, False otherwise.
    """
    if fileType == "FILE":
        return os.path.exists(fileName) and os.path.isfile(fileName)
    if fileType == "DIRECTORY":
        return os.path.exists(fileName) and os.path.isdir(fileName)


def isFile(fileName):
    """
    Check if fileName is a regular file.

    Parameters
    ----------
    fileName : str
        Name of the file to be checked.

    Returns
    -------
    bool
        True if the file exists and is a regular file.
    """
    return checkIfFileExists(fileName)


def isDirectory(dirName):
    """
    Check if `dirName` is a regular directory.

    Parameters
    ----------
    dirName : str
        Name of the directory to be checked.

    Returns
    -------
    bool
        True if the directory exists and is a directory, False otherwise.
    """
    return checkIfDirExists(dirName)


def getFileName(pathFileName):
    """
    Get the file name part from a complete file path.

    Parameters
    ----------
    pathFileName : str
        The complete file path.

    Returns
    -------
    str
        The file name part of the file path.

    Examples
    --------
    >>> getFileName('/home/usr/Desktop/2352222.pdf')
    '2352222.pdf'
    """
    return (
        os.path.basename(pathFileName) if pathFileName or pathFileName == "" else None
    )


def getFileExtension(pathFileName):
    """
    Get the file extension from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get the file extension from.

    Returns
    -------
    str
        The file extension of the file name.

    Examples
    --------
    >>> getFileExtension('/home/usr/Desktop/2352222.abc.pdf')
    '.pdf'
    """
    extension = os.path.splitext(pathFileName)[-1] if pathFileName else None
    if extension in [None, "."]:
        return ""
    return extension


def getPathName(pathFileName):
    """
    Get the path name from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get information from.

    Returns
    -------
    str
        The path name of the file name.
    """
    return (
        os.path.normpath(os.path.split(pathFileName)[0]) + os.path.sep
        if pathFileName or pathFileName == ""
        else None
    )


def getParentPathName(pathFileName):
    """
    Get the parent path name from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get information from.

    Returns
    -------
    str
        The parent path name.

    Examples
    --------
    >>> getParentPathName('/home/usr/Desktop/file.txt')
    '/home/usr/'
    """
    return (
        os.path.normpath(os.path.split(os.path.split(pathFileName)[0])[0]) + os.path.sep
        if pathFileName
        else None
    )


def getBaseName(pathFileName):
    """
    Get the base name part from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get information from.

    Returns
    -------
    str
        The base name of the file.

    Examples
    --------
    >>> getBaseName ('/home/usr/Desktop/file.txt')
    'file.txt'
    """
    return getFileName(pathFileName)


def getBaseNamePrefix(pathFileName):
    """
    Get the basename prefix from a complete fileName.

    Parameters
    ----------
    pathFileName : str
        The path file name to get information from.

    Returns
    -------
    str
        The basename prefix of the file name.

    Examples
    --------
    >>> getBaseNamePrefix('/home/usr/Desktop/file.abc.txt')
    'file.abc'
    """
    return (
        getBaseName(pathFileName).split(".")[0]
        if pathFileName or pathFileName == ""
        else None
    )


def getExtension(pathFileName):
    """
    Get the extension from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get the extension from.

    Returns
    -------
    str
        The extension of the file name.

    Examples
    --------
    >>> getExtension('/home/usr/Desktop/2352222.pdf')
    '.pdf'
    """
    return (
        getBaseName(pathFileName).split(".")[-1]
        if pathFileName or pathFileName == ""
        else None
    )


def getPathAndBaseNamePrefix(pathFileName):
    """
    Get the path and base name from a complete file name.

    Parameters
    ----------
    pathFileName : str
        The path file name to get information from.

    Returns
    -------
    str
        The path and base name of the file name.
    """
    return (
        os.path.normpath(os.path.splitext(pathFileName)[0])
        if pathFileName or pathFileName == ""
        else None
    )


def getCurrentDirectory():
    """
    Get the current directory of the process.

    Returns
    -------
    str
        The name of the current directory.
    """
    return os.getcwd()


def setCurrentDirectory(directoryName):
    """
    Set the current directory of the process.

    Parameters
    ----------
    directoryName : str
        The name of the directory to set as the current directory.

    Raises
    ------
    RuntimeError
        If the specified directory does not exist.

    """
    if directoryName not in [".", ".."] and not checkIfDirExists(directoryName):
        raise RuntimeError(f"Directory '{directoryName}' not found.")
    os.chdir(directoryName)


def renameFile(src, target, overwrite=False):
    """Rename a file.

    This function renames a file from the source path to the target path.
    It can also handle cases where the target file already exists and
    provides an option to overwrite it.

    Parameters
    ----------
    src : str
        The source file name or path.
    target : str
        The target file name or path.
    overwrite : bool, optional
        Flag indicating whether to overwrite the target file if it already exists.
        If set to False and the target file exists, a RuntimeError will be raised.
        Default is False.

    Raises
    ------
    FileNotFoundError
        If the target directory doesn't exist.
    FileExistsError
        If the target file already exists and the overwrite flag is set to False.
    FileNotFoundError
        If the source file doesn't exist.
    """
    # check if target directory exists if available
    dirName = getPathName(target)
    if not dirName or not checkIfDirExists(dirName):
        raise FileNotFoundError(f"{dirName} doesn't exist, can't rename file")
    # check if target file exists already and we should not overwrite it
    if overwrite == False and checkIfFileExists(target):
        raise FileExistsError(f"{target} already exists and overwrite flag set False")
    # check if source file exists
    if checkIfFileExists(src):
        os.rename(src, target)
    else:
        raise FileNotFoundError(f"{src} doesn't exist")


def removeFile(fileName):
    """Remove a file.

    This function removes the specified file if it exists.

    Parameters
    ----------
    fileName : str
        The name of the file to remove.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.

    """
    if checkIfFileExists(fileName):
        os.remove(fileName)


def createDirectory(dirName):
    """Create a directory recursively.

    This function creates a directory recursively, which means a complete path to
    the requested structure will be created if it doesn't exist yet.

    Parameters
    ----------
    dirName : str
        Directory path to create.

    Returns
    -------
    None
        This function does not return anything.

    Raises
    ------
    OSError
        If there is an error while creating the directory.

    """
    os.makedirs(dirName, exist_ok=True)


def removeDirectory(dirName):
    """Remove a directory.

    This function removes the specified directory and all its contents recursively.

    Parameters
    ----------
    dirName : str
        The name of the directory to be removed.

    Raises
    ------
    RuntimeError
        Raises a RuntimeError when trying to remove the root directory ('/').

    """
    if not checkIfDirExists(dirName):
        return
    if dirName == os.path.sep or dirName == "/":
        raise RuntimeError("Can't delete the root directory ('/')")
    shutil.rmtree(dirName)


def createFileList(
    patternList=["*"],
    dirName=None,
    recursive=False,
    appendDirs=False,
    addHiddenFiles=False,
    reverseSort=False,
):
    """
    Create a file list from a given directory.

    Parameters
    ----------
    patternList : list, optional
        Pattern elements to search for. Default is ["*"].
    dirName : str, optional
        Directory to search. If None, the current directory is used. Default is None.
    recursive : bool, optional
        Recursive search. Default is False.
    appendDirs : bool, optional
        Append directories matching the patterns. Default is False.
    addHiddenFiles : bool, optional
        Append hidden files matching the patterns. Default is False.
    reverseSort : bool, optional
        Reverse sort the result list. Default is False.

    Returns
    -------
    list
        List of files and directories matching the patterns.
    """
    resultList = []
    if not dirName:
        dirName = "."
    if not (
        dirName.startswith(os.path.sep) or ":" in dirName
    ) and not dirName.startswith("."):
        dirName = f".{os.path.sep}{dirName}"
    if not isinstance(patternList, list):
        patternList = [patternList]
    if not checkIfDirExists(dirName):
        return resultList
    for fileName in os.listdir(dirName):
        for pattern in patternList:
            if recursive and os.path.isdir(os.path.sep.join([dirName, fileName])):
                resultList.extend(
                    createFileList(
                        patternList,
                        os.path.sep.join([dirName, fileName]),
                        recursive,
                        appendDirs,
                        addHiddenFiles,
                        reverseSort,
                    )
                )
            if fnmatch.fnmatch(fileName, pattern):
                if appendDirs and os.path.isdir(os.path.sep.join([dirName, fileName])):
                    resultList.append(fileName)
                if isFile(os.path.sep.join([dirName, fileName])):
                    if not addHiddenFiles and fileName.startswith("."):
                        continue
                    resultList.append(os.path.sep.join([dirName, fileName]))
    resultList.sort(reverse=reverseSort)
    return resultList


def normpath(fileName):
    """
    Normalize a path.

    Parameters
    ----------
    fileName : str
        File name to normalize.

    Returns
    -------
    str
        Normalized path name.
    """
    return os.path.normpath(fileName.replace("\\", "/"))
