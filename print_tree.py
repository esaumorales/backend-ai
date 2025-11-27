import os

print("=== FILE TREE ===")
for root, dirs, files in os.walk(".", topdown=True):
    print(root, dirs, files)
