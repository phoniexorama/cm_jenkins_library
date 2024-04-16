@ECHO OFF
REM Deactivation of standard echoing of each command, 
REM even comment commands (REM), (ECHO OFF) without echoing about it (@)

REM By the way, this is a comment line since it begins with REM

REM Remind to use the Windows convention as separator folder in path
REM in batch specific commands (backslash \ instead of forward slash / )

REM CarMaker specific parts

REM 0) The CarMaker installation folder
SET CMDIR=%IPGHOME%\carmaker\win64-12.0.2

REM 1) The CarMaker GUI
SET CMEXE=%CMDIR%\bin\CM.exe

REM 2) APO broker daemon (automatically started, just if needed to close it)
SET APOBD=%CMDIR%\bin\apobrokerd.exe

REM 3) The CarMaker project, this sets the Tcl variable HIL(ProjDir)
SET CMPRJDIR=C:\CM_Test\Frg-Bedatung_Cayenne_E4_CM12

REM 4) The (project related) path of the CarMaker application
REM    to calculate the simulation
REM SET CMAPP=src/CarMaker.win64.exe
REM -> To use standard application of the installation folder:
SET CMAPP=CarMaker.win64.exe

REM 5) Some TestSerie and TestRun example to be simulated
SET TSFNAME=PO546_E4_Cayenne_SUV_TOP_VFF.ts
SET TSFPATH=C:/CM_Test/Frg-Bedatung_Cayenne_E4_CM12/Data/TestRun/%TSFNAME%

REM 6) The Tcl script to remote control the CarMaker GUI
SET TCLFNAME=CMGUI_RemCtrl.tcl
SET TCLFPATH=C:/CM_Test/Frg-Bedatung_Cayenne_E4_CM12/Data/Script/Examples/%TCLFNAME%

REM 7) Control flags
SET SIM_TS=1
SET SIM_TR=0
SET STOP_ABD=1

REM Lauch CarMaker GUI:
"%CMEXE%" -cmd "source %TCLFPATH%"
