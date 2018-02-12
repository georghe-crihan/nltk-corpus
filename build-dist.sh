#!/bin/sh

function build_jar()
{
local JYTHON_HOME="${1}"
local TARGET="${2}"
local DEST="${PWD}"

# Bug?: Somehow it needs the first imported module (script text file) toi
#       execute successfully. This happens to be the os.py
#       (see import_site_packages.py) in this case.
	cp "${JYTHON_HOME}/jython.jar" "${TARGET}"
	cd "${JYTHON_HOME}"
	zip -r "${DEST}/${TARGET}" 'Lib/' -i 'Lib/os.py' -i '*.class' -x \
		'Lib/site-packages/pip/*' \
		'Lib/site-packages/setuptools/*' \
		'Lib/site-packages/nltk/test/*' \
		'Lib/site-packages/chardet/*' \
		'Lib/site-packages/bs4/tests/*' \
		'Lib/site-packages/wcwidth/tests/*' \
		'Lib/json/tests/*' \
		'Lib/distutils/tests/*' \
		'Lib/email/test/*' \
		'Lib/unittest/*'
	cd "${DEST}"
# Arguably
	zip -d "${TARGET}" \
		'org/python/tests/*' \
		'org/python/bouncycastle/util/test/*'
}

function set_entrypoint()
{
local TARGET="${1}"

#	echo "Main-Class: org.python.util.JarRunner" > manifest.txt
#	jar umf manifest.txt "${TARGET}"
#	rm -f manifest.txt
	jar ufe "${TARGET}" org.python.util.JarRunner
}

function add_scripts()
{
local TARGET="${1}"

	TERM=xterm-color jython -c '
import import_site_packages
import sqlite3
import __run__
'
# Sadly, currently does not work
#	cp '__run__$py.class' '__main__$py.class'
	zip "${TARGET}" 'import_site_packages$py.class' '__run__$py.class' 'sqlite3$py.class'
	rm -f 'import_site_packages$py.class'
}

TARGET="${1}"

if [ -z "${TARGET}" ]; then
	echo "Usage: build-dist.sh target.jar"
	exit 1
fi

rm -f "${TARGET}"
build_jar "/opt/local/share/java/jython" "${TARGET}"
set_entrypoint "${TARGET}"
add_scripts "${TARGET}"
ls -lh "${TARGET}"

