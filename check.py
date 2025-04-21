import os

# Check if the script's directory is writable
if os.access('.', os.W_OK):
    print("You have write permission for this directory.")
else:
    print("Write permission denied.")
