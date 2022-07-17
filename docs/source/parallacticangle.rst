Parallactic Angle
=================

In the limit, atmosphere acts like prism shaped differential element taken
from the projection of circle of uniform altitude in the spherical Horizonal
Coordinate System -- a ring of constant airmass. The lower the altitude the
higher the gradient (thicker the prism) the more the chromatic distortion
of the exoatmospheric source. The distortion is primarily along a line
from the zenith to the azimuth direction of the target.

A better way of dealing with Parallactic Angle is to realize that when
all the complicated math suggested above is condensed to practical
terms, keeping the slit 'vertical' w.r.t. local gravity is all that is needed.

To this end, the FlexSpec-1 spectrograph uses a Inertia Measurement Unit (IMU).
The small Arduino processor is oriented w.r.t. the slit in a way that one
axis is parallel to that of the slit.

QED!

The impact of the parallactic angle is one of data reduction and not of
spectrograph operation -- except to rotate the spectrograph such that the
designated axis is close to zero.

The Arduino Nano 33 BLE Sense has a 9 Degree of Freedom (DoF) IMU with
a 14 bit accellerometer readout at 2g. Zeroing out the axis (equal
force on either side of rotation) brings the instrument into alignment
with the zenith line to well within artifacts introduced by nominal
seeing.  The rotation is a Cosine-Sine function for that axis. The sin
is related to the Elevation coordinate (Elevation of zero degrees or
pointing at the horizon allows full force on the chosen axis;
elevation at the zenith means no force on the chosen axis). Coarser
tollerences are acceptable the closer to the zenith.

