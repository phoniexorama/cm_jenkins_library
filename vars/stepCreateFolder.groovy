// Define a Groovy function to create a folder in the workspace directory
def call(String folderName) {
    // Get the workspace directory path using the $WORKSPACE environment variable
    def workspacePath = System.getenv('WORKSPACE')

    // Create the folder path within the Jenkins workspace directory
    def folderPath = "${workspacePath}/${folderName}"

    try {
        // Create the folder if it does not exist
        new File(folderPath).mkdirs()

        println("Folder '${folderName}' created successfully in workspace")
    } catch (Exception e) {
        println("Error creating folder '${folderName}' in workspace: ${e.message}")
    }
}
