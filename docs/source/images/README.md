README.md
=========

2022-07-17T11:34:41-0600

This directory has images that are placeholders for final release.

docker run -it --rm -v $(pwd):/home texlive/texlive /bin/bash

# Start in the main dir:
# /home/git/external/SAS_NA1_3D_Spectrograph/docs/source/images == pwd
# run the commands by hand.
latex refractionlaw.tex && dvips refractionlaw.ps


