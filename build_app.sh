#!/usr/bin/env sh

set -e

ROOT="$(pwd)"

APPDIR="${ROOT}/FUCTool.AppDir"
mkdir -p "${APPDIR}"
APPRUN="${APPDIR}/AppRun"

APPUSR="${APPDIR}/usr"
TOOLS="${ROOT}/tools"
SRC="${APPDIR}/src"

mkdir -p "${APPUSR}"
mkdir -p "${TOOLS}"
mkdir -p "${SRC}"

PYTHON="Python-3.11.8"

if [ ! -d "${PYTHON}" ]; then
    wget "https://www.python.org/ftp/python/3.11.8/${PYTHON}.tar.xz"
    tar -xf "${PYTHON}.tar.xz"
fi

if [ ! -f "${APPUSR}/bin/python3" ]; then
    cd "${PYTHON}"
    ./configure --prefix="${APPUSR}"
    make
    make install
    cd "${ROOT}"
fi

"${APPUSR}/bin/pip3" install pyqt5 bitstring pycdlib

if [ ! -d "${TOOLS}/mhef" ]; then
    git clone https://github.com/IncognitoMan/mhef.git "${TOOLS}/mhef"
    "${APPUSR}/bin/pip3" install -e "${TOOLS}/mhef"
fi

if [ ! -d "${TOOLS}/mhff" ]; then
    git clone https://github.com/IncognitoMan/mhff.git "$TOOLS/mhff"

    cd "${TOOLS}/mhff"
    mkdir mhff
    mv n3ds psp mhff
    cp "${TOOLS}/mhef/setup.py" .
    sed -i 's/mhef/mhff/g' setup.py

    "${APPUSR}/bin/pip3" install -e "${TOOLS}/mhff"
fi

if [ ! -d "${TOOLS}/UMD-replace" ]; then
    git clone https://github.com/Snakes128/UMD-replace_x64 "${TOOLS}/UMD-replace"
    cd "${TOOLS}/UMD-replace"
    sed -i 's/_fseeki64/fseeko64/g' UMDReplace_x64.cpp
    sed -i 's/_ftelli64/ftello64/g' UMDReplace_x64.cpp
    gcc --std=c++11 UMDReplace_x64.cpp -o UMD-replace
fi

mkdir -p "${SRC}/bin"
cp "${TOOLS}/UMD-replace/UMD-replace" "${SRC}/bin/"

cd "${ROOT}"
rsync -aP FUCTool.py FUCTool.spec qt_ui.* utils.py resources* "${SRC}"

if [ ! -f "${TOOLS}/appimagetool" ]; then
    wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage \
        -O "${TOOLS}/appimagetool"
    chmod +x "${TOOLS}/appimagetool"
fi

convert "${ROOT}/icon.ico" -thumbnail 256x256 -alpha on -background none -flatten "${APPDIR}/FUCTool-256x256.png"
ARCH=x86_64 "${TOOLS}/appimagetool" "${APPDIR}"
