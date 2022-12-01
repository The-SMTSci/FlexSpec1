Automation
==========

The overall goal of the project is to utilize free (as in money)
software that is platform agnostic (capable of running or being made
to run on all operating systems). One main sub-goal is to create an
simple architecture using basic web enabled applications, inexpensive
Single Board Computers (SBCs) (Raspberry Pi running the Astroberry
suite), inexpensive Single Board Microprocessors (SBMs) like the
Arduino family of processors. Another sub-goal is to leverage the best
tools for collaboration including Github, and Sphinx -- the package
that creates this documentation tied to Readthedocs.io.

The basic philosophy is to used 'mirrored' object-oriented classes written
in Python/Bokeh for managing the instructins from its users, relaying
those instructions via JSON to C/C++ classes running on the SBM. We use
the Raspberry Pi mounted to the telescope's OTA to offer the web interface
and to direct messages to other Pi's and arduinos within the full instrumentation
for the Pier and its OTAs.



Remote Desktop
--------------

Many use the VNC Desktop |reg|, TeamViewer |reg|, Microsoft Remote
Desktop |reg| and Chromeremote |reg| are packages we have encountered
in the wild.


KStars/INDI/Ekos:

*   Windows

*   Linux:

    * Desktop

    * Raspberry/PI

    * ODroid

*   Apple

*   SAOImage/ds9 (Platform Agnostic)

*   Astrometry.net (program and )

*   Sextractor (image to data conversion)

Scripts
-------

The predominent script is bash:

`Variable substitution <https://tldp.org/LDP/abs/html/parameter-substitution.html}`_
describes the rather obtuse syntax to fix variables on the fly. Handy for removing
spaces from filenames; changing FITS file extensions from 'FTS' to 'fits' etc.

Bash is spring-loaded on Linux systems and the fastest way to do things.
It allows fast access to the utility programs like sed, awk, etc.
What takes several minutes at a DOS command line, takes but several
seconds in bash.

Networking
----------

X11/R6 The X Consortium dissolved at the end of 1996, producing a
final revision, X11R6.3. Pre-1983, known as "W" -- move to X in
1984, settled down to the X11 release in 1986.

Wayland, X Org people (2010-Current), with XWayland to tie back
to legacy systems.

Serial Port Management
----------------------

The chapter on Serial Communications covers details, Putty is the
package of choice as it is platform independent.

End-user Software
-----------------

TODO Add hyperlinks

The 3D design work was done with SolidWorks |reg|, Autodesk Fusion/360 |reg|,
TinkerCad |reg| and special modifications made with Cura |reg|.

Computer Languages
------------------

The two languages of this project are Python and C++. The C++ is the
GNU toolchain -- very consistent across platforms. The GNU compiler
suite has excellent language libraries. Some external libraries
for the Arduino are not the best in the world -- be careful there.


The Pythonic environment of choice include Anaconda and VSCode. The
Anaconda environment is widely used in Astronomy and the VSCode widely
used on Win10 environments. Both have advantages and disadvantages.
The main thing with Python is to match the very extensive libraries
more that sweat the language details. The libraries include numpy, astropy,
scipy etc.

Other languages include "bash", the Linux/Unix shell. Beware, bash on
Win10 IS NOT CONSISTENT. A handful of useful Linux utilities were used
to develop code -- not needed for run-time support.


Science
-------

Telescope and camera management:

- KStars/INDI/Ekos
- Astroberry (augmented)

Reductions were performed with 

- BASS
- Demetra
- ISIS
- VSpec
- IRAF
- PlotSpectra

Tools include
- SAOImage ds9
- fitsverify

General tools:

- Anaconda Python env, including Jupyter, Spyder etc.

Bokeh/Holoviz/Panel
-------------------

Bokeh `parameters <https://www.psych.mcgill.ca/labs/mogillab/anaconda2/lib/python2.7/site-packages/bokeh/command/subcommands/serve.py>`_ at McGill University.

TODO: Token

TODO: Authentication


Bokeh `server <https://docs.bokeh.org/en/latest/docs/user_guide/server.html>`_
instructions.

Some additional software packages need to be installed:

..  code-block:: bash
    :linenos:

    apt-get update
    apt-get -y install gcc
    pip3 install numpy
    pip3 install astropy[all]
    pip3 install pandas
    pip3 install bokeh

TODO: Cite the trademarks etc.

.. |reg|    unicode:: U+000AE .. REGISTERED SIGN
.. |copy|   unicode:: U+000A9 .. COPYRIGHT SIGN


Python
------

The FlexSpec1 project makes extensive use of Python3 and many support packages.
In particular the Flask/Bokeh combination for the front-end GUI like WEBAPP.
Other utility programs the team developed are included.

See the `Official PEP <https://peps.python.org/pep-0420/>`_ Python
Extension Proposals (the actual rules of python).  Pay attention to
PEP 0, for the coding standards, we mostly follow.


Other Packages
--------------

Here is a collectin or very random links to other coding projects.

Mostly in PERL
`DragonFly <https://github.com/robertoabraham/ProjectDragonfly/tree/master/scripts>`_
