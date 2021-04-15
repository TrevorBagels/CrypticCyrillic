import random, json, argparse, sys, binascii
import hashlib
from typing import NewType

class Signer:
	def __init__(self, frequency = .7):
		self.freq = frequency
		self.dictionary = {}
		with open("dictionary.json", "r") as f: self.dictionary = json.loads(f.read())
		#remove all things that we need to exclude
		for value in self.dictionary['exclude']:
			key = ""
			for k, v in self.dictionary['characters'].items():
				if v == value:
					key = k
			if key != "":
				del self.dictionary['characters'][key]
		#ok, now that we've removed unwanted items, turn the dictionary into an actual list of keys and values
		self.dictionary = self.dictionary['characters']
	
	def sign_text(self, txt):
		"""Signs the text
		"""
		new_txt = ""
		for c in txt:
			if c in self.dictionary:
				do_sign = random.random() <= self.freq
				if do_sign:
					new_txt += self.dictionary[c]
				else:
					new_txt += c
			else:
				new_txt += c
		return new_txt

	def sign_secret(self, txt, secret):
		#convert the secret to binary
		binary:str = ''.join(format(ord(i), '08b') for i in secret)
		binary_index = 0
		new_txt = ""
		for c in txt:
			if c in self.dictionary:
				do_sign = False
				if binary_index < len(binary):
					do_sign = int(binary[binary_index]) == True
					binary_index += 1
				if do_sign:
					new_txt += self.dictionary[c]
				else:
					new_txt += c
			else:
				new_txt += c
		return new_txt
	
	def get_secret(self, txt):
		bits = ""
		inverted_dict = {v: k for k, v in self.dictionary.items()}
		for c in txt:
			if c in self.dictionary:
				bits += "0"
			elif c in inverted_dict:
				bits += "1"
		#now convert the binary
		bits2 = ""
		for x in range(len(bits) // 8):
			block = bits[x*8:][:8]
			if block == "00000000": break
			bits2 += block
		n = int(bits2, 2)
		secret = binascii.unhexlify('%x' % n).decode()
		return secret


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("--text", default=None, help="The raw text to hash.")
	ap.add_argument("--output", default=None, help="The file to output to. If not specified, it will print to stdout instead.")
	ap.add_argument("--readfrom", default=None, help="The file to read from. Disables raw text input.")
	ap.add_argument("--frequency", default=.7, help="How often to sign a letter with cyrillic.")
	ap.add_argument("--secret", default=None, help="Use this to encrypt a secret message")
	ap.add_argument("--getsecret", default=False, action="store_true", help="Use this to decrypt a secret message")
	args = ap.parse_args()

	

	txt = args.text
	if txt == None:
		if args.readfrom != None:
			with open(args.readfrom, "r") as f:
				txt = f.read()
		else:
			print("No input!")
			sys.exit()
	

	signer = Signer(frequency=args.frequency)
	normal_sign = False #indicates that this was signed normally, using random to make the signature
	if args.secret != None:
		signed = signer.sign_secret(txt, args.secret)
	elif args.getsecret:
		signed = signer.get_secret(txt)
	else:
		signed = signer.sign_text(txt)
		normal_sign = True

	#in case the signed text is the same as the original. only really happens in short strings
	if signed == txt and normal_sign:
		while True:
			signed = signer.sign_text(txt) #make new signed text
			if signed == txt: #still the same. increase the frequency and try again
				signer.freq += .1
			else:
				break
			if signer.freq >= 1:
				print("Could not sign this text! ")
				sys.exit()
	

	if args.output == None:
		print(signed)
	else:
		with open(args.output, "w+") as f:
			f.write(signed)
	

"""Examples
python3 main.py --text "1234"
	will not work, because 1234 doesn't contain any characters that look like they're from cyrillic

python3 main.py --text "hello world"
	will apply some cyrillic to "hello world"

python3 main.py --readfrom testinput.txt 
	will use the contents of testinput.txt as the input

python3 main.py --readfrom testinput.txt --output test.txt
	will output signed text to test.txt

python3 main.py --readfrom testinput.txt --output test.txt --secret "hi there"
	when signing, this will embed a secret message in binary. someone using the same dictionary configuration can decode this message.

python3 main.py --readfrom test.txt --getsecret
	reading from test.txt (where we stored the secret message), this will decrypt a secret binary message and print it to stdout.

"""