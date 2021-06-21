# Extend the sphinxdoc/sphinx-latexpdf-astropy to support Python docs
# add the gcc too -- this permits docs of c++ code.
# astropy[all] drags in its dependencies
# docker build -t sphinx-latexpdf-astropy .
# docker ps # look for the container to commit
# docker stop xxxxxxxxx
# docker commit sphinxdoc/sphinx-latexpdf sphinxdoc/sphinx-latexpdf-astropy


FROM sphinx-latexpdf

WORKDIR /

RUN apt-get update
RUN apt-get install gcc
RUN pip3 install astropy[all]
RUN pip3 install pandas
RUN pip3 install bokeh



