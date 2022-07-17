..
    extend sphinx-latexpdf docker container with the Dockerfile in the
    root of this repo
   
    apt-get update
    apt-get -y install gcc
    pip3 install numpy
    pip3 install astropy[all]
    pip3 install pandas
    pip3 install bokeh
   
    docker run -it --rm -v /home/git/external/SAS_NA1_3D_Spectrograph/docs:/docs \
                        -v /home/wayne/anaconda3/lib:/opt/lib \
                           sphinxdoc/sphinx-latexpdf /bin/bash
   
    docker run -it --rm -v /home/git/external/SAS_NA1_3D_Spectrograph/docs:/docs \
                           sphinxdoc/sphinx-latexpdf-fs1 make html
   
   
    docker run -it --rm -v /home/git/external/SAS_NA1_3D_Spectrograph/docs:/docs \
                        -v /home/wayne/anaconda3:/opt/lib \
                        -e PYTHONPATH=/home/wayne/anaconda \
                           sphinxdoc/sphinx-latexpdf make html latexpdf

    docker run -it --rm -v /home/git/external/FlexSpec1/docs:/docs \
                        -v /home/wayne/anaconda3/lib:/opt/lib \
                           sphinxdoc/sphinx-latexpdf /bin/bash

    browser build/html/index.html
   
    /home/wayne/anaconda3/bin
    /home/wayne/anaconda3/condabin

INTRODUCTION
============

.. figure:: images/FS1_Assembly_with_Baffle.jpeg

   CAD Layout for optical components of the FlexSpec 1.

The spectroscopist wants what they want. The spectrograph gives what
it will. One must strike the Faustian bargain that may only be paid
with the coin of credibility. Choose wisely.



The FlexSpec1 (FS1) spectrograph grew out of a segmented analysis of
the entire impact on a spectrum starting with the Source signal; through a
telescope's optical tube assembly (OTA); through the focal plane;
through the spectrograph; and into the sensor. This article limits all
variables from the Source to the OTA to one parameter: the `Parallactic
Angle`_. 

to those involving the impact of the atmosphere
(parallactic angle), the effective focal length of the main OTA, and
relationship of the OTA to the device injecting a calibration lamp
signal (Herein the Kzin ring).

Only the flux distortions taking place between the Source (a Star, Planet,
Calibration Lamp) are considered up to the

Ramifications of 3D printing leading to FlexSpec 1 (FS1): 
Introducing the Flexible Spectrograph I
Small Telescope Spectrograph.

This is documentation, the project and our aspirations for developing
a science data quality 3D spectrograph that is 'Flexible'.

It is a continuous in progress. Bear with us. Better yet, collaborate with us.

The STL and STEP files, EDA and CAD files and the software
may be cloned from the `FlesSpec1 Github Repository <https://github.com/The-SMTSci/FlexSpec1>`_ here.



.. toctree::
   :maxdepth: 3
   :numbered:
   :caption: Contents:

   abstract
   flexspec1
   openquestions
   kzin
   ovio
   parallacticangle
   optics
   experiments
   overview
   physics
   mathematics
   guiding
   protocol
   controls
   communication
   serial
   software
   postmaster
   cad
   electronics
   arduino
   documentation
   docker
   bom
   callamps
   outstanding
   history
   references
   youtube
   printer
   merlin
   
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. 
   docker run -it --rm -v /home/git/external/SAS_NA1_3D_Spectrograph/docs:/docs                         sphinxdoc/sphinx-latexpdf-fs1 make html latexpdf
