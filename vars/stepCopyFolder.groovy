// Function to copy folders using 'bat' step
def call(sourceDestinationMap) {
    sourceDestinationMap.each { sourcePath, destinationPath ->
        // Use 'bat' step to execute Windows command for copying
        bat "xcopy /E /I /Y \"${sourcePath}\" \"${destinationPath}\""
        println "Successfully copied '${sourcePath}' to '${destinationPath}'"
    }
}
