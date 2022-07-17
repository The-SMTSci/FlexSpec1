Using Docker
============

..
    # create a docker account (free) if you are comfortable.
    # Download the latest docker desktop and run as administrator.
    # install the latest sphinxdoc on your local machine
    docker pull sphinxdoc/sphinx-latexpdf:latest

    # update/create the documentation on your local machine

    docker run -it --rm -v "c:/git/FlexSpec1/docs:/docs" \
                        -v "$env:username/anaconda3/lib":/opt/lib \
                           sphinxdoc/sphinx-latexpdf /bin/bash
    > make html latexpdf

    open "file:///c:/git/FlexSpec1/docs:/docs/build/html/index.html"
    open c:/git/FlexSpec1/docs:/docs/build/latex/
    


A docker container is a software module, loaded into memory and
executed within its own environment. It contains both the OS image [#f1]_,
and and executables [#f2]_ for the environment. Containers may be opened
in interesting ways to share files, environments and to interoperate
with graphics in limited ways. An excellent use of containers is
to manage toolchains (cross compilers; Latex) without any impact
on the native file system. Containers may be linked, for example
one container for PostgreSQL and a separate container for its
database file images. These two may be readily shared. Protection
allows modification to the container's files, and unless actively
and overtly saved the changes are lost when the container shuts
down.

In the Flex Spec 1 project, a few containers are used.

#. Sphinx Documentation -- extended a small amount for pstricks.
#. Arduino toolchain to permit a full toolchain to run easily in batch mode using make.

To use containers:

#. Create a `Docker account <https://www.docker.com/ account>`_.
   * Through the account one gains access to a vast number of prepared images like Ubuntu, Alpine (very small Linux OS), PostgreSQL, Arduino toolchain, Sphinx etc.

#. Download and install docker.
   * The installation will tie the docker engine to your machine.

#. Use ``docker pull ...`` command to fetch a container from the Dockerhub repository

#. Use a local Dockerfile to extend and modify, or

#. Run the container as a ``bash`` command line; ``apt install`` packages, and while the container is still running ``commit`` the container.

These rather terse basic steps are well explained in online documentation. Just be wary of any GUI requirements.


Make the system
---------------

Start working with the docker file.

Docker Container Use
--------------------

.. code-block:: bash
   :linenos:

   docker run -it --rm -v $(pwd):/doc
                    -v $HOME:/root
                    --env SYSARCH=nano
                    arduino_base:v2 bash




Starting and Using Docker
=========================

.. code-block:: none

   sudo systemctl start docker

Will start the docker services.

Sphinx documentation
--------------------

.. code-block:: bash
   :linenos:

   docker run -it --rm -v ${GitREPO}/docs:/docs sphinxdoc/sphinx-latexpdf make clean latexpdf
   docker run -it --rm -v ${GitREPO}/docs:/docs sphinxdoc/sphinx-latexpdf make clean html

   Commands to rebuild the documentation.

.. literalinclude:: ../Docker/Dockerfile


Arduino Toolchain
-----------------


The toolchain is a layered container you build:

- The Ubuntu base/Docker27 file :index:`Dockerfile;toolchain;intermediate;base` brings down the main Ubuntu OS
- The intermediate/Dockerfile :index:`Dockerfile;toolchain;intermediate`, adds basic compiler and environmental support
- The support/Dockerfile :index:`Dockerfile;toolchain;support` adds support: git,zip,automake,subversion etc.
- The toolchain/Dockerfile :index:`Dockerfile;toolchain` adds the actual toolchain.

Each docker step requires a rather large amount of data transfer. Each
intermediate step, allows for mistakes and the ability to make small
corrections without a major 'from the top' repeat of previous downloads.

Each dockerfile has a comment about how to perform the step.

.. literalinclude:: ../Docker/ArduinoToolchain/base/Dockerfile
   :language: bash
   :linenos:

.. literalinclude:: ../Docker/ArduinoToolchain/intermediate/Dockerfile
   :language: bash
   :linenos:

.. literalinclude:: ../Docker/ArduinoToolchain/support/Dockerfile
   :language: bash
   :linenos:


.. literalinclude:: ../Docker/ArduinoToolchain/toolchain/Dockerfile
   :language: bash
   :linenos:


Issues
------

There are issues with cross-platform sharing of docker containers.
In this case, the sphinx-latexpdf-fs1 container is a docker image
pulled from dockerhub, and augmented with a few tools to make
tikz/pstricks work with latex. The attempt to `docker save` the container
from Linux and `docker load` the container in Win10 failed. Consultation
with a guru friend revealed his krew implements a "Docker in Docker"
way to build containers for export -- thus nailing the external dependencies.
The base of this issue is the vast size of a container and by using
the libraries in the "local" machine (user of the container's machine)
the overall size of a container could be reduced. Ha! this is right
back to why we want to use containers in the first place, and it
also driving some people to the insane idea that flatpacks, snap etc
will acutaully work. `Here <http://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/>`_ is an article to that effect.


Docker Basics
-------------

The file :code:`$HOME/.docker/config.json` holds your credentials, etc.
Adding :code:`"experimental": "enabled"` to file will enable the buildx
environment (docker 19.3/later).






.. rubric:: Footnotes

.. [#f1] OS may include various Linux operating systems, some Windows released images.
.. [#f2] The executable must be compiled for the CPU architecture, ARM vs AMD64 for example.



