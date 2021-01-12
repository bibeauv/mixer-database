FROM centos:7

ARG NUMDIFF_VERSION=5.9.0
ARG P4EST_VERSION=2.2
ARG TRILINOS_VERSION=12-18-1
ARG TRILINOS_BUILD_JOBS=1

# OS Dependencies
RUN set -ex \
    && yum makecache fast \
    && yum -y update \
    && yum -y install epel-release \
    && yum -y install \
        blas64-devel \
        boost-devel \
        cmake3 \
        file \
        gcc \
        gcc-c++\
        git \
        lapack64-devel \
        lua-devel \
        make \
        nano \
        openmpi3-devel \
        wget \
        zlib-devel \
    && yum clean all \
    && rm -rf /var/cache/yum

# numdiff
RUN set -ex \
    && mkdir -p /tmp/numdiff \
    && wget -qO /tmp/numdiff/numdiff.tar.gz "https://mirrors.sarata.com/non-gnu/numdiff/numdiff-$NUMDIFF_VERSION.tar.gz" \
    && wget -qO /tmp/numdiff/numdiff.tar.gz.sig "https://mirrors.sarata.com/non-gnu/numdiff/numdiff-$NUMDIFF_VERSION.tar.gz.sig" \
    && export GNUPGHOME="$(mktemp -d)" \
    && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys 23756380 \
    && gpg --batch --verify /tmp/numdiff/numdiff.tar.gz.sig /tmp/numdiff/numdiff.tar.gz \
    && tar -xf /tmp/numdiff/numdiff.tar.gz -C /tmp/numdiff/ \
    && cd "/tmp/numdiff/numdiff-$NUMDIFF_VERSION" \
    && ./configure \
    && make -j `nproc` \
    && make install \
    && rm -rf "${GNUPGHOME}" /tmp/numdiff \
    && numdiff --version

# p4est
RUN set -ex \
    && mkdir -p /tmp/p4est \
    && wget -qP /tmp/p4est/ "https://www.dealii.org/current/external-libs/p4est-setup.sh" \
    && wget -qP /tmp/p4est/ "https://p4est.github.io/release/p4est-$P4EST_VERSION.tar.gz" \
    && chmod u+x /tmp/p4est/p4est-setup.sh \
    && mkdir -p /opt/p4est \
    && cd /tmp/p4est \
    && source /etc/profile.d/modules.sh \
    && module load mpi/openmpi3-x86_64 \
    && ./p4est-setup.sh p4est-$P4EST_VERSION.tar.gz /opt/p4est \
    && rm -rf /tmp/p4est

# Trilinos
RUN set -ex \
    && mkdir -p /tmp/trilinos \
    && wget -qP /tmp/trilinos/ "https://github.com/trilinos/Trilinos/archive/trilinos-release-$TRILINOS_VERSION.tar.gz" \
    && tar -xf /tmp/trilinos/trilinos-release-$TRILINOS_VERSION.tar.gz -C /tmp/trilinos/ \
    && cd /tmp/trilinos/Trilinos-trilinos-release-$TRILINOS_VERSION \
    && mkdir build \
    && cd build \
    && mkdir -p /opt/trilinos \
    && source /etc/profile.d/modules.sh \
    && module load mpi/openmpi3-x86_64 \
    && cmake3                                            \
        -DTrilinos_ENABLE_Amesos=ON                      \
        -DTrilinos_ENABLE_Epetra=ON                      \
        -DTrilinos_ENABLE_EpetraExt=ON                   \
        -DTrilinos_ENABLE_Ifpack=ON                      \
        -DTrilinos_ENABLE_AztecOO=ON                     \
        -DTrilinos_ENABLE_Sacado=ON                      \
        -DTrilinos_ENABLE_Teuchos=ON                     \
        -DTrilinos_ENABLE_MueLu=ON                       \
        -DTrilinos_ENABLE_ML=ON                          \
        -DTrilinos_ENABLE_ROL=ON                         \
        -DTrilinos_ENABLE_Tpetra=ON                      \
        -DTrilinos_ENABLE_COMPLEX_DOUBLE=ON              \
        -DTrilinos_ENABLE_COMPLEX_FLOAT=ON               \
        -DTrilinos_ENABLE_Zoltan=ON                      \
        -DTrilinos_VERBOSE_CONFIGURE=OFF                 \
        -DTPL_ENABLE_MPI=ON                              \
        -DBUILD_SHARED_LIBS=ON                           \
        -DCMAKE_VERBOSE_MAKEFILE=OFF                     \
        -DCMAKE_BUILD_TYPE=RELEASE                       \
        -DCMAKE_INSTALL_PREFIX:PATH=/opt/trilinos        \
        ../                                              \
    && make install -j $TRILINOS_BUILD_JOBS \
    && rm -rf /tmp/trilinos

CMD bash