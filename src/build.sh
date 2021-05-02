#!/bin/bash
environment(){
	if $requse
	then
		echo "Installing packages using "$reqfile
		python$1 -m pip$1 install -r $reqfile
	else
		echo "Installing packages using pip$1"
		pip$1 install pyinstaller
		pip$1 install pyserial
		pip$1 install matplotlib
		pip$1 install twilio
		pip$1 install numpy
		pip$1 install python$1-tk
	fi
}

moveplugin(){
	echo "Moving Plugin"
	cp graph.py ./dist/app/graph.py
	cp sms.py ./dist/app/sms.py
	cp ic.ico ./dist/app/ic.ico
	#cp graph.py ./build/app/graph.py
	#cp sms.py ./build/app/sms.py
	#cp ic.ico ./build/app/ic.ico
}


buildfile(){
	echo "Building exectuable"
	path=$1
	pyinstaller --onedir $path
	if $2
	then
		moveplugin
	fi
}

usage(){
	echo "options:--------------------------------------------------------------------------------------"
	echo "-e     : Setup env with just pip      [ build.sh -e ]"
	echo "-e -v  : Setup env with sepific version of pip	       [build.sh -e -v <version_number>]"
	echo "-e -r  : Setup env using requirements file	[build.sh -e -r <requirements_file path>]"
	echo "-b     : Build executable		[ build.sh -b <python file path> ]"
	echo "-f     : Full install with plugin(needs config)		[ build.sh -f -b <python file path> ]"
	echo "-m     : Move plugin scripts to build		[ build.sh -m ]"
	echo "-h     : Show options      [ build.sh -h ]"
	echo "----------------------------------------------------------------------------------------------"
	echo ""
	echo "usage:----------------------------------------------------------------------------------------"
	echo "[ build.sh -e ]"
	echo "[build.sh -e -v < version alias eg. 3 >]"
	echo "[build -e -r <requirements_file>]"
	echo "[ build.sh -b <python file path> ]"
	echo "[ build.sh -f -b <python file path> ]"
	echo "[ build.sh -h ]"
	echo "----------------------------------------------------------------------------------------------"
}

bflag=false
eflag=false
fullflag=false
requse=false
unset pipv
unset reqfile
while getopts "ev:r:b:fhm" opt; do
	case $opt in
		e) 		eflag=true;;
		v)		pipv=$OPTARG;;
		r)		requse=true
				reqfile=$OPTARG;;
		b)		bflag=true
				target=$OPTARG;;
    		h)		usage ;;
		f)		fullflag=true;;
		m)		moveplugin;;
    		*)		usage;;
    esac
done

if $eflag
then
	environment $pipv
fi

if $bflag
then
	buildfile $target $fullflag
fi
