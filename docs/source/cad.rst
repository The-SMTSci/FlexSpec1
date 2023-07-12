CAD Computer Aided Design
=========================

The main design cycle consists of experiments, hand sketches, capture
of the sketches into one of the main CAD packages, to produce STL
files. STL files :index:`STL files` are converted into ``gcode`` using a slicer like Cura :index:`Cura`, moved to
the printer using ``Octoprint`` :index:`Octoprint` and printed. The 3D parts are
evaluated and (altered within this cycle) as needed.

Parts are easily shared across the world, via email or the GitHub we maintained while developing the spectrograph.

Flex Spec 1 relied heavily on CAD programs:

#. SolidWorks Known to a few of the Authors from previous lives. We are currently using the Solidworks 3DConnection (maker edition)

#. Autodesk's Fusion/360 popular (indeed basis for LowSpec). Autodesk is not as freely accessible to the community as before.

#. TinkerCAD modify STL files, capture basic designs.

#. FreeCAD, a pythonic 3D parametric modeler that is well supported by its community.

#. Cura convert STL into gcode

#. KiCAD for the electrical layout. The Power Supply Board was used.

#. Octoprint, used to readily transfer gcode to the 3D printer.



