from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from django.db.utils import IntegrityError

from catalog.models import *

def work_on_line(line, counter):
	return counter




"""

from tools.parsing_betaparts.save_prods import *

file = open('prods.text', 'r')
counter = 0
for line in file.readlines():
	if line.replace(' ', '') != '':
		counter = work_the_line(line, counter)

"""
# rootadminboss
# PasswordThatNooneCanHack4NoRe4sonyesididuseonethingfordifferentMea09