#!/usr/bin/env bash

source resources/env.sh

mkdir -p $WORK_DIR/logs
mkdir -p $RESULT_DIR

# check if file exists (can be a symlink)
if [ ! -e $BASE_DIR/$CUDNN7_PACKAGE ]; then
  echo "------------------------------------------------------------------"
  echo -e "Please download CUDNN $CUDNN7_PACKAGE from \n$CUDNN7_URL\nand place it in" $BASE_DIR
  echo "Login/Registration required to accept the license!"
  echo "------------------------------------------------------------------"
  exit
fi

if [ ! -e $BASE_DIR/$CUDNN8_PACKAGE ]; then
  echo "------------------------------------------------------------------"
  echo -e "Please download CUDNN $CUDNN8_PACKAGE from \n$CUDNN8_URL\nand place it in" $BASE_DIR
  echo "Login/Registration required to accept the license!"
  echo "------------------------------------------------------------------"
  exit
fi

if [ ! -e $BASE_DIR/$CUDA10_PACKAGE ]; then
  echo "------------------------------------------------------------------"
  echo "Downloading $CUDA10_PACKAGE..."
  wget "https://developer.download.nvidia.com/compute/cuda/$CUDA10_VERSION/Prod/local_installers/$CUDA10_PACKAGE" -P $BASE_DIR
fi

if [ ! -e $BASE_DIR/$CUDA11_PACKAGE ]; then
  echo "------------------------------------------------------------------"
  echo "Downloading $CUDA11_PACKAGE..."
  wget "https://developer.download.nvidia.com/compute/cuda/$CUDA11_VERSION/local_installers/$CUDA11_PACKAGE" -P $BASE_DIR
fi

# this one must *not* be a symlink as it's accessed in the container
if [ ! -f $BASE_DIR/$MKL_PACKAGE ];then
  echo "------------------------------------------------------------------"
  echo "Downloading Intel MKL 2019.5 (used by Apache SystemDS)"
  wget "https://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15816/$MKL_PACKAGE" -P $BASE_DIR
fi

if ! command -v singularity &> /dev/null; then
  echo "------------------------------------------------------------------"
  echo "Please install Singularity-CE 3.9.x container software from https://github.com/sylabs/singularity/releases"
  echo "For RHEL and Ubuntu, packages are provided there. For other systems, follow the instructions at
    https://github.com/sylabs/singularity/blob/master/INSTALL.md"
  echo "------------------------------------------------------------------"
fi

cd "$WORK_DIR" || exit
if [ ! -d $WORK_DIR/cuda-$CUDA10_VERSION ];then
  echo "Extracting CUDA $CUDA10_VERSION SDK and CUDNN7"
  chmod u+x $BASE_DIR/$CUDA10_PACKAGE
  $BASE_DIR/$CUDA10_PACKAGE --silent --toolkit --no-drm --no-man-page --no-opengl-libs --override --installpath=$WORK_DIR/cuda-$CUDA10_VERSION
  tar xf $BASE_DIR/$CUDNN7_PACKAGE --directory=$WORK_DIR/cuda-$CUDA10_VERSION/ --strip-components=1
fi

if [ ! -e $WORK_DIR/cuda-$CUDA10_VERSION/lib64/libcudnn.so ]; then
  echo "Failed to set up CUDA $CUDA10_VERSION SDK or CUDNN7"
  exit
fi

if [ ! -d $WORK_DIR/cuda-$CUDA11_VERSION ];then
  echo "Extracting CUDA $CUDA11_VERSION SDK and CUDNN8"
  chmod u+x $BASE_DIR/$CUDA11_PACKAGE
  $BASE_DIR/$CUDA11_PACKAGE --silent --toolkit --no-drm --no-man-page --no-opengl-libs --override --installpath=$WORK_DIR/cuda-$CUDA11_VERSION
  tar xf $BASE_DIR/$CUDNN8_PACKAGE --directory=$WORK_DIR/cuda-$CUDA11_VERSION/ --strip-components=1
fi

if [ ! -e $WORK_DIR/cuda-$CUDA11_VERSION/lib64/libcudnn.so ]; then
  echo "Failed to set up CUDA $CUDA11_VERSION SDK or CUDNN8"
  exit
fi

if [ ! -f $SANDBOX ]; then
  # ToDo: setup container remote build service
  #singularity pull library:/corepointer/cidr2022-daphne/experiment-sandbox:latest
  echo
  singularity build --fakeroot $SANDBOX $BASE_DIR/resources/singularity-container.def
  retVal=$?
  if [ $retVal -ne 0 ]; then
    echo "Error, building the experiment sandbox (singularity container) seems to have failed with exit status" $retVal
    exit
  fi
fi

if [ ! -f $SANDBOX ]; then
  echo "Error: Singularity image" $SANDBOX "does not exist. Please run 1_setup_env.sh to build it (root or fakeroot privileges required)"
  exit
fi

if [ ! -d $WORK_DIR/intel ]; then
  echo "Installing Intel MKL 2019.5"
  sed 's#_REPLACE_#'$WORK_DIR'/intel#' $BASE_DIR/resources/mkl2019.5-silent-setup-template.cfg > $WORK_DIR/mkl2019.5-silent-setup.cfg
  singularity run $SANDBOX "tar xzf $BASE_DIR/l_mkl_2019.5.281.tgz; cd l_mkl_2019.5.281; \
      ./install.sh --user-mode --silent ../mkl2019.5-silent-setup.cfg; cd ..; rm -rf l_mkl_2019.5.281"
fi
. $WORK_DIR/intel/bin/compilervars.sh intel64

if [ ! -d $DAPHNE_ROOT ]; then
  git clone https://github.com/daphne-eu/daphne.git $DAPHNE_ROOT
  cd $DAPHNE_ROOT
  echo -e "\nInitial Daphne build + third party dependencies\n"; sleep 3
  git checkout p2-alpha
  git apply $BASE_DIR/resources/0000-daphne-build_sh.patch
  cd $BASE_DIR
fi

if [ ! -d $DAPHNE_ROOT/build ]; then
  singularity run --bind $CUDA11_PATH:/usr/local/cuda --nv $SANDBOX \
    "cd $DAPHNE_ROOT;./build.sh 2>&1 | tee $WORK_DIR/logs/build-daphne-deps-log.txt"
fi

if [ ! -d $SYSTEMDS_ROOT ]; then
  git clone https://github.com/apache/systemds.git $SYSTEMDS_ROOT
  cd $SYSTEMDS_ROOT
  git checkout 007b684a99090b178ec33d3c75f38f7ccaccf07a
  singularity run $SANDBOX "mvn package | tee $WORK_DIR/logs/build-systemds-log.txt"
fi
