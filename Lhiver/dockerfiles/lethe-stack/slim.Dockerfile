FROM lethe as builder
FROM centos:7

# OS Dependencies
RUN set -ex \
    && yum makecache fast \
    && yum -y update \
    && yum -y install epel-release \
    && yum -y install \
        blas64 \
        # boost \
        lapack \
        lapack64 \
        libgfortran4 \
        openmpi3 \
        zlib \
    && yum clean all \
    && rm -rf /var/cache/yum

# Copy compiled software and libraries
COPY --from=builder /opt/dealii /opt/dealii
COPY --from=builder /opt/lethe /opt/lethe
COPY --from=builder /opt/numdiff /opt/numdiff
COPY --from=builder /opt/p4est /opt/p4est
COPY --from=builder /opt/trilinos /opt/trilinos

# Set .bashrc
RUN set -ex \
    && echo "module load mpi/openmpi3-x86_64" >> ~/.bashrc \
    && echo 'export PATH=$PATH:/opt/lethe/bin' >> ~/.bashrc

CMD gls_navier_stokes_3d