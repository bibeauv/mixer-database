ARG SLURM_VERSION=19.05.4
FROM giovtorres/docker-centos7-slurm:${SLURM_VERSION}

ENV SLURM_VERSION=${SLURM_VERSION}
ENV PYSLURM_COMMIT_REF=0d5e23a
ENV CYTHON=0.29.14
ENV PYTHON=3.6

RUN yum install -y git && pip3 install -U pip && pip3 install --user cython==${CYTHON}

# Building pyslurm
RUN git clone https://github.com/PySlurm/pyslurm.git &&\
    git --git-dir=pyslurm/.git checkout ${PYSLURM_COMMIT_REF} &&\
    ./pyslurm/scripts/build.sh

CMD bash