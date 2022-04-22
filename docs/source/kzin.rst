Kzin Ring
=========

The Kzin ring provides a close approximation to an 'on-axis' illumination
source using NeAr lamps (Relco, Vernons, neon, etc.), small grain-of-wheat (GoW)
tungsten bulbs and some wide-bandwidth Blue LEDs for blue flat boost. A printed
circuit board was designed and made at JCLPCB with turn-around times of around
8 days world wide. The design uses low-cost power-supples via Amazon and EBay
for low and high voltages. The mechanical components are 3D printed. See
the Github repo for the STL and Step files. Original CAD files are in SolidWorks
and may be located there as well.


The board's design supports direct control with the FlexSpec-1 control board
or use a stand-alone Seeed Xaio board. 

The KZin control is part of our overall FlexSpec-1 automation architecture.




NeAr Calibration Lamp
---------------------

Neon (Ne) produces bright and numerous lines in the red spectral range
while Argon (Ar) produces bright and numerous lines in the blue
spectral range. For working with Hydrogen-alpha lines, a Neon lamp
is all that is needed. 

For Stellar classification, etc -- most work is in the blue area and
Argon is the cheapest better gas for lines in that area. 

Gas lamps are no longer available, being replaced by LEDs (diodes) or
EL Wire (Electroluminescent wire 600V very low current). EL Wire in
glass tubing mimics the older Neon/Gas signs to the degree that is
hard to even find artisans working with the 15KVa transformers
anymore.

The 'Relco' florescent tube ballast control lamps use a building's 'mains' current
to excite the bulb -- heating the bi-metalic strip inside the bulb. This
strip closes, and mains-current then flows to the ballast. The ballast starts
out with a high potential to get the main gas in the large tube to turn on.
Once current is flowing the main tube; the starter is starved of current, the
NeAr (gas) stops conducting, the bi-metalic strip opens and the bulb to save
that starter, the fixture lights up and Bob's your uncle. 

This is a problem for us. We want the lamp to stay on! Some bulbs do not
have this strip and pass the current to the ballast via the flow across
the electrodes. They are the bulbs best suited for the work.


.. _fluorescent:
.. figure:: images/Fluorescent_Light.png *

   A preheat fluorescent lamp circuit using an automatic starting switch. A: Fluorescent tube, B: Power (+220 volts), C: Starter, D: Switch (bi-metallic thermostat), E: Capacitor, F: Filaments, G: Ballast. `Wikipedia article <https://commons.wikimedia.org/wiki/File:Fluorescent_Light.svg>`_ .

The starter bulb has two electrodes ("C" in Figure :num`fluorescent`) that requires a high
voltage.
