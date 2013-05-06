#!/usr/bin/python
#encoding: utf-8

import sys
import subprocess
import shlex
import urllib
import os

def arindex(source, text):
	result = 0
	try:
		result = source.rindex(text) + 3
	except ValueError:
		result = 0	
	return result

def speak(argtext = ""):
	# Initialize
	LENGTH = 300

	ARGCURL = ["curl", "--silent", "--user-agent", "\"Safari/1.0\""]
	URI1 = "http://translate.google.com/translate_tts?q="
	URI2 = "&tl=en"
	TMP = "/tmp/gjsay"
	ARGMPG = ["mpg321", "--quiet"]
	TIMEOUT = 10

	if os.path.isdir(TMP) == False:
		os.mkdir(TMP)


	# Arguments
	source = ""
	if argtext == "":
		if len(sys.argv) == 1:
			source = raw_input("Enter text : ")
		else:
			i = 1
			while i < len(sys.argv):
				source += sys.argv[i] + " "
				i += 1
	else:
		source = argtext
		
	i = 0
	count = 0
	while i < len(source): 
		# Split
		s = source[i:i + LENGTH]
		splitpos = []
		splitpos.append(arindex(s, "。"))
		splitpos.append(arindex(s, "、"))
		splitpos.append(arindex(s, ","))
		splitpos.append(arindex(s, "."))
		splitpos.append(arindex(s, " "))

		split = 0
		if max(splitpos) == 0:
			splitpos.append(arindex(s, "は"))
			splitpos.append(arindex(s, "が"))
			splitpos.append(arindex(s, "を"))
			splitpos.append(arindex(s, "に"))
			if max(splitpos) == 0:
				split = len(s)
			else:
				split = LENGTH
		else:
			split = max(splitpos)

		text = s[0:split]

		# Encode
		enc = urllib.quote(text)

		# File name
		path = TMP + "/" + str(count) + ".mp3"

		# Launch "curl"
		argcurl = ARGCURL[:]
		argcurl.append(URI1 + enc + URI2)

		curl = subprocess.Popen(argcurl, stdout = open(path, "w"))
		if curl.wait() != 0:
			print("Couldn't get file : curl")
			sys.exit(1)

		# Play
		argmpg = ARGMPG[:]
		argmpg.append(path)
		mpg = subprocess.Popen(argmpg)
		if mpg.wait() != 0:
			print("Couldn't play file : mpg321")
			sys.exit(1)

		# Increment
		i += split
		count += 1

	# Remove
	count -= 1
	while count >= 0:
		os.remove(TMP + "/" + str(count) + ".mp3")
		count -= 1
	os.removedirs(TMP)

	return 0

if __name__ =='__main__':
	speak()

