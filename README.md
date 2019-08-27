# Python-Apple-EFI-Patcher
patcher.py is a python3 script that automatically patches an Apple EFI SPI Rom file.

# Usage:
Place patcher.py, offsets.py, database.json and the ME_Regions folder into the same directory. Run as follows:

python3 patcher.py -i <input_efi_filename> -o <output_efi_filename> -t <efi_type_#> -s <serial_to_insert> -m <me_region_filename> -r

example: python3 patcher.py -i firmware.bin.bin -o dump.bin -t 5 -s ABCDEFGH1234 -m ME_Regions/MBA61/10.13.6_MBA61_0107_B00.rgn -r

Note: You can drag and drop files into the terminal to avoid having to type locations.

Note: ME Regions are untested, and may not be useable!!!! Require real world testing. Feedback would be appreciated.
ME Regions have been extracted from macOS 10.12.6, 10.13.6, and 10.14.6. They are contained in the ME_Regions folder. Each subfolder corresponds to a system type. (example: MBA61 = MacBook Air 6,1). Each ME region file is named in accordance to the macOS version from which it was extracted, the system type, the Boot Rom Version and the ME Version. (example: 10.13.6_MBA61_0107_B00_9.5.3.1526.rgn, means that the ME Region was extracted from macOS High Sierra 10.13.6, it is for a MacBook Air 6,1, it came from an EFI with Boot Rom Version 0107_B00 and the ME Version is 9.5.3.1526). In some instances, regions between macOS and Boot Rom versions may be identical. It seemed that anything extracted from *.scap files rather an *.fd files were the same between OS versions. You can use something like hex fiend to compare and see if they are identical. Also, anything extracted from macOS 10.14.6 had no references to Boot Room Versions in their names. Not that it particularly matters, what you want to match up is the ME version number.

Offsets for new types of EFI's can also be easily added. Just follow the format provided in the offsets.py file and append your additions. Use something like hexfiend to acquire the line position offsets for each region.

Options:
-i <input_efi_filename>     -- name of the file to be modified
-o <output_efi_filename>    -- name of the newly modified file
-t <efi_type>               -- type # of efi (see list below)
-s <serial_to_insert>       -- serial number to be inserted
-m <me_region_filename>     -- name of the ME Region file to insert
-r                          -- remove firmware lock

EFI Type Options:

1 = 2008 A1278 820-2327

2 = 2011 A1278 820-2936
    2011 A1286 820-2915

3 = 2011 A1369 820-3023

4 = 2012 A1278 820-3115
    2012 A1286 820-3330
    late 2012 / early 2013 A1398 820-3332
    late 2012 / early 2013 A1425 820-3462
    2012 A1465 820-3208
    2012 A1466 820-3209

5 = 2013/2014 A1502 820-3476
    2013/2014 A1398 820-3662
    2013/2014 A1465 820-3435
    2013/2014 A1466 820-3437

6 = 2015 A1398 820-00138
    2015 A1465 820-00164
    2015-2017 A1466 820-00165
    2015 A1502 820-4924

7 = 2017 A1706 820-00239
