#!/bin/bash
environment(){
	echo "Install pyinstaller"
	pip install pyinstaller
}

moveplugin(){
	echo "Moving Plugin"
	cp graph.py ./dist/app/graph.py
	cp sms.py ./dist/app/sms.py
	#cp graph.py ./build/app/graph.py
	#cp sms.py ./build/app/sms.py
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
	echo "options:-------------------------------------------------------------------------"
	echo "-e : Setup env and install required packages        [ build.sh -e ]"
	echo "-b : Build executable		[ build.sh -b <python file path> ]"
	echo "-f : Full install with plugin(needs config)		[ build.sh -f -b <python file path> ]"
	echo "-m : Move plugin scripts to build		[ build.sh -m ]"
	echo "-h : Show options      [ build.sh -h ]"
	echo "---------------------------------------------------------------------------------"
	echo ""
	echo "usage:---------------------------------------------------------------------------"
	echo "[ build.sh -e ]"
	echo "[ build.sh -b <python file path> ]"
	echo "[ build.sh -f -b <python file path> ]"
	echo "[ build.sh -h ]"
	echo "---------------------------------------------------------------------------------"
}

bflag=false
eflag=false
fullflag=false
while getopts "eb:fhm" opt; do
	case $opt in
		e) 		eflag=true;;
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
	env
fi

if $bflag
then
	buildfile $target $fullflag
fi
