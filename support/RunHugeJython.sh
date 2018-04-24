#!/bin/sh
JYTHON_HOME=/opt/local/share/java/jython
HEAP_SZ=6

TERM=xterm-color \
	/usr/bin/java \
	-Xss2560k \
	-Xnoclassgc \
	-Xms${HEAP_SZ}G \
	-Xmn$(( ${HEAP_SZ} / 2 ))G \
	-classpath ${JYTHON_HOME}/jython.jar:./target/minimal-pom-1.0-SNAPSHOT-jar-with-dependencies.jar:. \
	-Dpython.home=${JYTHON_HOME} \
	-Dpython.executable=${JYTHON_HOME}/bin/jython \
	-Dpython.launcher.uname=darwin \
	-Dpython.launcher.tty=true \
	-Dpython.cachedir=/Users/mac/.jython_cachedir \
	-Dfile.encoding=UTF-8 \
	org.python.util.jython \
	${@}

