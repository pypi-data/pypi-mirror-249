from basefunctions import filefunctions
import os
import pytest
import shutil


def test_checkIfFileExists():
    # Test when file exists
    assert filefunctions.checkIfFileExists("./test_filefunctions.py") == True

    # Test when file does not exist
    assert filefunctions.checkIfFileExists("/path/to/nonexistent/file.txt") == False

    # Test when file is a directory
    assert filefunctions.checkIfFileExists(".") == False

    # Test when file is a symbolic link
    assert filefunctions.checkIfFileExists("/path/to/symlink") == False


def test_checkIfDirExists():
    # Test when directory exists
    assert filefunctions.checkIfDirExists(".") == True

    # Test when directory does not exist
    assert filefunctions.checkIfDirExists("/path/to/nonexistent/directory") == False

    # Test when directory is a file
    assert filefunctions.checkIfDirExists("./test_filefunctions.py") == False

    # Test when directory is a symbolic link
    assert filefunctions.checkIfDirExists("/path/to/symlink") == False


def test__checkIfExists():
    # Test when file exists
    assert filefunctions._checkIfExists("./test_filefunctions.py", "FILE") == True

    # Test when file does not exist
    assert filefunctions._checkIfExists("/path/to/nonexistent/file.txt", "FILE") == False

    # Test when directory exists
    assert filefunctions._checkIfExists(".", "DIRECTORY") == True

    # Test when directory does not exist
    assert filefunctions._checkIfExists("/path/to/nonexistent/directory", "DIRECTORY") == False

    # Test when file is a symbolic link
    assert filefunctions._checkIfExists("/path/to/symlink", "FILE") == False

    # Test when directory is a symbolic link
    assert filefunctions._checkIfExists("/path/to/symlink", "DIRECTORY") == False
    

def test_isFile():
    # Test when file exists
    assert filefunctions.isFile("./test_filefunctions.py") == True

    # Test when file does not exist
    assert filefunctions.isFile("/path/to/nonexistent/file.txt") == False

    # Test when file is a directory
    assert filefunctions.isFile(".") == False

    # Test when file is a symbolic link
    assert filefunctions.isFile("/path/to/symlink") == False


def test_isDirectory():
    # Test when directory exists
    assert filefunctions.isDirectory(".") == True

    # Test when directory does not exist
    assert filefunctions.isDirectory("/path/to/nonexistent/directory") == False

    # Test when directory is a file
    assert filefunctions.isDirectory("./test_filefunctions.py") == False

    # Test when directory is a symbolic link
    assert filefunctions.isDirectory("/path/to/symlink") == False


def test_getFileName():
    # Test when path contains a file name
    assert filefunctions.getFileName("/path/to/file.txt") == "file.txt"

    # Test when path ends with a slash
    assert filefunctions.getFileName("/path/to/directory/") == ""

    # Test when path is empty
    assert filefunctions.getFileName("") == ""

    # Test when path contains multiple directories
    assert filefunctions.getFileName("/path/to/directory/file.txt") == "file.txt"

    # Test when path contains special characters
    assert filefunctions.getFileName("/path/to/file with spaces.txt") == "file with spaces.txt"


def test_getFileExtension():
    # Test when path contains a file extension
    assert filefunctions.getFileExtension("/path/to/file.txt") == ".txt"

    # Test when path does not contain a file extension
    assert filefunctions.getFileExtension("/path/to/file") == ""

    # Test when path ends with a dot
    assert filefunctions.getFileExtension("/path/to/file.") == ""

    # Test when path is empty
    assert filefunctions.getFileExtension("") == ""

    # Test when path contains multiple dots
    assert filefunctions.getFileExtension("/path/to/file.tar.gz") == ".gz"

    # Test when path contains special characters
    assert filefunctions.getFileExtension("/path/to/file with spaces.txt") == ".txt"


def test_getPathName():
    # Test when path contains a file name
    assert filefunctions.getPathName("/path/to/file.txt") == "/path/to/"

    # Test when path ends with a slash
    assert filefunctions.getPathName("/path/to/directory/") == "/path/to/directory/"

    # Test when path is empty
    assert filefunctions.getPathName("") == "./"

    # Test when path contains multiple directories
    assert filefunctions.getPathName("/path/to/directory/file.txt") == "/path/to/directory/"

    # Test when path contains special characters
    assert filefunctions.getPathName("/path/to/file with spaces.txt") == "/path/to/"


def test_getParentPathName():
    # Test when path contains a file name
    assert filefunctions.getParentPathName("/path/to/file.txt") == "/path/"

    # Test when path ends with a slash
    assert filefunctions.getParentPathName("/path/to/directory/") == "/path/to/"

    # Test when path is empty
    assert filefunctions.getParentPathName("") == None

    # Test when path contains multiple directories
    assert filefunctions.getParentPathName("/path/to/directory/file.txt") == "/path/to/"

    # Test when path contains special characters
    assert filefunctions.getParentPathName("/path/to/file with spaces.txt") == "/path/"


def test_getBaseName():
    # Test when path contains a file name
    assert filefunctions.getBaseName("/path/to/file.txt") == "file.txt"

    # Test when path ends with a slash
    assert filefunctions.getBaseName("/path/to/directory/") == ""

    # Test when path is empty
    assert filefunctions.getBaseName("") == ""

    # Test when path contains multiple directories
    assert filefunctions.getBaseName("/path/to/directory/file.txt") == "file.txt"

    # Test when path contains special characters
    assert filefunctions.getBaseName("/path/to/file with spaces.txt") == "file with spaces.txt"


def test_getBaseNamePrefix():
    # Test when path contains a file name
    assert filefunctions.getBaseNamePrefix("/path/to/file.txt") == "file"

    # Test when path ends with a slash
    assert filefunctions.getBaseNamePrefix("/path/to/directory/") == ""

    # Test when path is empty
    assert filefunctions.getBaseNamePrefix("") == ""

    # Test when path contains multiple directories
    assert filefunctions.getBaseNamePrefix("/path/to/directory/file.txt") == "file"

    # Test when path contains special characters
    assert filefunctions.getBaseNamePrefix("/path/to/file with spaces.txt") == "file with spaces"


def test_getExtension():
    # Test when path contains a file extension
    assert filefunctions.getExtension("/path/to/file.txt") == "txt"

    # Test when path ends with a slash
    assert filefunctions.getExtension("/path/to/directory/") == ""

    # Test when path is empty
    assert filefunctions.getExtension("") == ""

    # Test when path contains multiple extensions
    assert filefunctions.getExtension("/path/to/directory/file.tar.gz") == "gz"

    # Test when path contains special characters
    assert filefunctions.getExtension("/path/to/file with spaces.txt") == "txt"


def test_getPathAndBaseNamePrefix():
    # Test when path contains a file name
    assert filefunctions.getPathAndBaseNamePrefix("/path/to/file.txt") == "/path/to/file"

    # Test when path ends with a slash
    assert filefunctions.getPathAndBaseNamePrefix("/path/to/directory/") == "/path/to/directory"

    # Test when path is empty
    assert filefunctions.getPathAndBaseNamePrefix("") == "."

    # Test when path contains multiple directories
    assert filefunctions.getPathAndBaseNamePrefix("/path/to/directory/file.txt") == "/path/to/directory/file"

    # Test when path contains special characters
    assert filefunctions.getPathAndBaseNamePrefix("/path/to/file with spaces.txt") == "/path/to/file with spaces"


def test_getCurrentDirectory():
    assert filefunctions.getCurrentDirectory() == os.getcwd()


def test_setCurrentDirectory():
    # remember current directory
    currentDir = filefunctions.getCurrentDirectory()

    # Test when directory exists
    directory_name = filefunctions.normpath( currentDir + os.path.sep + "../src/basefunctions" )
    filefunctions.setCurrentDirectory(directory_name)
    assert os.getcwd() == directory_name

    # Test when directory does not exist
    directory_name = "/nonexistent/directory"
    with pytest.raises(RuntimeError):
        filefunctions.setCurrentDirectory(directory_name)

    # restore current directory
    os.chdir(currentDir)
    

def test_renameFile():
    # remove target file if it exists
    target_file = "./target.txt"
    if os.path.exists(target_file):
        os.remove(target_file)

    # Test when source file exists and target file does not exist
    source_file = "./source.txt"
    target_file = "./target.txt"
    open(source_file, 'w').close()  # create source file
    filefunctions.renameFile(source_file, target_file)
    assert os.path.exists(target_file)
    assert not os.path.exists(source_file)

    # Test when source file exists and target file exists with overwrite=True
    source_file = "./source.txt"
    target_file = "./target.txt"
    open(source_file, 'w').close()  # create source file
    open(target_file, 'w').close()  # create target file
    filefunctions.renameFile(source_file, target_file, overwrite=True)
    assert os.path.exists(target_file)
    assert not os.path.exists(source_file)

    # Test when source file exists and target file exists with overwrite=False
    source_file = "./source.txt"
    target_file = "./target.txt"
    open(source_file, 'w').close()  # create source file
    open(target_file, 'w').close()  # create target file
    with pytest.raises(FileExistsError):
        filefunctions.renameFile(source_file, target_file, overwrite=False)

    # Test when source file does not exist
    source_file = "./nonexistent.txt"
    target_file = "./target.txt"
    os.remove(target_file)
    with pytest.raises(FileNotFoundError):
        filefunctions.renameFile(source_file, target_file)

    # Test when target file is a directory
    source_file = "./source.txt"
    target_dir = "./target_dir"
    if os.path.exists(target_dir):
        os.rmdir(target_dir)
    os.makedirs(target_dir)  # create target directory
    with pytest.raises(IsADirectoryError):
        filefunctions.renameFile(source_file, target_dir)

    # cleanup for source and target files
    if filefunctions.checkIfFileExists(source_file):
        os.remove(source_file)
    if filefunctions.checkIfFileExists(target_file):    
        os.remove(target_file)
    if os.path.exists(target_dir):
        os.rmdir(target_dir)


def test_removeFile():
    temp_file = "./temp.txt"

    # Create a temporary file
    open(temp_file, 'w').close()

    # Remove the file
    filefunctions.removeFile(temp_file)

    # Check if the file no longer exists
    assert not os.path.exists(temp_file)


def test_createDirectory():
    # Test when directory does not exist
    dir_name = "test_directory"
    filefunctions.createDirectory(dir_name)
    assert os.path.exists(dir_name)
    assert os.path.isdir(dir_name)
    
    # Test when directory already exists
    filefunctions.createDirectory(dir_name)
    assert os.path.exists(dir_name)
    assert os.path.isdir(dir_name)
    
    # Test when more then one directory needs to be created
    filefunctions.createDirectory("test_directory/test_subdirectory")
    assert os.path.exists(dir_name)
    assert os.path.isdir(dir_name)

    # Clean up
    shutil.rmtree(dir_name)


def test_createFileList():
    # prepare test directory
    dir_name = "./test_directory"
    filefunctions.createDirectory(dir_name)
    open(dir_name + "/file1.txt", 'w').close()
    open(dir_name + "/file2.txt", 'w').close()
    open(dir_name + "/file3.csv", 'w').close()
    open(dir_name + "/.file4.txt", 'w').close()
    dir_name2 = "./test_directory/sub_directory"
    filefunctions.createDirectory(dir_name2)
    open(dir_name2 + "/file5.txt", 'w').close()
    open(dir_name2 + "/file6.txt", 'w').close()

    # Test when patternList contains a single pattern
    fileList = filefunctions.createFileList(patternList=["*.txt"], dirName=dir_name)
    assert len(fileList) == 2  # Assuming there are 2 text files in the test_directory
    
    # Test when patternList contains multiple patterns
    fileList = filefunctions.createFileList(patternList=["*.txt", "*.csv"], dirName=dir_name)
    assert len(fileList) == 3  # Assuming there are 2 text files and 1 CSV file in the test_directory
    
    # Test when dirName is None
    fileList = filefunctions.createFileList(patternList=["*.txt"])
    assert len(fileList) == 0  # Assuming there are no text files in the current directory
    
    # Test when recursive is True
    fileList = filefunctions.createFileList(patternList=["*.txt"], dirName=dir_name, recursive=True)
    assert len(fileList) == 4  # Assuming there are 4 text files in the test_directory and its subdirectories
    
    # Test when appendDirs is True
    fileList = filefunctions.createFileList(patternList=["*.txt"], dirName=dir_name, appendDirs=True)
    assert len(fileList) == 2  # Assuming there are 2 text files in the test_directory and 1 subdirectory
    
    # Test when addHiddenFiles is True
    fileList = filefunctions.createFileList(patternList=["*.txt"], dirName=dir_name, addHiddenFiles=True)
    assert len(fileList) == 3  # Assuming there are 2 text files and 1 hidden file in the test_directory

    # Test when reverseSort is True
    fileList = filefunctions.createFileList(patternList=["*"], dirName=dir_name, reverseSort=True)
    assert fileList == ["./test_directory/file3.csv", "./test_directory/file2.txt", "./test_directory/file1.txt"]  # Assuming the files are named file1.txt, file2.txt, file3.txt in that order

def test_normpath():
    # Test when path contains backslashes
    path = "C:\\Users\\username\\Documents\\file.txt"
    expected_result = "C:/Users/username/Documents/file.txt"
    assert filefunctions.normpath(path) == expected_result

    # Test when path contains duplicate slashes
    path = "C:/Users//username/Documents//file.txt"
    expected_result = "C:/Users/username/Documents/file.txt"
    assert filefunctions.normpath(path) == expected_result

    # Test when path contains relative directory references
    path = "C:/Users/username/Documents/../file.txt"
    expected_result = "C:/Users/username/file.txt"
    assert filefunctions.normpath(path) == expected_result

    # Test when path contains current directory references
    path = "C:/Users/username/Documents/./file.txt"
    expected_result = "C:/Users/username/Documents/file.txt"
    assert filefunctions.normpath(path) == expected_result

    # Test when path is already normalized
    path = "C:/Users/username/Documents/file.txt"
    expected_result = "C:/Users/username/Documents/file.txt"
    assert filefunctions.normpath(path) == expected_result

