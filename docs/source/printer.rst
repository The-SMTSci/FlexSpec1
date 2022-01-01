Printer
======

3D Printer Calibration
Jerry Foote Oct 21, 2021

This procedure assumes that OctoPrint is attached and running. To send commands select
“Terminal” at the top of the screen and use the “Send” button to send the command to the
printer.

# Send M503 command. Look for the M92 line and and note Current values for X, Y, Z and E.

# Using printer controls heat up extruder temp to 190C for PLA or 245C for PETG.

# Mark length of filament at 100mm & 120mm from the filament guide.

# When hot, send command: G1 E100 F100

# After the filament is extruded measure how much was extruded. If less than 100mm note how much, if more than 100, use 120 mark and compute how much. This is “ActualE”.

# From the M92 command get the value for “E”= CurrentE.

# Compute the new value for “E”, NewE= (100/ActualE)* CurrentE

# Send M92 ENewE

# Print 20 cm cube. https://www.thingiverse.com/thing:1278865

# Measure X, Y, Z dimensions (X is right to left, Y is front to back and Z is verticle)

# Compute New X = (20/ActualX) * CurrentX

# Compute New Y = (20/ActualY) * CurrentY

# Compute New Z = (20/ActualZ) * CurrentZ

# Send M92 XNewX YNewY ZNewZ This command should format like the M92 command previously but with the new values.

# Send M500 which saves these values.

# Repeat process and fine tune values.
