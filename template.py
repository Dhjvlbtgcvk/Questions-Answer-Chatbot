from pathlib import Path
import os 


list_of_files = [
    
    "research/test.py",
    "research/test.ipynb",
    "app.py",
    ".env",
    "requirements.txt"
]

for file in list_of_files:
   files = Path(file)
   file_dir, file_name = os.path.split(files)
   
   if file_dir and os.path.exists(file_dir):
       os.makedirs(file_dir,exist_ok=True)
   if not(os.path.exists(files)) or os.path.getsize(files)==00:
       with open(files,"w") as f:
           pass
   else:
       print(f"File already exists and is not empty: {files}")
       

    