```
python zipt.py -h
usage: zipt.py [-h] [-u] zip version

Create a compressed zip file and specify its version

positional arguments:
zip            The zip file which version is to be updated, or a file to create the zip from
version        A version to be put in a "VERSION.txt" file inside the zip

optional arguments:
-h, --help     show this help message and exit
-u, --updated  Insert into the zip a file "updated.txt" with the current UTC time
```
