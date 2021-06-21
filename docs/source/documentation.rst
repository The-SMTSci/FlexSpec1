Documentation
*************

This section holds the technical details to produce and extend
the Flex Spec 1 documentation.

It relies on the texlive docker container. 

Make a subdir under the usual sphinx directory called documentation
and put the .tex files related to images etc there. Using the container
make the images. Some additional processing may be needed. Then
move the final images to doc/source/images and run the other
docker container sphinx-latex-fs1. This makes the overall
readthedocs files. The sphinx-latex-fd1 container has the regular
sphinx-latexpdf container augmented with astropy, numpy and other
necessary files.

Note: There is a way to fake sphinx into accepting inaccessible
modules and ignore them.

Next door to the docs dir, create a FS1Code directory and move
code copies there. This protects the files from other aspects
of the system. Judicious use of __init__.py files will create
the illusion of code in a way that Sphinx expects. This gets
complicated -- witness the astropy documentation approach.
Ugh.

.. code-block:: bash

   docker run -it --rm -v /home/$(USER)/git/FlexSpec1/docs/documentation:/home \
      texlive/texlive /bin/bash

   cd /home
   latex ... # output goes to /home/$(USER)/git/FlexSpec1/docs

Then within the command prompt you can run commands.

Here the example is for making the art.

Use commands like:

.. code-block:: bash

   > latex exa100.tex
   > dvips exa100.ps

To produce a postscript file.

Currently, the docker texlive-latest has pstricks working.




