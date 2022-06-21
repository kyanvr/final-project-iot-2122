from distutils.core import setup
from glob import glob
import os
import py2exe

data_files = []

Mydata_files = []
for files in os.listdir('C:\\Users\\kyanv\\LocalDev\\AHS-IoT\\final-project-iot-2122\\assets'):
    f1 = 'C:\\Users\\kyanv\\LocalDev\\AHS-IoT\\final-project-iot-2122\\assets' + files
    if os.path.isfile(f1):
        f2 = 'images', [f1]
        Mydata_files.append(f2) 

setup(
    console=['flappySnake.py'],
    data_files = data_files
)
