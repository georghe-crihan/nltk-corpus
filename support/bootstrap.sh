#!/bin/sh
# From here: https://stackoverflow.com/questions/1348842/what-should-i-set-java-home-to-on-osx

JAVA_HOME=$(/usr/libexec/java_home)
#JAVA_HOME=$(/usr/libexec/java_home -v 1.5)
#sudo ln -s /System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/java_home /usr/libexec/java_home
export JAVA_HOME
EPUBCHECK=/Users/mac/Downloads/epubcheck-4.0.2
CLASSPATH="${EPUBCHECK}/lib/*:${EPUBCHECK}/*:/Users/mac/bin/*:${CLASSPATH}"
export CLASSPATH
nohup java com.martiansoftware.nailgun.NGServer &
sleep 2
# Set up aliases
ng ng-alias ng-epubcheck com.adobe.epubcheck.tool.Checker 
# These are for the NLTK scripts being developed.
ng ng-cp /Users/mac/jython-dist/myapp.jar
ng ng-alias ng-jarrunner org.python.util.JarRunner
ng ng-alias ng-jython org.python.util.jython

