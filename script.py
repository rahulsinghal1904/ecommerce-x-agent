import subprocess
import tempfile
import os

# Corrected AppleScript string
script = '''tell application "Google Chrome"
    activate
    delay 2
    tell front window to set theTab to active tab
    tell theTab 
        execute JavaScript "document.querySelector('#login2').click();"
    end tell
end tell'''

# Create a temporary AppleScript file
with tempfile.NamedTemporaryFile(mode="w", suffix=".applescript", delete=False) as f:
    script_path = f.name
    f.write(script)

print("Using temporary AppleScript file:", script_path)

# Ensure the file was written correctly
with open(script_path, "r") as f:
    file_content = f.read()
    print("AppleScript file content:\n", file_content)

# Run the AppleScript file
result = subprocess.run(
    ["osascript", script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Clean up temporary file
os.remove(script_path)

# Print outputs
print("Return code:", result.returncode)
print("STDOUT:", result.stdout.strip())
print("STDERR:", result.stderr.strip())
