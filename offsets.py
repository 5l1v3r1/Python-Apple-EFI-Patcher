#Offsets List:

def set_offsets(efi_type):
	# Offsets for: 
	# 2008 A1278 820-2327 (Needs more research for lock offsets)
	# Older 4MB EFI
	#if efi_type == '2008_A1278':
	if efi_type == '1':
		fsys_start_offset = 663552 # Offset = Begining of Fsys
		fsys_end_offset = 665596 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		#firmware_lock_start_offset = 7323724 # Offset = Beginning of Firmware Lock
		#firmware_lock_end_offset = 7331912 # Offset = End of Firmware Lock
		#firmware_lock_buffer = $firmware_lock_end_offset - $firmware_lock_start_offset # calculate size of lock
		# me_region_start_offset = 8192 # Offset = Beginning of ME Region
		# me_region_end_offset = 1630208 # Offset = End of ME Region
		# me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer #, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer


	# Offsets for: 
	# 2011 A1278 820-2936
	# 2011 A1286 820-2915
	#elif efi_type == '2011_A1278_A1286':
	elif efi_type == '2':
		fsys_start_offset = 7315456 # Offset = Begining of Fsys
		fsys_end_offset = 7317500 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		firmware_lock_start_offset = 7323724 # Offset = Beginning of Firmware Lock
		firmware_lock_end_offset = 7331912 # Offset = End of Firmware Lock
		firmware_lock_buffer = firmware_lock_end_offset - firmware_lock_start_offset # calculate size of lock
		me_region_start_offset = 4096 # Offset = Beginning of ME Region
		me_region_end_offset = 1576960 # Offset = End of ME Region
		me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer


	# Offsets for:
	# 2011 A1369 820-3023
	#elif efi_type == '2011_A1369':
	elif efi_type == '3':
		fsys_start_offset = 7282688 # Offset = Begining of Fsys
		fsys_end_offset = 7284732 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		firmware_lock_start_offset = 7290956 # Offset = Beginning of Firmware Lock
		firmware_lock_end_offset = 7299144 # Offset = End of Firmware Lock
		firmware_lock_buffer = firmware_lock_end_offset - firmware_lock_start_offset # calculate size of lock
		me_region_start_offset = 4096 # Offset = Beginning of ME Region
		me_region_end_offset = 1638400 # Offset = End of ME Region
		me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer


	# Offsets for:
	# 2012 A1278 820-3115
	# 2012 A1286 820-3330
	# late 2012 / early 2013 A1398 820-3332
	# late 2012 / early 2013 A1425 820-3462
	# 2012 A1465 820-3208
	# 2012 A1466 820-3209
	#elif efi_type == '2012_e2013_A1278_A1286_A1398_A1425_A1465_A1466'
	elif efi_type == '4':
		fsys_start_offset = 6881280 # Offset = Begining of Fsys
		fsys_end_offset = 6883324 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		firmware_lock_start_offset = 6889556 # Offset = Beginning of Firmware Lock
		firmware_lock_end_offset = 6897744 # Offset = End of Firmware Lock
		firmware_lock_buffer = firmware_lock_end_offset - firmware_lock_start_offset # calculate size of lock
		me_region_start_offset = 4096 # Offset = Beginning of ME Region
		me_region_end_offset = 1638400 # Offset = End of ME Region
		me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer


	# Offsets for:
	# 2013/2014 A1502 820-3476
	# 2013/2014 A1398 820-3662
	# 2013/2014 A1465 820-3435
	# 2013/2014 A1466 820-3437
	#elif efi_type == '2013_2014_A1398_A1465_A1466_A1502':
	elif efi_type == '5':
		fsys_start_offset = 6488064 # Offset = Begining of Fsys
		fsys_end_offset = 6490108 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		firmware_lock_start_offset = 6496340 # Offset = Beginning of Firmware Lock
		firmware_lock_end_offset = 6504528 # Offset = End of Firmware Lock
		firmware_lock_buffer = firmware_lock_end_offset - firmware_lock_start_offset # calculate size of lock
		me_region_start_offset = 8192 # Offset = Beginning of ME Region
		me_region_end_offset = 1638400 # Offset = End of ME Region
		me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer


	# Offsets for:
	# 2015 A1398 820-00138
	# 2015 A1465 820-00164
	# 2015-2017 A1466 820-00165
	# 2015 A1502 820-4924
	#elif efi_type == '2015_2017_A1398_A1465_A1466_A1502':
	elif efi_type == '6':
		fsys_start_offset = 5832704 # Offset = Begining of Fsys
		fsys_end_offset = 5834748 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		firmware_lock_start_offset = 5840980 # Offset = Beginning of Firmware Lock
		firmware_lock_end_offset = 5849168 # Offset = End of Firmware Lock
		firmware_lock_buffer = firmware_lock_end_offset - firmware_lock_start_offset # calculate size of lock
		me_region_start_offset = 8192 # Offset = Beginning of ME Region
		me_region_end_offset = 1630208 # Offset = End of ME Region
		me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer


	# Offsets for:
	# 2017 A1706 820-00239
	# 2017 A1707 820-00928
	#elif efi_type == '2017_A1706':
	elif efi_type == '7':
		fsys_start_offset = 1413120 # Offset = Begining of Fsys
		fsys_end_offset = 1415164 # Offset = End of Fsys - also crc32 offset
		fsys_buffer = fsys_end_offset - fsys_start_offset # used to calculate size of Fsys block
		# Wireless and Nand Info need to be added for this model A1706
		firmware_lock_start_offset = 1421396 # Offset = Beginning of Firmware Lock
		firmware_lock_end_offset = 1429584 # Offset = End of Firmware Lock
		firmware_lock_buffer = firmware_lock_end_offset - firmware_lock_start_offset # calculate size of lock
		me_region_start_offset = 8192 # Offset = Beginning of ME Region
		me_region_end_offset = 1273856 # Offset = End of ME Region
		me_region_buffer = me_region_end_offset - me_region_start_offset # calculate size of ME Region
		return fsys_start_offset, fsys_end_offset, fsys_buffer, firmware_lock_start_offset, firmware_lock_end_offset, firmware_lock_buffer, me_region_start_offset, me_region_end_offset, me_region_buffer
