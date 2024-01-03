

'''
	#
	#	write private key to path
	#
	import earring.modules.ED448.private.creator as ED448_private_key_creator
	private_key = ED448_private_key_creator.create (seed, format, path)
	if (private_key ["success"] == "yes"):
		private_key_class = private_key ["class"]
		private_key_string = private_key ["string"]
		
'''

'''
	import earring.modules.ED448.private.creator as ED448_private_key_creator
	private_key = ED448_private_key_creator.create (seed, format)
	if (private_key ["success"] == "yes"):
		private_key_class = private_key ["class"]
		private_key_string = private_key ["string"]
'''



'''
	seed:
		4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8
		5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8
		4986888B11358BF3D541B41EEA5DAECE1C6EFF64130A45FC8B9CA48F3E0E02463C99C5AEDC8A847686D669B7D547C18FE448FC5111CA88F4E8
		
	format:
		DER
		PEM
'''
from Crypto.PublicKey.ECC import EccKey
import os.path

def write_private_key (path, private_key_string, format):
	if (os.path.exists (path)):
		raise Exception (f"The path for the private_key is not available. '{ path }'");
	
	if (format == "DER"):
		f = open (path, 'wb')
	elif (format == "PEM"):
		f = open (path, 'w')
	else:
		raise Exception (f"format '{ format }' was not accounted for.")
	
	f.write (private_key_string)
	f.close ()
	
	return True


def create (
	seed, 
	format, 
	
	path = ""
):	
	assert (len (path) >= 1)
	assert (len (seed) == 114)

	private_key_class = EccKey (
		curve = "Ed448", 
		seed = bytes.fromhex (seed)
	)
	private_key_string = private_key_class.export_key (format = format)	
	write_private_key (path, private_key_string, format)
	
	return {		
		"instance": private_key_class, 
		"string": private_key_string
	}