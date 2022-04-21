OVERVIEW
========

This documentation has all :ref:`bill-of-materials<flexspec1-bom>` and in-depth discussion of
the concepts, development, technical and scientific aspects of
Flexspec 1. "Flexible" is "Flexible". A concrete example
of the Flexspec 1 is presented but the ideas, CAD drawings, 
software and documentation are available in the public-domain
for vendors and fellow small telescope scientists to use and
enjoy.

During an after-meeting in Flagstaff, AZ in late 2018 a few of the
authors met and developed the idea of leveraging Paul Gerlach's
LOWSPEC 3D Printed spectrograph as a means of gaining more data from
the small telescope community. In early 2019, at the Sacramento
Mountains Spectroscopy Workshop II in Las Cruces NM the decision was
taken to refine 3D printed spectrographs. This collaboration will
continue beyond this paper.

The Flexspec 1 small instrument operating as a full peer within a
network of sites with other instruments.  Flexspec employs multiple
control components and can share its state-of-affairs with other
interested control elements throughout its associated networks. For
example, one does not start a deep spectral exposure while a neighbor
in a roll-off building is taking dome flats. We made an attempt to
design a control messaging architecture to address the full
control/scheduler issue. Those implementation details will be
addressed in future. See Section :ref:`Controls<fs1-control>`.

Adding automated control elements such as motors, sensors, and
switches to a spectrograph were driven by experience and issues with
other instruments.

Issues include:

- **Thermal Expansion:** The complete thermal range is from daytime 118F to nighttime -20F depending on the season. 3D Plastics have high thermal expansion coefficients. 
- **Flexture:** PLA/Plastics are highly flexible. Threads are unreliable.
- **Focus:** Temperature changes across a night, bench setup.
- **Seeing:** Seeing conditions are variable as small telescope work is done deep in the atmosphere.
- **Parallactic Angle:** Always a concern. The Arduino Nano Sense 33 IoT (BLE) provides rotator feedback.
- **Remote use:** Here Office to backyard was the goal, architecture was global.

During 2020 we became aware of thermal and structural issues. Yeager
did the bulk of these experiments in the the cold Colorado winter.
This year's work concentrated on the math, physics, optics, and
engineering aspects of the spectrograph. There have been requests for
accommodating apertures beyond the nominal 11-inch SCT telescopes, to
include short-focus (f/5 - f/8) instruments; and apertures in the
ranges of 36-60cm and beyond.

..  index::
    single: issues;thermal
    single: issues;flexure

Matching the slit size to focal length and seeing. TODO Move this table.

    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |Aperture  | f/ratio  |  fl     |   Magic        | Seeing (arcsec)                             |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |(inch)    | (inch)   |  (mm)   |"/:math:`\mu{m}`|      1    |     2    |     3    |      4    |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |6         | 5        |   735   |   0.28063      |   3.56338 | 7.12676  | 10.69014 |  14.25352 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |6         | 6.7      |   984.9 |   0.20943      |   4.77493 | 9.54986  | 14.32479 |  19.09972 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |6         | 8        |  1176   |   0.17540      |   5.70141 | 11.40282 | 17.10423 |  22.80564 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |8         |  5       |   980   |   0.21047      |   4.75117 | 9.50235  | 14.25352 |  19.00470 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |8         |  6       |  1176   |   0.17540      |   5.70141 | 11.40282 | 17.10423 |  22.80564 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |8         | 10       |  1960   |   0.10524      |   9.50235 | 19.00470 | 28.50705 |  38.00939 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |11        |  5       |  1347.5 |   0.15307      |   6.53286 | 13.06573 | 19.59859 |  26.13146 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |11        | 11       |  2964.5 |   0.06958      |  14.37230 | 28.74460 | 43.11691 |  57.48921 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |12        |  4       |  1176   |   0.17540      |   5.70141 | 11.40282 | 17.10423 |  22.80564 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |12        | 13.5     |  3969   |   0.05197      |  19.24226 | 38.48451 | 57.72677 |  76.96902 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |14        |  6.7     |  2298.1 |   0.08975      |  11.14150 | 22.28301 | 33.42451 |  44.56601 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |14        |  8       |  2744   |   0.07517      |  13.30329 | 26.60658 | 39.90986 |  53.21315 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |16        |  4       |  1568   |   0.13155      |   7.60188 | 15.20376 | 22.80564 |  30.40752 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |16        | 13.5     |  5292   |   0.03898      |  25.65634 | 51.31268 | 76.96902 | 102.62536 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |24        |  4       |  2352   |   0.08770      |  11.40282 | 22.80564 | 34.20845 |  45.61127 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
    |24        |  8       |  4704   |   0.04385      |  22.80564 | 45.61127 | 68.41691 |  91.22255 |
    +----------+----------+---------+----------------+-----------+----------+----------+-----------+
   
    Table of focal lengths matching slit widths with seeing.

.. index::
   single: seeing;slit width

..
   % (iv (setq tmp (* 14 2.54 )))    35.56  
   % (iv (setq tmp (* 24 2.54 )))    60.96  
