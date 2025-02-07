import os
import subprocess

data_directory = './tests/fixtures/data'

for filename in os.listdir(data_directory):
    file_path = os.path.join(data_directory, filename)
    if os.path.isfile(file_path):
        command = f'python manage.py packages -o import_business_data -s {file_path} -ow overwrite'
        subprocess.run(command, shell=True)