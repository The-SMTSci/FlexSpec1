FlexSpec Simple Main.
---------------------

**The Structure of the Files:**

SolidWorks™, used as the main CAD software, wants paths that come down from
a windows drive. Every one has C: so might as well feature that drive. The
path we chose is:

C:\git\FlexSpec1\CAD\... 

where the ... are major sub-components of the design.

This Github Repo should be placed at C:\git\FlesSpec1 on Windows systems.

For Linux users, and any non-SolidWorks people, you can clone the repository
anywhere you like.

The docs directroy contains the Sphinx sources needed to produce the
documentation found a:

[readthedocs](https://flexspec1.readthedocs.io/en/latest/).

The EDA (Electronic Design Automation) directory holds schematics
and other electronic/electrical details.

**The Code/FlesSpec Tree**

'Camera lens holder'
Collimating_lens_holder
Grating_Holder
Guide_mirror_holder
Main_mirror_holder


The simple main program "FlexSpec" is started with:

bokeh serve FlexSpec.py --unused-session-lifetime 3600000

**--unused-session-lifetime 3600000** allows one hour of idle time.


