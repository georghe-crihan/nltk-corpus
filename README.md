# NLTK-Corpus

This is a set of NLTK scripts to create personal vocabulary kernel.
It is to be used to aid learning new foreing languages.

It uses Jython both, for portability and ease of distribution (Java is nearly
everywhere nowadays) and speed (JVM is up to 10 times faster than Python
bytecode).

To aid development, it uses Nailgun (cuts down JVM loading times).

The following preprocessor backends are planned:
- from *.webarchive files - easily extract conversations from VK.com and others.
- from *.mbox files - process personal mail
- from IMAP mail servers - process corporate mail

Microsoft Outlook databases are out of scope at this moment. They lack Jython
support and would use native WIN32 interfaces. Perhaps it could be possible to
access them through JAVA libraries.

## Notes
NLTK distribution could be both patched and made into thinking there is a
Python-like Sqlite3 support in Jython (see patches).

It has a nice script for building the standalone fat jar distribution as well.
