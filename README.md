# espedite

A smart micropython codebase uploader for ESP boards

## Main Features

* Deploys full code structure (files/folders) on your board
* Allows you to specify which files to skip from the deployment process
* During development, espedite will deploy only the changed files on your board saving precious time
* Has the ability to cross-compile your code (.mpy) before deploying it to improve efficiency during importing
* Is able to uninstall (format) any code existing on the board
* Allows you to connect to the board immediately after code deployment
* Has full logging capabilities with color formatting


## Resources

Github issues list/bugtracker: https://github.com/idimitrakopoulos/espedite/issues

## Pre-requisites

* Adafruit ampy

To install ampy follow the instructions here https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy

* picocom

To install picocom on a Debian/Ubuntu box use the following command

```bash
$ sudo apt-get install picocom
```

## Quick Install

Clone the git repository in any local directory by typing the following:

```bash
user@hostname:~$ git clone https://github.com/idimitrakopoulos/espedite
```

Go to your micropython code folder

```bash
user@hostname:~$ cd mycode
```
Connect your micropython enabled ESP board (espedite assumes /dev/ttyUSB0 by default but you can specify the device path with -d)

```bash
user@hostname:~/mycode$ ../espedite/espedite.py -d /dev/ttyUSB0 -u
```

-d specifies the device path, you may change it as needed
-u will uninstall (clean-up) any code existing on your board


Now run the following to deploy your code on the ESP

```bash
$ ../espedite/espedite.py -i -C -c
```
-i Installs (deploys) your all files and folders from the working folder (plus subfolders) on the board
-C Cross-compiles all .py files into .mpy and deploys them on the board
-c Connects to the board via picocom

Other options include

-s Specify a skipfile (a text file where you can define which files must be skipped (e.g. README.md) during deployment. One line per file with relative paths required (e.g. conf/skipme.txt))
-b Specify BAUD rate to connect to your board. Default is 115200
-v Verbose mode for debugging

# License

The content of this project itself is licensed under the [Creative Commons Attribution 3.0 license](http://creativecommons.org/licenses/by/3.0/us/deed.en_US), and the underlying source code used to format and display that content is licensed under the [MIT license](http://opensource.org/licenses/mit-license.php).



Enjoy!

Iason D.
