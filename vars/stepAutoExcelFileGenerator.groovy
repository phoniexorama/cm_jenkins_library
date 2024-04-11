def call() {
    // Fetch Python script content from library resource
    def pythonContent = libraryResource('scripts/autoexcelfilegenerator.py')

    // Write Python script to a file in the Jenkins workspace
    writeFile(file: 'autoexcelfilegenerator.py', text: pythonContent)

    // Use correct file path separator for Windows
    def pythonScriptPath = "${env.WORKSPACE}\\autoexcelfilegenerator.py"

    // Execute Python script using Python interpreter (python or python3) depending on your setup
    // Make sure 'python' is in the system PATH or provide full path to the Python interpreter
    bat "python ${pythonScriptPath}"
}
