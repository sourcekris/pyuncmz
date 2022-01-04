## uncmz - extractor for Lotus CMZ files

Probably a proprietary format by Lotus. These files are DCL imploded with some basic
header.

#### Usage

```shell
usage: uncmz.py [-h] -e FILENAME [-d PATH] [-p PATH]

Extract Lotus CMZ Files.

optional arguments:
  -h, --help            show this help message and exit
  -e FILENAME, --extract FILENAME
                        The CMZ file to extract.
  -d PATH, --destination PATH
                        An optional output folder.
  -p PATH, --deark PATH
                        Path to deark archiver in case it is not in $PATH

Please file bugs on the GitHub Issues. Thanks
```

#### Format Info

Reverse engineering of the format I found:

- 4 byte file signature: "Clay"
- 4 byte integer - Compressed data size
- 4 byte integer - Uncompressed data size
- 4 byte checksum - unknown checksum algorithm?
- 1 byte filename length
- 3 bytes unknown, usually "\x00\x00\x00" but is sometimes "\x00\x02\x00"
- n bytes Filename 
- remainder - DCL Imploded payload

A 010 Editor binary template covering the file format is included in this repo.

#### References

- Archive format information: http://fileformats.archiveteam.org/wiki/CMZ_(archive_format)
- Samples: http://cd.textfiles.com/cdaction/cdaction35/PROG/AMIPRO/

#### Author

- Kris Hunt (@ctfkris)