#!/usr/bin/env python

import sys, os, glob
from optparse import OptionParser

class Palette(object):
	def __init__( self ):
		self.name = ""
		self.colums = ""
		self.colors = {}
	
	def asHtmlColor( self, name ):
		return "#%02x%02x%02x" % tuple(self.colors[ name ])
	
	def asGtkRcColor( self, name ):
		return "{ %.2f, %.2f, %.2f }" % tuple(map(lambda c: c / 255.0, self.colors[ name ] ))
	
	@classmethod
	def load( _class, file_name ):
		p = _class()
		f = file( file_name )
		lines = f.readlines()
		p.name = lines[ 1 ].strip()
		p.colums = lines[ 2 ].strip()
		for line in lines[ 4: ]:
			parts = line.strip().split()
			p.colors[ " ".join( parts[ 3: ] ) ] = map( int, parts[ :3 ] )
		return p

def main():
	"""usage: %prog <palette> <files>
	"""
	palette_dir = os.path.expanduser( "~/" )
	palette
	parser = OptionParser( main.__doc__ )
	#parser.add_option( "-c", "--case-sensitive", action="store_true", dest="case_sensitive",
	#	help="Case sensitive matching (default is ignore case)" )
	options, args = parser.parse_args()
	
	
