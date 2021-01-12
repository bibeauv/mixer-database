FROM lhiver

#ENV SLURM_VERSION=${SLURM_VERSION}
#ENV PYSLURM_COMMIT_REF=0d5e23a
#ENV CYTHON=0.29.14
#ENV PYTHON=3.6

# OS Dependencies
#RUN yum

# Python dependencies
COPY requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt

CMD bash