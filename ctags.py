import os
import sys
import gtk
import subprocess

class CtagsTag( object ):
  def __init__( self, lang, name, desc, active=True ):
    self.lang = lang
    self.name = name
    self.desc = desc
    self.active = active

  def __str__( self ):
    return "%s: %s" % (self.name,self.desc.capitalize())

class CtagsLang( object ):
  def __init__( self, name, active=True ):
    self.name = name
    self.active = active
    self.tags = {}
    self.tkeys = []

  def add_tag( self, tag ):
    self.tags[ tag.name ] = tag
    self.tkeys = self.tags.keys()
    self.tkeys.sort()

  def __str__( self ):
    tags = "\n\t".join( [ str( tag ) for tag in self.tags.values() ] )
    return "Tags for %r:\n\t%s\n" % ( self.name, tags )

class Ctags( object ):
  def __init__( self ):
    self.langs = {}
    self.lkeys = []

  def add_lang( self, lang ):
    self.langs[ lang.name ] = lang
    self.lkeys = self.langs.keys()
    self.lkeys.sort()

  def init_langs( self ):
    process = self.get_process( "--list-languages" )
    process.wait()
    for lang_name in process.stdout.readlines():
      lang = CtagsLang( lang_name.strip() )
      self.langs[ lang.name ] = lang
    self.lkeys = self.langs.keys()
    self.lkeys.sort()

  def init_tags( self ):
    for lang in self.langs.values():
      process = self.get_process( "--list-kinds=%s" % lang.name )
      process.wait()
      for line in process.stdout.readlines():
        line = line.strip().split()
        tag_name = line[ 0 ]
        tag_desc = " ".join( line[1:] )
        lang.tags[ tag_name ] = CtagsTag( lang, tag_name, tag_desc )
      lang.tkeys = lang.tags.keys()
      lang.tkeys.sort()

  def get_process( self, *ctags_args ):
    ctags_args = list( ctags_args )
    ctags_args.insert( 0, "ctags" )
    return subprocess.Popen(
      args = ctags_args,
      stdin = subprocess.PIPE,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      env = os.environ )

  class CtagsLangsTreeModel(gtk.GenericTreeModel):
    """
    Iterators of this model:
    ( lang_name:string, tag_name:string )
    """
    def __init__( self, ctags, *args, **kwargs ):
      gtk.GenericTreeModel( self, *args, **kwargs )
      self.ctags = ctags

ctags = Ctags()
ctags.init_langs()
ctags.init_tags()
for lang_name in ctags.lkeys:
  print ctags.langs[ lang_name ]


