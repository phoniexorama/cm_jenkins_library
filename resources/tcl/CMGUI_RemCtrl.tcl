# Set which CarMaker application to load
Application exe "$env(CMAPP)"

# Start this CarMaker application
Application start

# Set the saving mode
SaveMode save_all

#Set File format
#Fileformat ERG
#DStore.Format erg
#SaveFormat erg
#FileFormat erg

# If a TestSerie to simulate was specified
if $env(SIM_TS) {
	
	# Load a TestSerie
	LoadTestRun "$env(TSFPATH)"

	# -> Can be triggered by below command too, just it 
	# popups the TestMgr window too using LoadTestRun
	# TestMgr load $env(TSFPATH)

	# Start simulation of the TestSerie
	TestMgr start
	
	# Set the path to the report folder
    	set report_folder "doc"

     	#Diagram setting small defined here
	Report loadtemplate TestTemplate.cmrep
	
	# Set a convenient name for the report file
    	set RptFPath [file join $report_folder "$env(TSFNAME)"]
    	set RptFPath [file rootname "$RptFPath"]
    	set RptFPath "${RptFPath}.pdf"
	
	# Let some time to finish to prepare the report diagrams
	after 1000
	
	# Generate the report for simulated TestSerie
	Report create "$RptFPath"
}

# If a TestRun to simulate was specified
if $env(SIM_TR) {
	
	# Load a TestRun
	LoadTestRun "$env(TRFNAME)"

	# Start simulation of the TestRun
	StartSim
	WaitForStatus running
	WaitForStatus idle
}

# Reset the saving mode
SaveMode collect_only

# Close CarMaker application
Application disconnect

# If specified that APO broker daemon must be closed
if $env(STOP_ABD) {

	# Close APO broker daemon
	exec "$env(APOBD)" -stop
}

# Close Carmaker GUI
exit
