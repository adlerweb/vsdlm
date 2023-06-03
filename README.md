# vsdlm
A Very Simple Download Manager

## What it is

This script will read URLs line by line from a text document, and download each address. Nothing more, nothing less.

## How to use

Start the script. It will start looking at **in.txt** for URLs. Add whatever you want.

Tipp: On bash add an alias like ``alias dl='echo "$1" >> in.txt'``.

you can also create a file called **exit.txt** to exit after finishing the current download, even if there are more URLs present. The script will remove the file when exiting.

## Things worth knowing

* Yes, it will always use the current folder
* Yes, it will retry as long as the predicted file size isn't downloaded
  * Yes, this might cause loops and kill kittens
* The current URL is written to a file called **current.txt**. If something fails you can find the last URL there (keep in mind: It's already deleted from *in.txt*). If a **current.txt** is present while starting the script, it will try to resume the download

## Who wrote it?
Mostly ChatGPT, as you can probably tell ;)

## What to expect?
Nothing but bugs.