README
======

The following few Python scripts are provided to assist with image
manipulation. In general -- the python dialect is intended to be
Python2.7/3.x agnostic. (simple enough so they may be run from within
PyRAF processes). Pandas and Astropy have issues between the dialects
and deference to Python 3x is made,


fitserial   - rename fits files by prepending "a1NNNN\_" to each name.
              Based on DATE-OBS in the header. This makes
              them list in observation order, and disambiguates
              names.

fixgain     - EXPERIMENTAL -- Fix ADU/DN add GAIN for a camera specified
              by command line or the CAMERA keyword, change the
              data. This removes the silly shift by 4 and replaces
              with an actual ADU/DN and a GAIN keyword. This requires
              characterizing your camera. It requires other aspects to
              consider like the CMOS HCD-GAIN and the offset. You may
              add small values of random noise to those
              least-significant-bits that are bull-dozed under by the
              camera firmware. This will actually improve fittings by
              blurring out systematic noise (similar to padding FFTS
              with zeros)

fixheader   - DEVELOPING: Use ".csv" files to fix headers.
              The columns KEYWORD,VALUE,COMMENT [,whatev] add/copy/delete/replaces
              keywords values in file list supplied. The columns may be
              in any order; but are case sensitive and must be
              spelled as above. A value line:

              MYLAT,!BSS-LAT,Copy BSS-LAT value for me.

              and:

              BSS-LAT,#BSS-LAT,Remove this keyword

              are additional capability. This program is python3
              only.

trim        - USe a DATASEC switch to create smaller images
              Given a region described in FITS/NOAO/pro tradition
              of, say the DATASEC keyword; trim the images.
              A prefix is prepended to files, so originals and other
              are kept. Prefix defaults to "t_". 

              The region is for FITS images (ala ds9). The coordinates
              are 1-s based (ala FORTRAN). The splat ('*' asterisk)
              stands in for the whole axis, or a part of the range
              of an axis.

              Example: "[600:*,500,700]" removes the left side and
              keeps the middle 500-700 inclusive rows. 

              Created to chop a star trace and some sky region from
              huge CMOS camera's images.

              A logical/physical WCS is added to allow ds9 to say
              how the trimmed image related back to its original.

TODO
----

* Refine operation. 

* Make sure TRIMSEC and DATASEC are done correctly.

* There may be off-by-one issues with 'inclusive' and FITS->numpy array translations.




