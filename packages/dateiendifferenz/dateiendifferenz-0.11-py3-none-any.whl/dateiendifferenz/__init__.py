import ctypes
import os
import platform
import sys
import tempfile
from functools import cache, partial
from time import strftime, sleep
from touchtouch import touch
from subprocess_alive import is_process_alive
import subprocess
import pandas as pd
import re
import numpy as np

wd = os.sep.join(__file__.split(os.sep)[:-1])

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}


@cache
def get_short_path_name(long_name):
    r"""
    Convert a given long file path to its equivalent short file path on Windows.

    Args:
        long_name (str): The long file path to convert.

    Returns:
        str: The shortened file path if on Windows; otherwise, returns the original path.
    """
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return long_name


def get_tmpfile(suffix=".txt"):
    r"""
    Create a temporary file and return its path along with a function to remove it.

    Args:
        suffix (str, optional): Suffix for the temporary file. Defaults to ".txt".

    Returns:
        tuple: A tuple containing the temporary filename and a function to remove it.
    """
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    return filename, partial(os.remove, tfp.name)


def _remf(*args, **kwargs):
    return


def parsetext(
    file2parse,
    stringsextpath="stringsext.exe",
    blocks_in_one_line=64,
    output_encoding="Latin",
    min_chars=64,
    outputfolder=wd,
    save_as=(
        "UTF-16BE",
        "UTF-16LE",
        "UTF-8",
        "ISO-8859-1",
        "ISO-8859-2",
        "ISO-8859-3",
        "windows-1252",
    ),
    wait=True,
):
    r"""
    Parse a specified file or content utilizing the external tool 'stringsext' and save the parsed content in multiple encodings.

    This function uses 'stringsext' (https://github.com/getreu/stringsext) to process the input file or content.
    It provides flexibility in specifying various parameters like encoding, block processing, and output directory.

    Args:
        file2parse (str or bytes): The file path or content that needs to be parsed.
        stringsextpath (str, optional): Path to the 'stringsext' executable. Defaults to 'stringsext.exe'.
        blocks_in_one_line (int, optional): Number of blocks to process in a single line. Defaults to 64.
        output_encoding (str, optional): Encoding type for the output files. Defaults to 'Latin'.
        min_chars (int, optional): Minimum number of characters required for processing. Defaults to 64.
        outputfolder (str, optional): Directory where the parsed files will be saved. Defaults to the working directory.
        save_as (tuple, optional): Tuple of encoding formats to save the parsed content. Defaults to multiple common encodings.
        wait (bool, optional): If True, the function will wait for all subprocesses to complete before returning. Defaults to True.

    Returns:
        list: A list containing commands executed and associated subprocess objects created during the parsing process.
    Example
        from dateiendifferenz import parsedtxt2df,parsetext
        allscrapedfiles = [
            r"C:\testUTF-16LE.txt",
            r"C:\testUTF-16BE.txt",

            r"C:\testwindows-1252.txt",
            r"C:\testISO-8859-3.txt",
            r"C:\testISO-8859-2.txt",
            r"C:\testISO-8859-1.txt",
            r"C:\testUTF-8.txt",

        ]
        outputfolder='c:\\outputparsingtestx'
        stringsext=r"C:\Users\hansc\.conda\envs\dfdir\stringsext.exe"
        filetoparse=r"C:\Users\hansc\Downloads\a158\m3.ans"
        allcmds = parsetext(file2parse=filetoparse, stringsextpath=stringsext,
                            blocks_in_one_line=64, output_encoding='Latin', min_chars=64, outputfolder=outputfolder,
                            save_as=(
                                "UTF-16BE",
                                "UTF-16LE",
                                "UTF-8",
                                "ISO-8859-1",
                                "ISO-8859-2",
                                "ISO-8859-3",
                                "windows-1252",), wait=True)

        df=parsedtxt2df([x[1] for x in allcmds], )

    """
    removefu = _remf
    if not isinstance(file2parse, str):
        filename, removefu = get_tmpfile()
        with open(filename, mode="wb") as f:
            f.write(file2parse)
        file2parse = filename
    elif isinstance(file2parse, str):
        if not os.path.exists(file2parse):
            filename, removefu = get_tmpfile()
            with open(filename, mode="w") as f:
                f.write(file2parse)
            file2parse = filename

    tstamp = strftime("%Y_%m_%d_%H_%M_%S")
    stringsextpath = get_short_path_name(stringsextpath)
    os.makedirs(outputfolder, exist_ok=True)
    allcommands = []
    file2parse = get_short_path_name(file2parse)
    for form in save_as:
        savefilepath = os.path.normpath(
            os.path.join(outputfolder, f"{tstamp}--{form}.txt")
        )
        touch(savefilepath)
        savefilepath = get_short_path_name(savefilepath)
        cmd = rf"""{stringsextpath} -td -r -q {blocks_in_one_line} -u {output_encoding} --chars-min {min_chars} --output={savefilepath} --encoding={form} {file2parse}"""
        allcommands.append([cmd, savefilepath])
    allcommands2 = allcommands.copy()
    for ini, cmd in enumerate(allcommands):
        p = subprocess.Popen(cmd[0], **invisibledict)
        allcommands2[ini].append(p)
    alliveprocs = [True]
    if wait:
        # sleep(2)
        while alliveprocs:
            alliveprocs.clear()
            for c, o, proc in allcommands2:
                print(f"Checking: {proc.pid} {c}\r")
                if is_process_alive(proc.pid):
                    alliveprocs.append(True)
                    sleep(0.1)
        removefu()
    return allcommands2


def parsedtxt2df(allscrapedfiles, save_folder=None):
    r"""
    Parse multiple scraped files and consolidate the results into a single DataFrame.

    Args:
        allscrapedfiles (list): List of files to be parsed.
        save_folder (str, optional): Folder path to save the parsed DataFrames. Defaults to None.

    Returns:
        pandas.DataFrame: A combined DataFrame containing the parsed data from all specified files.
    """
    finaldfs = []
    allapliset = set()
    if save_folder:
        os.makedirs(save_folder, exist_ok=True)
    for fi in allscrapedfiles:
        try:
            with open(fi, mode="rb") as f:
                data = f.read()

            df2 = (
                pd.DataFrame(
                    (
                        (
                            [g[0][0:1], int(g[0:1][0][1:-1]), g[0:1][0][-1:], g[1]]
                            for x in data.splitlines()
                            if len(g := x.split(b"\t", maxsplit=1)) == 2
                        )
                    )
                )
                .astype(
                    {
                        0: "category",
                        1: "Int64",
                        2: "category",
                    }
                )
                .rename(
                    columns={
                        0: "aa_direction",
                        1: "aa_address",
                        2: "aa_continues",
                        3: "aa_payload",
                    }
                )
            )

            df3 = df2.loc[
                (
                    df2.aa_continues.apply(
                        lambda qq: True if re.match(rb"^\s*$", qq) else False
                    )
                )
            ].index
            df2["aa_group_number"] = pd.NA
            df2["aa_group_number"] = df2["aa_group_number"].astype("Int64")
            df2.loc[df3, "aa_group_number"] = np.arange(len(df3))
            df2["aa_group_number"] = df2["aa_group_number"].ffill().bfill()

            df2["aa_file"] = fi
            madix = df2.groupby("aa_group_number")["aa_payload"].apply(
                lambda p: b"".join(p.__array__())
            )
            madi = madix.to_dict()
            df2["aa_whole_string"] = (
                df2.aa_group_number.map(lambda j: madi.get(j, b"")).__array__().copy()
            )
            allapliset.update(list(madi.values()))
            finaldfs.append(df2)
            if save_folder:
                tstamp = strftime("%Y_%m_%d_%H_%M_%S")

                savefolderfile = os.path.join(save_folder, f"{tstamp}.pkl")
                df2.to_pickle(savefolderfile)
        except Exception as fe:
            sys.stderr.write(f"{fe}\n")
            sys.stderr.flush()
    if len(finaldfs) > 1:
        try:
            df = pd.concat(finaldfs, ignore_index=True)
        except Exception as fe:
            return pd.DataFrame()
    elif len(finaldfs) == 1:
        df = finaldfs[0]
    else:
        return pd.DataFrame()
    df["aa_whole_string"] = pd.Series(
        pd.Categorical(
            df["aa_whole_string"],
            categories=allapliset,
        )
    )
    df["aa_file"] = pd.Series(
        pd.Categorical(
            df["aa_file"],
            categories=allscrapedfiles,
        )
    )
    return df

