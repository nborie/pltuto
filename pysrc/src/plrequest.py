#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  request.py
#  
#  Copyright 2017 Dominique Revuz <dr@univ-mlv.fr>
#  

__doc__ = """

	Ce fichier a pour objectif de gérer les comunications
	avec la sandbox.
	"""


import requests
import question
import zipfile
import pathlib

import cd
import subprocess

class SanboxSession:
	def __init__(self,question,url,studentfile):
		self.question = question
		self.url = url
		self.call(studentfile)

	def createEnvZipRun(self):
		from shutil import rmtree
		rmtree('/tmp/env/', ignore_errors=True)
		p=pathlib.Path('/tmp/env/')
		p=self.question.createdir(p)
		self.zipname = str(p.resolve() /  "env.zip")
		with cd.cd(str(p)) :
			subprocess.run(['zip','-qjr','env.zip','.'])
			

	def createEnvFile(self):
		from shutil import rmtree
		rmtree('/tmp/env/', ignore_errors=True)
		p=pathlib.Path('/tmp/env/')
		p=self.question.createdir(p)
		with zipfile.ZipFile('/tmp/env.zip','w') as zfile :
			for filename in p.iterdir():
				print(filename)
				zfile.write(str(filename))
			zfile.printdir()

	def checkgrader(self):
		self.question.checkgrader()

	def call(self,studentfile):
		self.createEnvZipRun()
		self.checkgrader()
		self.files = {'environment': open(self.zipname, 'rb'),'student.py':studentfile,"grader.py":self.question.dico['grader']}
		print(self.zipname)	
		self.answer = requests.post(self.url,data=self.question.dico,files=self.files,timeout=1000)
		return self.answer

