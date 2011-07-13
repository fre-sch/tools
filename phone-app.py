#!/usr/bin/env python
import re

def default_number_writer( instance, country_code="", area_code="", number="" ):
  area_code_formatted = []
  t = area_code[:2]
  while t:
    area_code_formatted.append( t )
    area_code = area_code[2:]
    t = area_code[:2]
  number_formatted = []
  t = number[:2]
  while t:
    number_formatted.append( t )
    number = number[2:]
    t = number[:2]
  return "%s (%s) %s" % (
    country_code,
    " ".join( area_code_formatted ),
    " ".join( number_formatted ) )

default_number_reader_rex = re.compile(
# country_code
"\s*([\d\s]*)"
# area_code in parenthesis
"\(([\d\s]*)\)"
# number
"\s*([\d\s]*)" )
def default_number_reader( number_string ):
  all_match = default_number_reader_rex.search( number_string )
  number = { "country_code": "", "area_code": "", "number": "" }
  if not all_match: return number
  number_keys = [ "country_code", "area_code", "number" ]
  key_index = 0
  for g in all_match.groups():
    number[ number_keys[ key_index ] ] = g.replace( " ", "" )
    key_index += 1
  return number

class Number( object ):
  Writer = None
  Reader = None
  def __init__( self, country_code="", area_code="", number="" ):
    self.country_code = country_code
    self.area_code = area_code
    self.number = number
  def __str__( self ):
    return self.Writer(
      self.country_code, self.area_code, self.number )
  @classmethod
  def from_string( cls, number_string ):
    return cls( **cls.Reader( number_string ) )

class Person( object ):
  def __init__( self ):
    self.name = None
    self.numbers = []
  def __str__( self ):
    return "%s\n\t%s" % ( self.name,
      "\n\t".join( map( str, self.numbers ) ) )

class App( object ):
  def __init__( self ):
    self.file_name = ""
    self.list_as_text = ""
    self.list_objects = []
  
if __name__ == "__main__":
  Number.Writer = staticmethod(default_number_writer)
  Number.Reader = staticmethod(default_number_reader)
  number = { "country_code": "04",
    "area_code": "06151",
    "number": "3681959", }
  instance = Number( **number )
  print instance
  number_string = "04 (06 15 1) 36 81 95 9"
  instance = Number.from_string( number_string )
  print instance
