import random, argparse, sys

class MessageHider:
	def __init__(self, seed=303):
		random.seed(seed)
		self.letterindex = list(" abcdefghijklmnopqrstuvwxyz0123456789,.?;:\"'=+-_)(*&^%$#@!|[]}{/\\`~<>\n\t")
		for x in self.letterindex.copy():
			if x.upper() != x: self.letterindex.append(x.upper())
		random.shuffle(self.letterindex)
		self.letterindex = "".join(self.letterindex)
		self.letterindex = "∆" + self.letterindex
		

	def encode(self, spam, secret):
		i = 0
		offset = 0
		newtxt = spam
		for index, x in enumerate(secret):
			i = index + offset
			newtxt = newtxt[:i] + (self.letterindex.index(x) * "\u200E") + newtxt[i:]
			offset += self.letterindex.index(x)
		return newtxt

	def decode(self, spam):
		indexes = []
		current = 0
		for i in spam:
			if i == "\u200E":
				current += 1
			elif i != "\u200E" and current > 0:
				indexes.append(current)
				current = 0
		txt = ""
		for index in indexes:
			txt += self.letterindex[index]
		return txt

def read_from(file, txt):
	if file == None: return txt
	try:
		with open(file, "r") as f: return f.read()
	except:
		print("File \"" + file + "\" does not exist!")
		sys.exit()
	


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("--spam", default=None, help="Some spam to hide a message in or find a message from. ")
	ap.add_argument("--spamfile", default=None, help="File to read spam from. ")
	ap.add_argument("--message", default=None, help="The message to hide")
	ap.add_argument("--messagefile", default=None, help="The message to hide")
	ap.add_argument("--output", default=None, help="The file to output to. If not specified, it will print to stdout instead.")
	ap.add_argument("--seed", default=300, help="Use this to encrypt a secret message")
	args = ap.parse_args()
	
	mh = MessageHider(seed=args.seed)
	
	spam = read_from(args.spamfile, args.spam)
	message = read_from(args.messagefile, args.message)
	if spam == None:
		print("Spam wasn't provided. Exiting...")
		sys.exit()
	output = None
	if message == None:
		output = mh.decode(spam)
	else:
		output = mh.encode(spam, message)
	if args.output != None:
		with open(args.output, "w+") as f:
			f.write(output)
			print("Output saved to " + args.output)
	else:
		print(output)

#Create secret message
#python3 encrypt_invisible.py --spamfile "spam.txt" --message "hello world" --output output.txt

#Decrypt secret message
#python3 encrypt_invisible.py --spamfile output.txt