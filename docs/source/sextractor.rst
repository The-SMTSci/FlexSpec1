Sextractor
==========

Sextractor relies on default files to guide its extraction of objects
from files.

There are 4 files:

#. default.sex   - details about seeing/ota/gain etc. Take this 'quiz'

#. default.param - the values you want back from sextractor ~400 of them

#. default.conv  - a NxN convolution matrix (PSF). They have examples

#. default.nnw   - a neural net to recognize things. No idea.
                Too Dense; Did Not Think.

.. code-block::

    ALPHAWIN_SKY             Windowed   ...  [deg]
    DELTAWIN_SKY             Windowed   ...  [deg]
    X_IMAGE                  Object po  ...  [pixel]
    Y_IMAGE                  Object po  ...  [pixel]
    FWHM_IMAGE               FWHM assu  ...  [pixel]
    FWHM_WORLD               FWHM assu  ...  [deg]
    ELONGATION               A_IMAGE/B  ...
    ELLIPTICITY              1 - B_IMA  ...
    FLUX_ISO                 Isophotal  ...  [count]
    FLUXERR_ISO              RMS error  ...  [count]
    ISOAREA_IMAGE            Isophotal  ...  [pixel**2]
    BACKGROUND               Backgroun  ...  [count]
    THRESHOLD                Detection  ...  [count]
    #NUMBER                  Running object number


Basic Tricks
------------

#. Sextractor is designed to find things: any size any orientaion,
   anywhere. So you want the FWHM_x, ELLIPTICITY and ELLIPTICITY to
   disambiguate stars from stuff. Sextractor started out classifying
   oddly shaped galaxies -- so be careful with output. It finds 'dark'
   areas so FLUX is a handy disambiguator.

#. The .param file, simply COPY param lines from bottom up to the
   top and remove the leading sharp (#). Thus you can
   recover, change mind etc by deleting the 'un-sharped' lines
   as the original image of that lines remained lower in the file.

#. The NxN matrix may have to be bigger with small pixels
   on some amateur small telescopes. Pretty easy to make
   with something like Astropy.

#. If you run the .param file above on a non-solved
   image, ALPHAWIN_SKY, and DELTAWIN_SKY are just
   zeros which is livable!

#. Put the default files in the dir, or soft link
   to a set (what I do -- I maintain several sets
   for various classes of telescopes). 

#. Of late, Sextractor on GitHUB leverages ATLAS, CBLAS
   etc, and that is hard to compile from a bookkeeping
   point of view. 

Discussion
----------

One may  'ln -s' to the set of default.x file for
sky and scope. AN uses it, solves the file. The .new produces
a catalog with RA/DEC etc to match to, say UCAC 4 or Landolt
fields. Viola photometry! Salt to taste.

FLUX_ISO < 10,000 reject non-1% photometry.

ELONGATION A/B close to 1

ELLIPTICITY is 1-ELONGATION. It also serves  as a check for star like things.

FWHM_x where you want it: They are pretty close to each other for stars.

You may use a python code for this. Take the time to match the column
names to the columnar positions. Use X and Y IMAGE to avoid the chip
edges.

If you put ALPHAWIN_SKY, and DELTAWIN_SKY in columns 1 and 2 then
SAOImage/ds9 will be very happy.

The columnar output is almost always a string that is float/int or
INDEF. That INDEF is a pain, but can be dealt with.

Resources
---------

The source/manual is well worth the study. It is on GitHub:

https://github.com/astromatic/sextractor

...and using readthedocs tricks, access the online manual or download
your own PDF....

https://sextractor.readthedocs.io/

https://sextractor.readthedocs.io/_/downloads/en/latest/pdf/

My head is into this now for a project. 




