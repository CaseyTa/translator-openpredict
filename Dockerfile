FROM jupyter/all-spark-notebook:python-3.8.8
# FROM jupyter/all-spark-notebook:spark-3.1.1
# FROM jupyter/pyspark-notebook
# Without Spark: FROM python:3.7 

# Required to be able to edit the .joblib model directly in the python package
USER root
WORKDIR /root

RUN apt-get update && apt-get install -y build-essential

# RUN fix-permissions $CONDA_DIR && \
#     fix-permissions /home/$NB_USER

# USER $NB_USER

ENV OPENPREDICT_DATA_DIR=/data/openpredict
ENV PYSPARK_PYTHON=/opt/conda/bin/python3
ENV PYSPARK_DRIVER_PYTHON=/opt/conda/bin/python3

# Install from source code
COPY . .
RUN pip install .

EXPOSE 8808
ENTRYPOINT [ "openpredict", "start-api" ]