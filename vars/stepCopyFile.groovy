// Define a function to copy a file from sourcePath to targetPath
def call(String fileName, String sourcePath, String targetPath) {
    def fileContent = libraryResource(sourcePath)
    
    if (fileContent == null) {
        error "Failed to load file content from path: ${sourcePath}"
    }
    
    def targetFilePath = "${targetPath}/${fileName}"
    
    writeFile(file: targetFilePath, text: fileContent)
    
    echo "File '${fileName}' copied to workspace: ${targetFilePath}"
}
