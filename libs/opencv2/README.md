# openCV 3.1.0 for ODROID XU4

This contains openCV 3.1.0 binaries and library for python3.5 developers. This may work only in a specific platform and does not guarantee on other system configurations.

The target configurations are
* 32-bit ARM-based CPU
* Ubuntu 16.04
* Python 3.5

To install,
```bash
# root access is required
./install.sh
```
The installation requires Internet connection as it installs depedencies. For python3.5 users type the code below to check if the installation is successful.
```
$ python3
>>> import cv2
>>> cv2.__version__
'3.1.0'
```