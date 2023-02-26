#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import glob
import json
import os
import shutil
import sys
from pathlib import Path, PureWindowsPath

import bitstring

import mhef.psp
import mhff.psp.data

UMD_MD5HASH = "1f76ee9ccbd6d39158f06e6e5354a5bd"
PSN_MD5HASH = "cc39d070b2d2c44c9ac8187e00b75dc4"
PATCHED_MD5HASH = "1890386601adf7d1d3d69067e8917c83"  # TODO: Cambiar con la version final

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


def int_to_bytes(x):
    if x == 0:
        return b'\x00'
    else:
        return x.to_bytes((x.bit_length() + 7) // 8, 'little')


def create_temp_folder():
    if not temp_folder.exists():
        os.makedirs(temp_folder)


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

    for itm in config["config.bin"]:
        offset = int(itm["options"]["offset"], 16)
        jvalues = [bytes.fromhex(i["data"][2:]) for i in itm["options"]["values"]]

        file_value = int_to_bytes(configbin[offset])

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

    # check if the data folder exists
    if not Path(infolder, "data").exists():
        return existing_files

    for f in infiles:
        key = PureWindowsPath(f).relative_to(infolder).as_posix()
        try:
            idx = filelist[key]
            existing_files.append({"path": key, "id": idx})
        except KeyError:
            continue  # File is not in the csv

    existing_files.sort(key=lambda k: k['id'])

    return existing_files


def get_filebin_data(filename):
    filebin = read_file_bytes(filename)

    files = []
    for i, byte in enumerate(filebin):
        if byte != 0x00:
            barray = bitstring.BitArray(uint=byte, length=8)

            for j, bit in enumerate(barray[::-1]):
                if bit:
                    files.append(i * 8 + j)

    return files


def generate_filebin(infolder, outfolder):
    infiles = get_all_files(infolder)

    file_ids = []
    existing_files = []
    for fi in infiles:
        try:
            key = PureWindowsPath(fi).relative_to(infolder).as_posix()
            idx = filelist[key]
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

    # copy/rename files and save file.bin
    with open(Path(outfolder, "file.bin"), "wb") as f:
        newbin.tofile(f)

    copy_files(existing_files, outfolder)


def copy_files(allfiles, outfolder):
    for f in allfiles:
        shutil.copy2(Path(f['path']), Path(outfolder, f['id']))


def rename_dump_files(outfolder):
    allfiles = glob.glob(f"{outfolder}/*", recursive=True)
    inv_filelist = dict((v, k) for k, v in filelist.items())

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


def decrypt_save(filepath, mode):
    game = None

    if mode == 1:
        game = mhef.psp.MHP2G_EU
    if mode == 2:
        game = mhef.psp.MHP2G_NA
    if mode == 3:
        game = mhef.psp.MHP2G_JP

    sfile = read_file_bytes(filepath)

    psc = mhef.psp.PSPSavedataCipher(game)
    sfile = psc.decrypt(sfile)

    sc = mhef.psp.SavedataCipher(game)
    dec = sc.decrypt(sfile)

    return dec


def get_quest_data(qfile):
    current = 0x80
    while qfile[current] != 0x00:
        current += 1

    name = qfile[0x80:current].decode("utf-8")
    qid = int.from_bytes(qfile[0x64:0x66], byteorder='little')

    return str(qid), name


def get_quests_in_folder():
    quests = glob.glob("quests/*.mib.dec")+glob.glob("quests/*.pat")

    res = []
    for q in quests:
        if Path(q).suffix == ".pat":
            qfile = read_file_bytes(q)[0x04:]
        else:
            qfile = read_file_bytes(q)

        qid, name = get_quest_data(qfile)
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

            if dec is not None:
                qid, name = get_quest_data(dec)
                res.append({"bytes": bytearray(dec), "qid": qid, "name": name})

    return res


def encrypt_quest(quest):
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

    return None


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

        # Quest filename
        fname = f"m{q['qid']}.mib"
        nsize = len(fname)
        fname = fname.encode()

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
            nfilelist.setdefault(path, idx)

    return nfilelist


config = get_config_json("res/config.json")
filelist = get_filelist("res/filelist_2g.csv")
current_path = Path(sys.executable).parent.resolve()
# current_path = Path(__file__).resolve().parent
temp_folder = Path(current_path, "res", "temp")
