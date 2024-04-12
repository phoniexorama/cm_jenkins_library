import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption

// Define a Groovy function to copy a file or directory
def call(String sourcePath, String destinationPath) {
    Path source = Paths.get(sourcePath)
    Path destination = Paths.get(destinationPath)

    try {
        // Copy the file or directory
        Files.copy(source, destination, StandardCopyOption.REPLACE_EXISTING)

        println("Successfully copied '${sourcePath}' to '${destinationPath}'")
    } catch (IOException e) {
        println("Error copying '${sourcePath}' to '${destinationPath}': ${e.message}")
    }
}
