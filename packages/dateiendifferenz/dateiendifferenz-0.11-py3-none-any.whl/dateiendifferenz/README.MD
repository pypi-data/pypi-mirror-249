### Wrapper for stringsext and some other stuff

### Tested against Windows 10 / Python 3.11 / Anaconda 

### Wrapper for stringsext and some other stuff

## Overview:

stringsext https://github.com/getreu/stringsext is a versatile library designed to facilitate text processing tasks, especially tailored for handling file parsing and encoding conversion. By leveraging this library, developers can effortlessly parse files, transform content into various encodings, and optimize text-based operations.

## Key Features:

File Parsing: With stringsext, parsing both file paths and byte content is streamlined, ensuring seamless data extraction and manipulation.

## Multi-Encoding Support: 

The library boasts extensive support for multiple encoding formats, including but not limited to:

UTF-16BE
UTF-16LE
UTF-8
ISO-8859-1
ISO-8859-2
ISO-8859-3
Windows-1252


```python

"""
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
filetoparse=r"C:\WINDOWS\system32\cmd.exe"
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


print(df[:5].to_string())
  aa_direction  aa_address aa_continues                                                           aa_payload  aa_group_number                   aa_file                                                                                      aa_whole_string
0         b'<'      255360         b' '  b'<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersi'                0  c:\OU3AF1~1\204D3D~1.TXT                         b'<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">'
1         b'>'      255360         b'+'                                                         b'on="1.0">'                0  c:\OU3AF1~1\204D3D~1.TXT                         b'<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">'
2         b'<'      256000         b' '  b'        <dpiAware  xmlns="http://schemas.microsoft.com/SMI/2005/'                1  c:\OU3AF1~1\204D3D~1.TXT  b'        <dpiAware  xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>'
3         b'>'      256000         b'+'                                                           b'Windows'                1  c:\OU3AF1~1\204D3D~1.TXT  b'        <dpiAware  xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>'
4         b' '      256128         b'+'                                         b'Settings">true</dpiAware>'                1  c:\OU3AF1~1\204D3D~1.TXT  b'        <dpiAware  xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>'


```
