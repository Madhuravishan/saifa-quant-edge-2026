$source = "C:\Users\Madhura\OneDrive\Desktop\UOC\quant_edge_project"
$destination = "C:\Users\Madhura\OneDrive\Desktop\UOC\saifa_quant_edge_1.0_submission.zip"
$tempDir = "C:\Users\Madhura\OneDrive\Desktop\UOC\temp_submission"

# Remove existing temp and zip if any
if (Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force }
if (Test-Path $destination) { Remove-Item -Path $destination -Force }

# Create temp dir
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Copy necessary files and exclude unnecessary ones
Copy-Item -Path "$source\*" -Destination $tempDir -Recurse -Exclude ".git",".venv","venv","__pycache__",".pytest_cache",".idea",".vscode","*.zip","*.log","scratch" -Force

# Compress
Compress-Archive -Path "$tempDir\*" -DestinationPath $destination

# Cleanup temp
Remove-Item -Path $tempDir -Recurse -Force
Write-Output "Zip created at $destination"
