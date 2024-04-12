import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption
import java.util.List

// Define a Groovy function to copy multiple files or directories
def call(List<String> sourcePaths, String destinationPath) {
    Path destination = Paths.get(destinationPath)

    try {
        sourcePaths.each { sourcePath ->
            Path source = Paths.get(sourcePath)
            // Resolve the source file/directory name for the destination path
            Path resolvedDestination = destination.resolve(source.getFileName())

            // Copy the file or directory
            Files.copy(source, resolvedDestination, StandardCopyOption.REPLACE_EXISTING)

            println("Successfully copied '${sourcePath}' to '${resolvedDestination}'")
        }
    } catch (IOException e) {
        println("Error copying files/directories: ${e.message}")
    }
}
