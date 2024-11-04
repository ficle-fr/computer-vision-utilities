## Computer vision utilities
This repository is for publishing small functions and utilities that help me write more complex components for various projects. Unfortunately, I find myself needing to write such functions almost every day, but now I plan to solve this by organizing them all in one place.

-----
### lsimgs
This simple utility prints the properties of images in a specified folder.

Example Usage:

`python3 lsimgs.py ~/images`

or, to filter by a specific format (e.g., TIFF):

`python3 lsimgs.py ~/images -t tiff`

-----
### fft2filter
A program that filters images using fft.

Depending on the optional argument `-t` or `--ftype`, this can be a low-pass or high-pass filter. If you don't specify anything, it's a high-pass filter. 

You can adjust the threshold by changing the [variable](https://github.com/ficle-fr/computer-vision-utilities/blob/267b48597478e54ddd4c5ebe9f1f91073f77a37b/fft2filter/fft2filter.py#L25C5-L25C10)

Example Usage:

`python3 fft2filter.py input.tif output.tif -t low -v 2`

`python3 fft2filter.py input.tif output.tif -v 1`


