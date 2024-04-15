// Define the copyFolder function
def call(List<String> sourcePaths, String destinationPath) {
    // Iterate over each source path and copy to the destination path
    sourcePaths.each { sourcePath ->
        // Use 'bat' step to execute batch command for copying
        bat "xcopy \"${sourcePath}\" \"${destinationPath}\" /E /I /Y"
        println "Successfully copied '${sourcePath}' to '${destinationPath}'"
    }
}
