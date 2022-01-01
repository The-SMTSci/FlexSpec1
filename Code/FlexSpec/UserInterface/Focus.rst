Focus
=====


Given a path to a directory with focus test images and corresponding sextractor
catalog files. Assume the x,y's match to a pixel.

We want a image that shows the best focus of the batch and the sequence number
for that match.

https://stackoverflow.com/questions/62227786/how-to-create-bokeh-plots-with-image-in-background

sexprep # get links to the main definitions this instrument
for f in default.*; do cp $f xxx; mv xxx $f; done # make hard links to be safe

Open the images and make a cube. (sparse essentially the centroid locations)
make 'view' (image) as mean and std of 
