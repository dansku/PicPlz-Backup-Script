#-----------------------------------------------------------------------------
#	Script to Backup all your photos from PicPlz
#	
#	Daniel Spillere Andrade - www.DanielAndrade.net
#
#	Usage: download the file to some folder, and under terminal
#	python main.py, enter your username and you are good to go! :)
#
#-----------------------------------------------------------------------------

import urllib2
import simplejson
import os
from datetime import datetime

#Clear Screen
os.system('clear')

print '--------------------------------'
print 'Welcome to PicPlz Backup Script'
print '--------------------------------\n'


username = raw_input("Enter your username: ")
jsonurl = 'https://api.picplz.com/api/v2/user.json?include_pics=1&pic_page_size=5000&username='+username+'&include_geo=1'

#---------[ Functions ]-------------------#

def download(url):
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])

	name = 'Bytes'

	if file_size > 1000 and file_size < 1000000:
		file_size = file_size / 1000
		name = 'Kbytes'
	elif file_size > 1000000:
		name = 'Mbytes'
		file_size = file_size / 1000000

	print "Downloading: %s %s%s" % (file_name, file_size, name)

	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break

		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		print status,

	f.close()

def captionReplace(caption):
	for char in ('!','?', '#', '(', ')', '+', ':', '.', '/', '\\', ','):
		caption=caption.replace(char, '')
	for char in (' ', '='):
		caption=caption.replace(char, '_')
	return caption

#---------[ Download & Save]--------------#

# Fetch JSON
json = urllib2.urlopen(jsonurl).read()
j = simplejson.loads(json)

x=1
# Get the total number of pics
for c in j['value']['users'][0]['pics']:
	x=x+1

# Download and rename
for c in j['value']['users'][0]['pics']:
	fileUrl = c['pic_files']['640r']['img_url']
	fileName = fileUrl.split('/')[-1]
	caption = captionReplace(c['caption'])
	date = c['date']
	date = datetime.fromtimestamp(date)
	download(fileUrl)
	x=x-1
	print 'Renaming '+fileName+' to '+str(x)+'_'+caption+'.jpg'
	os.rename(fileName,str(x)+'_'+caption+'.jpg')

print 'Done!'

