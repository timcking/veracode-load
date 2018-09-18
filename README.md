## Veracode Loader Installation and Usage
### Installation
*This installation will not modify Windows settings (e.g., the registry). This app can be completely removed by deleting the installation folder.*

1. The Microsoft Access 2010 Database Engine is required. Download and install from [Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=13255).
	
1. Unzip the file LoadApp_YYYY-MM-DD.7z into a local directory of your choice. A sub-folder named LoadApp will be created with the executables and data. 

1. There will be two .exe files in the LoadApp directory, LoadApp.exe and LinkApp.exe. You can create shortcuts on the Desktop if you choose. 

1. Verify that the following sub-folders exist under the LoadApp directory:
	* xml
	* log
	* data

The data directory will contain the Access database, Veracode.accdb. The Veracode XML files should be copied to the xml directory.

### Usage  

1. Run the LoadApp.exe file.

1. Use the File/Open menu to locate the XML file.

1. Press the Load button.

1. The status bar will display the number of flaws loaded.

1. If you have Cygwin installed, you can load all folders in the xml/ directory by running ./run.sh.

1. You can browse the Scans and associated Flaws by opening the Veracode database and selecting frmScans. You can view the raw data by opening the flaws, scans, or ticket tables.

1. When you are ready to assign Flaws to Citrix tickets:
	1. Open the Veracode database.

	1. Open frmTickets and enter the Citrix Ticket ID and the Release Version. Save the new record.

	1. Run the LinkApp.exe file and enter the Sandbox ID, the Citrix Ticket ID, and the Flaw IDs.

	1. Press the Link button.

	1. The linked Flaws will be displayed in frmTickets in the Veracode database.

