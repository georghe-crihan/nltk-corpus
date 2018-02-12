# Drop-in replacement for Python sqlite3 to allow running from under Jython.
# The sqlite3 module is implemented as native in Python, hence it is replaced
# here with Java.
# NB: This is only a lite patch and by no means a fully-functional replacement.
# It only allows to run certain NLTK modules (nltk/corpus/reader/panlex-lite.py,
# nltk/corpus/reader/sem80.py but probably NOT nltk/sem/relextract.py).
# It works grace to the fact that Python imports any module exactly once, or,
# rather, the sqlite3 mimic module being in the CLASSPATH.

from java.lang import Class
from java.sql  import DriverManager, SQLException
 
def connect(conn_str):
    _JDBC_URL = 'jdbc:sqlite:%s' % ( conn_str, )
    return getConnection(_JDBC_URL, "org.sqlite.JDBC")
