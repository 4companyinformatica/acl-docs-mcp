import os
import pathlib
import shutil


# Guard Rails! Mind the gap...
check_list = [
    'src',
    'util',
    'main.py'
]

for item in check_list:
    if not os.path.exists(item):
        raise FileNotFoundError(f"Error: {item} not found.")
root = pathlib.Path(".")
print("I'm on root! Let's go!")


all_py_caches = list(root.rglob("**/__pycache__")) # Get all pycaches in root

py_caches_to_remove = [ # Don't mess with venv files, don't know what those mf do
    item
    for item in all_py_caches
    if '.venv' not in item.parts
]

for item in py_caches_to_remove: # Deleting pycaches
    print(f"Removing {item}...")
    shutil.rmtree(item)