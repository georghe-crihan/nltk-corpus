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
local UPD="${2}"
local NG="${3}"
local CMD1
local CMD2

	if [ -z "${NG}" ]; then
		CMD1='jython'
	else
		CMD1='ng ng-jython'
	fi

	if [ -n "${UPD}" ]; then
		CMD2='-f'
	fi

	TERM=xterm-color ${CMD1} -c '
import import_site_packages
import sqlite3
import __run__
#reload(import_site_packages)
#reload(sqlite3)
reload(__run__)
'
# Sadly, currently does not work
	cp '__run__$py.class' '__main__$py.class'
        DIST=${PWD}
        rm -rf /tmp/jardeps; mkdir /tmp/jardeps
        (cd /tmp/jardeps; jar -xf ${DIST}/target/*-jar-with-dependencies.jar;
        zip -r ${CMD2} "${DIST}/${TARGET}" . -x META-INF/MANIFEST.MF)
        zip -r ${CMD2} "${TARGET}" 'import_site_packages$py.class' '__run__$py.class' 'sqlite3$py.class' '__main__$py.class' \
            ./analysis/ -i '*.class'
        rm -rf /tmp/jardeps 'import_site_packages$py.class'
}



while [ "${#}" -gt 0 ]; do 
	case "${1}" in
	-u)
		shift
		UPD=1
	  ;;
	-ng)
		shift
		NG=1
	  ;;
	*)
	# Must be the TARGET filename
		break
	  ;;
	esac
done

TARGET="${1}"

if [ -z "${TARGET}" ]; then
	echo "Usage: build-dist.sh [-u] [-ng] target.jar"
	exit 1
fi

if [ -z "${UPD}" ]; then
	rm -f "${TARGET}"
	build_jar "/opt/local/share/java/jython" "${TARGET}"
	set_entrypoint "${TARGET}"
fi

# Build dependencies fat jar.
mvn package
add_scripts "${TARGET}" "${UPD}" "${NG}"
ls -lh "${TARGET}"

