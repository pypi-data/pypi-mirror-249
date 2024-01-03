

'''
	{ verify, approve, validate, certify, vouch }
'''

'''
	import earring.modules.ED448.vouch as vouch
	vouched = vouch.start (
		public_key_string,
		signed_bytes = signed_bytes,
		unsigned_bytes = unsigned_bytes
	)
'''

from Crypto.Signature import eddsa
from Crypto.PublicKey import ECC

def start (
	public_key_string,
	unsigned_bytes,
	signed_bytes
):
	public_key_instance = ECC.import_key (public_key_string)
	voucher = eddsa.new (public_key_instance, 'rfc8032')
	
	try:
		voucher.verify (unsigned_bytes, signed_bytes)		
		return True;
		
	except Exceptions as E:
		pass;
				
	return False;