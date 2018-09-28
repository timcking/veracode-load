## Veracode Loader Developer Notes
### Dependencies

The Load and Link apps are written in Python 3.7 with PyQt5 for the GUI. Any version of Python 3.4 through 3.7 will work. The PyQt GUI requires Python 3, therefore Python 2 will not work. Connectivity to the database requires the Microsoft Access Database Engine 2010 which can be downloaded from [Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=13255). The later versions of the engine (2013 and 2016) seem to have compatibility problems with the 64-bit version of Office. The latest versions of pyodbc and pyinstaller are also required (installation instructions below).

### Development Environment Setup

Download [Python 3.x](https://www.python.org/downloads/windows/) (I recommend you install the 32-bit version - fewer compatibility issues) and run the installer. The installer should add the Python executable to your path. To test the install, open a command line and enter:
```
python --version
```

Rather than installing the Python packages globally, it is recommended that you setup a virtual environment. After you check out the code from SVN, go to the folder above your source folder (VeracodeAccessDb by default) and on the command line enter:
```
python -m venv VeracodeAccessDb
```
This will create several subfolders in VeracodeAccessDb including "Lib", "Include", "Scripts", and "\_\_pycache\_\_". You should add these folders to the TortoiseSVN ignore list.

Change to the VeracodeAccessDb directory and activate the environment by entering:
```
Scripts\activate.bat
```

You will need to run activate each time you open a new command window.

Install pyodbc, PyQt5, and the Python installer (one time only):
```
pip install pyodbc
pip install PyQt5
pip install pyinstaller
```
(The pip command installs packages from the internet and I have noticed that it does not work on the DCA network. A work-around is to temporarily disconnet your ethernet and sign on to the Guest WiFi network.)

### How to Run the Apps

After activating the environment and installing the additional packages, you should be able to run the GUI by entering:
```
python LoadApp.py
```

LoadApp calls VcParse, which does all of the parsing/loading work. You can run VcParse from the command line by entering:
```
python VcParse.py xml\filename.xml
```

To run the Link app:
```
python LinkApp.py
```

### How to Build and Deploy  

1. Open a command window and run ```Scripts\activate.bat```.

1. Run the Python installer for the LoadApp by entering:
   ```
   pyinstaller LoadApp.spec
   ```

1. Run the installer for the LinkApp:
   ```
   pyinstaller LinkApp.spec
   ```

1. The installer will create two folders, LoadApp and LinkApp, under the "dist" folder (you should tell TortoiseSVN to ignore the "dist" and "build" folders). The two directories will contain the same runtime libraries, so it is recommended that you copy ```LinkApp\*.*``` to the ```LoadApp``` directory and then delete the LinkApp directory. You should now have all of the executables and runtime libraries in the LoadApp directory.

1. In the LoadApp directory, verify that that ```data\Veracode.accdb``` exists. Create two additional directories, "log" and "xml" if they don't exist. 

1. Zip (or 7z) the LoadApp directory to a file named VeracodeLoad_YYYY-MM-DD.zip.

1. There is no install program, users can just unzip the file into a local directory. They will need to manually create Deskstop shortcuts to LoadApp.exe and LinkApp.exe.

1. To uninstall, delete the LoadApp folder.