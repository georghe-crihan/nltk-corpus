# Make sure we have site-packages in our classpath
from java.io import File
from os import path
from sys.path import append 
from org.python.core.util import FileUtil as _dummy

# To avoid hardcoding myapp.jar...
_jar_file = File(_dummy().__class__.getProtectionDomain() \
  .getCodeSource() \
  .getLocation() \
  .getPath()) \
  .getName()

append(path.join(path.dirname(path.abspath(__file__)) \
  .replace('__pyclasspath__',''), _jar_file, 'Lib', 'site-packages'))
