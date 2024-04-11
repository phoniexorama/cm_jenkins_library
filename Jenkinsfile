@Library('cm_shared_library') _
pipeline {
    agent {
        label 'CarMakerServer' // Label for Windows agent
    }
    environment {
        TEMPLATE_FOLDER_PATH = "${WORKSPACE}\\Data\\TestRun\\Lenkwinkelrampe_Template"
        TEMPLATE_FILE = "${WORKSPACE}\\Template.ts"
        DESTINATION_FOLDER = "${WORKSPACE}\\Data\\TestRun"
        VEHICLE_FOLDER_PATH = "${WORKSPACE}\\Data\\Vehicle"
        OUTPUT_FOLDER = "${WORKSPACE}\\SimOutput\\ENGPMAKNB022"
        LOG_FOLDER = "${WORKSPACE}\\SimOutput\\ENGPMAKNB022\\Log"
        VFF_FOLDER_PATH = "${WORKSPACE}\\Data\\Vehicle"
        DAT_FOLDER_PATH = "${WORKSPACE}\\SimOutput\\ENGPMAKNB022\\log"
        EXCEL_FOLDER_PATH = "${WORKSPACE}\\VehicleInfoExcel"
        BATCH_SCRIPT_PATH = "${WORKSPACE}\\carmakerTestseries.bat"
        TEST_SERIES_FOLDER_PATH = "${WORKSPACE}\\Data\\TestRun"
        FORMAT_FILE_CONFIG_PATH = "${WORKSPACE}\\Data\\Config\\Lenkwinkelrampe_Temp"
    }

    stages {
        
        stage('dat file generation') {
            steps {
                script {
                    // Call the Python script for dat file generation
                    //bat "python carmakerdatfilegenerator.py"
                    stepCarMakerDatFileGenerator()
                }
            }
        }

        stage('excel file generator') {
            steps {
                script {
                    // Call the Python script for excel file generation
                    //bat "python autoexcelfilegenerator.py"
                    stepAutoExcelFileGenerator()
                }
            }
        }

        stage('test series generator') {
            steps {
                script {
                    // Call the Python script for test series generation
                    //bat "python testseriesgenerator.py"
                    stepTestSeriesGenerator()
                }
            }
        }
        
        stage('run test manager') {
            steps {
                script {
                    // Call the Python script for running test manager
                    //bat "python runtestmanager.py"
                    stepRunTestManager()
                }
            }
        }
    }
}
