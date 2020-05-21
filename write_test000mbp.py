START = bytes.fromhex('7465 73743030305f504152000000000000000000000000000000000000000000000000005e91e9ae5e91e9ae00000000000000000000000000000000425041524d4f4249')

LONG_DATA = bytes.fromhex("4441 5441 0000 0054 4542 4152 0000 00010000 0000 4542 5653 0000 0004 ffff ffff0000 0001 0000 0008 ffff ffff 0000 00000000 000c 0000 0004 0000 0005 0000 00080000 0003 0003 0002 0000 0000 0003 00020000 0000 0000 0000 0000 fdea")

SHORT_DATA = bytes.fromhex("4441 5441 0000 0000")

BPAR = bytes.fromhex("42 50 41 52 00 00 00 38 FF FF FF FF 00 00 00 00 00 00 00 01 00 00 00 04 FF FF FF FF 00 00 00 7F FF FF FF FF DC E3 F4 84 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00")

BKMK_color = bytes.fromhex("00000000 00000001 00ffff0f 00000004")

highlights = [(5,9),(0,4)]

bkmk_length = 60

num_of_entries = 2 + 3*len(highlights)
print("{:>30} {}".format("num_of_entries", num_of_entries))
bpar_pos = len(START)+2+8+2+num_of_entries*8
print("{:>30} {}".format("bpar_pos", bpar_pos))
bpar_length = len(BPAR)
print("{:>30} {}".format("bpar_length", bpar_length))
print(bpar_pos+bpar_length)
with open("test000.mbp", "wb") as file:
	file.write(START) #Start until BPAR MOBI
	file.write(num_of_entries.to_bytes(4,'big')) #pointer_id
	file.write(b'\x00\x00')
	file.write(num_of_entries.to_bytes(4,'big')) #number_of_entires
	#BPAR pointer
	file.write(bpar_pos.to_bytes(4,'big')) #bpar pos
	file.write((0).to_bytes(4,'big')) #bpar id

	pointer_address = bpar_pos + bpar_length
	for i in range(len(highlights)): #print DATA pointers
		#Long data
		file.write(pointer_address.to_bytes(4,'big')) #address
		file.write((3*i+1).to_bytes(4,'big')) #index
		pointer_address += len(LONG_DATA)
		#Short data
		file.write(pointer_address.to_bytes(4,'big')) #address
		file.write((3*i+2).to_bytes(4,'big')) #index
		pointer_address += len(SHORT_DATA)

	#Last Long data
	file.write(pointer_address.to_bytes(4,'big')) #address
	file.write((3*len(highlights)+1).to_bytes(4,'big')) #index
	pointer_address += len(LONG_DATA)

	for i in range(len(highlights)): #print BKMK pointers
		file.write(pointer_address.to_bytes(4,'big')) #address
		file.write((3*(i+1)).to_bytes(4,'big')) #index
		pointer_address += bkmk_length

	file.write(b'\x00\x00')

	file.write(BPAR) #write BPAR
	for i in range(len(highlights)): #write DATA
		file.write(LONG_DATA) 
		file.write(SHORT_DATA)

	file.write(LONG_DATA) #last DATA

	for index in range(len(highlights)): #Write BKMKs of highlights
		file.write(b'\x42\x4b\x4d\x4b')#print BKMK name
		file.write((52).to_bytes(4,'big'))#size
		file.write(highlights[index][0].to_bytes(4,'big')) #start highlight
		file.write(highlights[index][1].to_bytes(4,'big')) #end   highlight
		file.write(BKMK_color)
		file.write((3*index + 2).to_bytes(4,'big')) #pointer to DATA
		file.write(b'\xff\xff\xff\xff')
		file.write((3*index + 1).to_bytes(4,'big')) #pointer to DATA
		file.write(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

