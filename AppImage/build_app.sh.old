#!/usr/bin/env sh

set -e

ROOT="$(pwd)"

APPDIR="${ROOT}/FUCTool.AppDir"
mkdir -p "${APPDIR}"

APPUSR="${APPDIR}/usr"
TOOLS="${ROOT}/tools"
SRC="${APPDIR}/src"
BIN="${SRC}/bin"

mkdir -p "${APPUSR}"
mkdir -p "${TOOLS}"
mkdir -p "${SRC}"
mkdir -p "${BIN}"

PYTHON="${TOOLS}/python"
MHEF="${TOOLS}/mhef"
MHFF="${ROOT}/mhff"
UMDR="${TOOLS}/UMD-replace"
XDELTA="${TOOLS}/xdelta3"
SEDPC="${TOOLS}/SED-PC"

if [ ! -d "${PYTHON}" ]; then
    cd "${TOOLS}"
    wget "https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tar.xz" -O "python.tar.xz"
    tar -xf "python.tar.xz"
    rm "python.tar.xz"
    mv "Python-3.11.8" "${PYTHON}"
    cd "${ROOT}"
fi

if [ ! -f "${APPUSR}/bin/python3" ]; then
    cd "${PYTHON}"
    ./configure --prefix="${APPUSR}"
    make
    make install
    cd "${ROOT}"
fi

"${APPUSR}/bin/pip3" install pyqt5 bitstring pycdlib

if [ ! -d "${MHEF}" ]; then
    git clone https://github.com/IncognitoMan/mhef.git "${MHEF}"
    "${APPUSR}/bin/pip3" install "${MHEF}"
fi

if [ ! -d "${MHFF}" ]; then
    git clone https://github.com/IncognitoMan/mhff.git "${MHFF}"
    # cd "${MHFF}"
    # mkdir mhff
    # mv n3ds psp mhff
    # cp "${MHEF}/setup.py" .
    # sed -i 's/mhef/mhff/g' setup.py
    # cd "${ROOT}"
    # "${APPUSR}/bin/pip3" install -e "${MHFF}"
fi

if [ ! -d "${UMDR}" ]; then
    git clone https://github.com/Snakes128/UMD-replace_x64 "${UMDR}"
fi

if [ ! -f "${BIN}/UMD-replace" ]; then
    cd "${UMDR}"
    sed -i 's/_fseeki64/fseeko64/g' UMDReplace_x64.cpp
    sed -i 's/_ftelli64/ftello64/g' UMDReplace_x64.cpp
    gcc --std=c++11 UMDReplace_x64.cpp -o UMD-replace
    cp UMD-replace "${BIN}"
    cd "${ROOT}"
fi

if [ ! -d "${XDELTA}" ]; then
    cd "${TOOLS}"
    wget "https://github.com/jmacd/xdelta/archive/refs/tags/v3.0.11.tar.gz" -O xdelta.tar.gz
    tar xf xdelta.tar.gz
    rm xdelta.tar.gz
    mv xdelta-3.0.11 "${XDELTA}"
    cd "${ROOT}"
fi

if [ ! -f "${BIN}/xdelta3" ]; then
    cd "${XDELTA}/xdelta3"
    autoreconf --install
    ./configure
    make
    cp xdelta3 "${BIN}"
    cd "${ROOT}"
fi

if [ ! -d "${SEDPC}" ]; then
    git clone https://github.com/BrianBTB/SED-PC.git "${SEDPC}"
fi

if [ ! -f "${BIN}/SED-PC" ]; then
    cd "${SEDPC}/SED"
    sed -i 's/key > 0/key != 0/' main.cpp
    make
    cp psp-sed "${BIN}/SED-PC"
    cd "${ROOT}"
fi

rsync -aP mhff FUCTool.py FUCTool.spec qt_ui.* utils.py resources* "${SRC}"

if [ ! -f "${TOOLS}/appimagetool" ]; then
    wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage \
        -O "${TOOLS}/appimagetool"
    chmod +x "${TOOLS}/appimagetool"
fi

convert "${ROOT}/icon.ico" -thumbnail 256x256 -alpha on -background none -flatten "${APPDIR}/FUCTool-256x256.png"
ARCH=x86_64 "${TOOLS}/appimagetool" "${APPDIR}"
