#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import glob
import hashlib
import json
import os
import shutil
import sys
from io import BytesIO
from pathlib import Path

import bitstring
import pycdlib

import mhef.psp
import mhff.psp.data

VERSION = "1.2.1"

UMD_MD5HASH = "1f76ee9ccbd6d39158f06e6e5354a5bd"
PSN_MD5HASH = "cc39d070b2d2c44c9ac8187e00b75dc4"

QUESTS_START = 0x142300
QUESTS_END = 0x169360
QUESTS_SIZE = 0x22B0


def read_file_bytes(filepath):
    with open(filepath, "rb") as f:
        bfile = f.read()

    return bytearray(bfile)


def write_file_bytes(filepath, barray):
    with open(filepath, "wb") as f:
        f.write(barray)


def create_temp_folder():
    if not temp_folder.exists():
        os.makedirs(temp_folder)


def get_iso_hash(isofile):
    with open(isofile, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def extract_data_bin(isofile):
    iso = pycdlib.PyCdlib()
    iso.open(isofile)

    data_bin = BytesIO()
    iso.get_file_from_iso_fp(data_bin, iso_path='/PSP_GAME/USRDIR/DATA.BIN')

    iso.close()

    data_bin_path = Path(temp_folder, "DATA.BIN")
    with open(data_bin_path, "wb") as f:
        f.write(data_bin.getbuffer())

    return str(data_bin_path)


def write_config(barray, offset, data):
    offset = int(offset, 16)
    data = bytes.fromhex(data[2:])
    dsize = len(data)

    # Expand file if the offset is bigger
    if len(barray) < offset + len(data):
        ext = (offset + len(data)) - len(barray)
        barray.extend(b'\x00' * ext)

    for i in range(dsize):
        barray[offset + i] = data[i]

    return barray


def read_configs(config_path):
    configbin = read_file_bytes(config_path)
    values = []

    for itm in config["CONFIG.BIN"]:
        offset = int(itm["options"]["offset"], 16)
        jvalues = [bytes.fromhex(i["data"][2:]) for i in itm["options"]["values"]]

        op_size = len(bytes.fromhex(itm["options"]["values"][0]["data"][2:]))
        file_value = bytes(configbin[offset:offset+op_size])

        if file_value in jvalues:
            index = None
            for i, v in enumerate(itm["options"]["values"]):
                if bytes.fromhex(v["data"][2:]) == file_value:
                    index = i
                    break

            values.append(index)
        else:
            values.append(0)  # current value is not in the json options

    return values


def get_all_files(folderpath):
    return glob.glob(f"{folderpath}/**/*.*", recursive=True)


def read_replace_folder(infolder):
    infiles = get_all_files(infolder)

    existing_files = []

    for f in infiles:
        key = Path(f).relative_to(infolder).name
        try:
            idx = filelist[key][0]
            full_path = filelist[key][1]
            existing_files.append({"path": full_path, "id": idx})
        except KeyError:
            continue  # File is not in the csv

    existing_files.sort(key=lambda k: k['id'])

    return existing_files


def generate_filebin(infolder, outfolder):
    infiles = get_all_files(infolder)

    file_ids = []
    existing_files = []
    for fi in infiles:
        try:
            key = Path(fi).relative_to(infolder).name
            idx = filelist[key][0]
            file_ids.append(idx)
            existing_files.append({"path": fi, "id": idx})
        except KeyError:
            continue  # File is not in the csv

    newbin = bitstring.BitArray(uint=0, length=826 * 8)

    for f in file_ids:
        idx = int(f)
        block = int(idx / 8)
        offset = idx % 8
        index = (block * 8) + (7 - offset)
        newbin[index] = True

    if not os.path.isdir(outfolder):
        os.mkdir(outfolder)

    # copy/rename files and save FILE.BIN
    with open(Path(outfolder, "FILE.BIN"), "wb") as f:
        newbin.tofile(f)

    copy_files(existing_files, outfolder)


def copy_files(allfiles, outfolder):
    for f in allfiles:
        nbytes = add_size_header(Path(f['path']))
        write_file_bytes(Path(outfolder, f['id']), nbytes)


def add_size_header(path):
    fbytes = read_file_bytes(path)
    size = len(fbytes).to_bytes(4, byteorder='little')

    return size + fbytes


def rename_dump_files(outfolder):
    allfiles = glob.glob(f"{outfolder}/*", recursive=True)
    inv_filelist = dict((v[0], v[1]) for k, v in filelist.items())

    for f in allfiles:
        npath = inv_filelist[Path(f).name]
        new_folders = Path(outfolder).joinpath(Path(npath).parent)
        os.makedirs(new_folders, exist_ok=True)

        dest = Path(outfolder).joinpath(npath)
        shutil.move(f, dest)


def decrypt_data_bin(data_bin, outpath):
    dc = mhef.psp.DataCipher(mhef.psp.MHP2G_JP)
    dc.decrypt_file(data_bin, outpath)


def dump_data_bin(data_bin, outfolder):
    mhff.psp.data.extract(data_bin, outfolder)


def decrypt_save(filepath, region):
    game = None

    if region == 1:
        game = mhef.psp.MHP2G_EU
    if region == 2:
        game = mhef.psp.MHP2G_NA
    if region == 3:
        game = mhef.psp.MHP2G_JP

    sfile = read_file_bytes(filepath)

    psc = mhef.psp.PSPSavedataCipher(game)
    sfile = psc.decrypt(sfile)

    sc = mhef.psp.SavedataCipher(game)
    dec = sc.decrypt(sfile)

    return dec


def encrypt_save(save, region):
    game = None

    if region == 1:
        game = mhef.psp.MHP2G_EU
    if region == 2:
        game = mhef.psp.MHP2G_NA
    if region == 3:
        game = mhef.psp.MHP2G_JP

    sc = mhef.psp.SavedataCipher(game)
    enc = sc.encrypt(save)

    return enc


def get_quest_data(qfile):
    # Check if it's encrypted
    if qfile[0x00:0x08] != bytearray(b"\x4C\x00\x00\x00\x32\x4E\x44\x47"):
        return None, None

    current = 0x80
    while qfile[current] != 0x00:
        current += 1

    name = qfile[0x80:current].decode("utf-8")
    qid = int.from_bytes(qfile[0x64:0x66], byteorder='little')

    return str(qid), name


def get_quests_in_folder():
    quests = glob.glob("quests/*.mib*")+glob.glob("quests/*.pat")

    res = []
    for q in quests:
        if Path(q).suffix == ".pat":
            qfile = read_file_bytes(q)[0x04:]
        else:
            qfile = read_file_bytes(q)

        qid, name = get_quest_data(qfile)
        if qid is not None:  # Ignore encrypted quests
            if not qid.startswith("61"):  # Ignore arena/challenge quests
                res.append({"bytes": qfile, "qid": qid, "name": name})

    res = sorted(res, key=lambda d: d['qid'])
    return res


def get_quests_in_save(save_file):
    res = []
    for i in range(QUESTS_START, QUESTS_END, QUESTS_SIZE):
        current = i
        while save_file[current:current + 0x4] != b'\x00\x00\x00\x00':
            current += 1

        if current - i > 0:  # Check for empty slots
            dec = decrypt_quest(save_file[i:current])

            if len(dec) > 0:
                qid, name = get_quest_data(dec)
                res.append({"bytes": bytearray(dec), "qid": qid, "name": name})

    return res


def encrypt_quest(quest):
    enc = bytes(bytearray(32))

    if len(quest) > 0:
        qc = mhef.psp.QuestCipher(mhef.psp.MHP2G_JP)
        enc = qc.encrypt(quest)

    return enc


def decrypt_quest(quest):
    # Very ugly but, yeah...
    try:
        qc = mhef.psp.QuestCipher(mhef.psp.MHP2G_JP)
        dec = qc.decrypt(quest)
        return dec
    except ValueError:
        pass

    try:
        qc = mhef.psp.QuestCipher(mhef.psp.MHP2G_NA)
        dec = qc.decrypt(quest)
        return dec
    except ValueError:
        pass

    try:
        qc = mhef.psp.QuestCipher(mhef.psp.MHP2G_EU)
        dec = qc.decrypt(quest)
        return dec
    except ValueError:
        pass

    return bytes()


def add_quests_to_save(save, quests):
    offsets = []
    for i in range(QUESTS_START, QUESTS_END, QUESTS_SIZE):
        offsets.append(i)

    for i, q in enumerate(quests):
        # Quest data
        qenc = encrypt_quest(q["bytes"])
        qsize = len(qenc)

        for j in range(qsize):
            save[offsets[i]+j] = qenc[j]

        # Padding
        padding = (offsets[i] + QUESTS_SIZE) - (offsets[i] + qsize)
        for j in range(padding):
            save[offsets[i]+qsize+j] = 0x00

        if q['qid']:
            # Quest filename
            fname = f"m{q['qid']}.mib"
            nsize = len(fname)
            fname = fname.encode()
        else:
            nsize = 0
            fname = ""

        noff = offsets[i] + QUESTS_SIZE - 0x10
        for j in range(nsize):
            save[noff+j] = fname[j]

        # Padding
        padding = 0x10 - nsize
        for j in range(padding):
            save[noff+nsize+j] = 0x00

    return save


def get_config_json(filename):
    with open(filename) as f:
        nconfig = json.loads(f.read())

    return nconfig


def get_filelist(filename):
    nfilelist = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for idx, path in reader:
            fname = Path(path).name
            nfilelist.setdefault(fname, [idx, path])    # 0 = ID, 1 = full path

    return nfilelist


def is_linux() -> bool:
    return sys.platform.startswith('linux')


if is_linux():
    current_path = Path(__file__).parent.resolve()
else:
    current_path = Path(sys.executable).parent.resolve()

resources_path = Path(current_path, "res")
bin_path = Path(current_path, "bin")

if is_linux():
    # Can't create dirs inside AppImage
    temp_folder = Path.home() / ".cache/FUCTool"
else:
    temp_folder = resources_path.joinpath("temp")

config = get_config_json(resources_path.joinpath("config.json"))
filelist = get_filelist(resources_path.joinpath("filelist.csv"))
