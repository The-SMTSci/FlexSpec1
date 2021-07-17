FlexSpec Initial README
-----------------------

**The Structure of the Files:**

This Github Repo should be placed at C:\git\FlesSpec1 on Windows systems.

The main Python development environment is **conda** from Anaconda.com.
This requirement is used because it may be installed in one go.

SolidWorks™ was used as the main CAD software and runs under Microsoft's Windows 10™
environment. The program wants file paths that come all the way down from a Windows
drive. Everyone has **C:** so we might as well feature that drive. The path we chose is:

**C:\git\FlexSpec1\CAD\...** 

where the elpisis (...) holds major components of the design. The **CAD** directory
has components like:

'Camera lens holder'
Collimating_lens_holder
Grating_Holder
Guide_mirror_holder
Main_mirror_holder

For Linux users, and any non-SolidWorks people, you can clone the repository
anywhere you like.

The **Rule** is for to include all CAD source files, assemblies, drawings
and PDFs that facilitate understanding and building the FlexSpec1 or
adapting these components to custom spectrograph needs.

**DOcumentation**

The docs directroy contains the Sphinx sources needed to produce the
documentation found a:

[readthedocs](https://flexspec1.readthedocs.io/en/latest/).



**Electronics**

The EDA (Electronic Design Automation) directory holds schematics
and other electronic/electrical details.

**Simple usage**

The simple main program "FlexSpec" is started with:

bokeh serve FlexSpec.py --unused-session-lifetime 3600000

**--unused-session-lifetime 3600000** allows one hour of idle time.


