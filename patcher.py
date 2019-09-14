import binascii
import sys, getopt
import json
from sys import getsizeof
from offsets import set_offsets
from urllib.request import urlopen
from xml.etree import ElementTree

def check_length(a, b):
	length_of_a = len(a)
	length_of_b = len(b)
	if(length_of_a == length_of_b):
		return True
	else:
		return False

def search_json_last4(json_object, hwc_code):
	for dict in json_object:
		if dict['last4'] == hwc_code:
			return dict['name']

# function from MacmodelShelf - https://github.com/MagerValp/MacModelShelf
def lookup_mac_model_code_from_apple(model_code):
	try:
		f = urlopen("http://support-sp.apple.com/sp/product?cc=%s&lang=en_US" % model_code, timeout=2)
		et = ElementTree.parse(f)
		return et.findtext("configCode")
	except:
		return None

def search_and_update_db(json_db, hwc_code, destination_file):
	with open(json_db, 'rb') as db:
		json_database = json.load(db)
		db.close()

	search = search_json_last4(json_database, hwc_code)

	if (search is None):
		model_info = lookup_mac_model_code_from_apple(hwc_code)

		with open(destination_file, "w") as write_file:
			entry = {"last4": hwc_code, "name": model_info, "id": None, "modelnum": None}
			json_database.append(entry)
			sorted_database = sorted(json_database, key = lambda i: i['last4'])
			json.dump(sorted_database, write_file, indent=3)
		
		search_message = '- Database Updated with New Model Info'
		return model_info, search_message

	else:
		model_info = search
		search_message = '- Model Info Found in Database'
		return model_info, search_message

def main(argv):

	#Variable Initialization
	inputfile = ''
	outputfile = ''
	efi_type = ''
	patch_serial = ''
	remove_lock = ''
	me_region_filename = ''
	fsys_start_offset = 0
	fsys_end_offset = 0
	fsys_buffer = 0
	firmware_lock_start_offset = 0
	firmware_lock_end_offset = 0
	firmware_lock_buffer = 0
	me_region_start_offset = 0
	me_region_end_offset = 0
	me_region_buffer = 0
	count = 0
	write_me = False
	write_fsys = False
	write_lock = False

	#Command Line Operations
	try:
		opts, args = getopt.getopt(argv,"hri:o:t:s:m:",["ifile=","ofile=","efi_type=","patch_serial=","me_region_filename="])
	except getopt.GetoptError:
		print ('patcher.py -i <input_efi_filename> -o <output_efi_filename> -t <efi_type> -s <serial_to_insert> -m <me_region_filename> -r')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('Usage: patcher.py -i <input_efi_filename> -o <output_efi_filename> -t <efi_type_#> -s <serial_to_insert> -m <me_region_filename> -r')
			print ()
			print ('Options:')
			print ('-i <input_efi_filename>		-- name of the file to be modified')
			print ('-o <output_efi_filename>	-- name of the newly modified file')
			print ('-t <efi_type>			-- type # of efi (see list below)')
			print ('-s <serial_to_insert>		-- serial number to be inserted')
			print ('-m <me_region_filename>		-- name of the me region file to insert')
			print ('-r   				-- remove firmware lock')
			print ()
			print ('EFI Type Options:')
			print ('1 = 2008 A1278 820-2327')
			print ()
			print ('2 = 2011 A1278 820-2936')
			print ('    2011 A1286 820-2915')
			print ()
			print ('3 = 2011 A1369 820-3023')
			print ()
			print ('4 = 2012 A1278 820-3115')
			print ('    2012 A1286 820-3330')
			print ('    late 2012 / early 2013 A1398 820-3332')
			print ('    late 2012 / early 2013 A1425 820-3462')
			print ('    2012 A1465 820-3208')
			print ('    2012 A1466 820-3209')
			print ()
			print ('5 = 2013/2014 A1502 820-3476')
			print ('    2013/2014 A1398 820-3662')
			print ('    2013/2014 A1465 820-3435')
			print ('    2013/2014 A1466 820-3437')
			print ()
			print ('6 = 2015 A1398 820-00138')
			print ('    2015 A1465 820-00164')
			print ('    2015-2017 A1466 820-00165')
			print ('    2015 A1502 820-4924')
			print ()
			print ('7 = 2017 A1706 820-00239')
			print ('    2017 A1707 820-00928')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-t", "--efi_type"):
			efi_type = arg
		elif opt in ("-s", "--patch_serial"):
			patch_serial = arg.upper()
		elif opt in ("-m", "--me_region_filename"):
			me_region_filename = arg
		elif opt in ("-r"):
			remove_lock = 'yes'

	#Get & Set Offset Variables from set_offsets function in offsets.py
	fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer = set_offsets(efi_type)

	#Variables
	filename = inputfile
	patch_hwc = patch_serial[8:12]

	#Open EFI Original file and get Fsys, CRC32 and Firmware Lock Sections
	with open(filename, 'rb') as content:
		entire_efi = content.read()
		content.close()

	with open(filename, 'rb') as content:
		fsys = content.seek(fsys_start_offset,0)
		fsys = content.read(fsys_buffer)
		crc32 = content.seek(fsys_end_offset,0) #fsys_end_offset is also crc32 offset
		crc32 = content.read(4)
		firmware_lock = content.seek(firmware_lock_start_offset,0)
		firmware_lock = content.read(firmware_lock_buffer)
		me_region = content.seek(me_region_start_offset,0)
		me_region = content.read(me_region_buffer)
		content.close()

	#Retrieve Serial Number:
	serial_offset = fsys.find(b'ssn')
	if (serial_offset == -1): # if = -1, then didn't find search term
		serial_offset = fsys.find(b'SSN')
		if (serial_offset == -1): # if still -1, then failed both searches
			serial_search = False
		else:
			serial_search = True
			serial_offset = serial_offset + 5
			serial_offset_end = serial_offset + 12
			serial = fsys[serial_offset:serial_offset_end]
	else:
		serial_search = True
		serial_offset = serial_offset + 5
		serial_offset_end = serial_offset + 12
		serial = fsys[serial_offset:serial_offset_end]

	#Retrieve Current HWC:
	hwc_offset = fsys.find(b'hwc')
	if (hwc_offset == -1): # if = -1, then didn't find search term
		hwc_offset = fsys.find(b'HWC')
		if (hwc_offset == -1): # if still -1, then failed both searches
			hwc_search = False
		else:
			hwc_search = True
			hwc_offset = hwc_offset + 5
			hwc_offset_end = hwc_offset + 4
			hwc = fsys[hwc_offset:hwc_offset_end]
	else:
		hwc_search = True
		hwc_offset = hwc_offset + 5
		hwc_offset_end = hwc_offset + 4
		hwc = fsys[hwc_offset:hwc_offset_end]
	
	#CRC32 Calculations for Original Fsys
	calc_crc32 = hex((binascii.crc32(fsys)))
	fixed_calc_crc32_1 = calc_crc32[-2:10]
	fixed_calc_crc32_2 = calc_crc32[-4:8]
	fixed_calc_crc32_3 = calc_crc32[-6:6]
	fixed_calc_crc32_4 = calc_crc32[-8:4]
	fixed_calc_crc32 = fixed_calc_crc32_1 + fixed_calc_crc32_2 + fixed_calc_crc32_3 + fixed_calc_crc32_4

	#Create Patched Fsys if Serial OK
	if(len(patch_serial) == 12):
		patched_fsys_part1 = fsys.replace(serial, binascii.a2b_qp(patch_serial))
		patched_fsys_part2 = patched_fsys_part1.replace(hwc, binascii.a2b_qp(patch_hwc))

		#CRC32 Calculations for Patched Fsys
		patched_calc_crc32 = hex((binascii.crc32(patched_fsys_part2)))
		fixed_patched_calc_crc32_1 = patched_calc_crc32[-2:10]
		fixed_patched_calc_crc32_2 = patched_calc_crc32[-4:8]
		fixed_patched_calc_crc32_3 = patched_calc_crc32[-6:6]
		fixed_patched_calc_crc32_4 = patched_calc_crc32[-8:4]
		fixed_patched_calc_crc32 = fixed_patched_calc_crc32_1 + fixed_patched_calc_crc32_2 + fixed_patched_calc_crc32_3 + fixed_patched_calc_crc32_4
		
		#Create Patched CRC32 
		final_patched_crc = binascii.unhexlify(fixed_patched_calc_crc32)
		
		#Compare Original and Patched Fsys Lengths
		fsys_comparison = check_length(fsys, patched_fsys_part2)

		if(fsys_comparison == True and serial_search == True and hwc_search == True):
			write_fsys = True
			fsys_message = 'Fsys Block Successfully Patched!'
		else:
			fsys_message = 'Fsys Block Not Patched! - Size Mismatch or Unable to Locate Serial / Hwc Offsets'

	else:
		fsys_message = 'Fsys Block Not Patched! - Serial Length Incorrect'

		
	#Firmware Lock Removal
	if(remove_lock == 'yes' and efi_type != '1'):
		
		lock_fill = b'\xFF' * firmware_lock_buffer
		lock_comparison = check_length(firmware_lock, lock_fill)

		if(lock_comparison == True):
			lock_message = 'Firmware Lock Successfully Removed!'
		elif(lock_comparison == False):
			lock_message = 'Firmware Lock Not Removed! - Size Mismatch'

	else:
		lock_message = 'Frimware Lock Not Removed! - Option not Selected or EFI Type = 1 (Type 1 not Supported)'

	
	# ME Region
	if(me_region_filename and efi_type != '1'):
		with open(me_region_filename, 'rb') as me_content:
			patch_me_region = me_content.read()
			me_content.close()

		me_comparison = check_length(me_region, patch_me_region)
		if(me_comparison == True):
			write_me = True
			me_message = 'ME Region Successfully Patched!'
		elif(me_comparison == False):
			me_message = 'ME REgion Not Patched! - File Size Mismatch'
	else:
		me_message = 'ME Region Not Patched - Option not Selected or EFI Type = 1 (Type 1 not Supported)'
	

	#Create and Write Patched EFI file
	patched_efi = open(outputfile, 'wb')
	patched_efi.write(entire_efi)
	
	if(write_me == True):
		patched_efi.seek(me_region_start_offset,0)
		patched_efi.write(patch_me_region)

	if(write_fsys == True):
		patched_efi.seek(fsys_start_offset,0)
		patched_efi.write(patched_fsys_part2)
		patched_efi.seek(fsys_end_offset,0)
		patched_efi.write(final_patched_crc)
	
	if(write_lock == True):
		patched_efi.seek(firmware_lock_start_offset,0)
		patched_efi.write(lock_fill)

	patched_efi.close()

	#Get Model Information:
	database = 'database.json'

	orig_model, search_orig_message = search_and_update_db(database, hwc.decode("utf-8"), database)
	patched_model, search_patch_message = search_and_update_db(database, patch_hwc, database)

	# Print Output
	print('Model Associated with Original Serial: ', orig_model, search_orig_message)
	print('Original Serial: ', serial.decode("utf-8"))
	print('Original Hwc: ', hwc.decode("utf-8"))
	print('Original CRC32 from file: ', binascii.hexlify(crc32).decode("utf-8"))
	if (write_fsys == True):
		print('Calculated CRC32 from extracted Fsys: ', calc_crc32)
		print('Fixed Calculated CRC32 from extracted Fsys (Reversed): ', fixed_calc_crc32)
		print('Model Associated with Patched Serial: ', patched_model, search_patch_message)
		print('Serial to Patch into Fsys: ', patch_serial)
		print('HWC to Patch into Fsys: ', patch_hwc)
		print('Calculated CRC32 from Patched Fsys: ', patched_calc_crc32)
		print('Fixed Calculated CRC32 from Patched Fsys (Reversed): ', fixed_patched_calc_crc32)
	print(fsys_message)
	print(lock_message)
	print(me_message)
	print('Patching Complete!')

if __name__ == "__main__":
	main(sys.argv[1:])
