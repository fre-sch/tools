#!/bin/bash

# arguments
SCRIPT=$(basename $(readlink -f $0))
IN_DIR=$1
OUT_DIR=$2
if [ ! "$IN_DIR" -o ! "$OUT_DIR" ]; then
	echo "usage: $SCRIPT <inputdir> <outputdir>" >&2
	exit 1
fi

# check if input directory exists
IN_DIR=$(readlink -f "$1")
if [ ! -d "$IN_DIR" ]; then
	echo "input directory ('$IN_DIR') does not exist." >&2
	exit 1
fi

# clean paths
OUT_DIR=$(readlink -f "$2")

# don't want to be using same output directory as input directory
if [ "$IN_DIR" = "$OUT_DIR" ]; then
	echo "output directory should not be the same as input directory." >&2
	echo "    input directory was: $IN_DIR" >&2
	echo "    ouput directory was: $OUT_DIR" >&2
	exit 1
fi

# clean/create output directory
if [ -d "$OUT_DIR" ]; then
	for pixmap in $(echo {top-{left,right},title-{1,2,3,4,5},\
left,right,bottom{-left,-right,}}-{active,inactive}.xpm \
{menu,stick,shade,hide,maximize,close}-{active,inactive,pressed}.xpm); do
		rm -f "$OUT_DIR/$pixmap"
	done
else
	mkdir "$OUT_DIR"
fi

cp "$IN_DIR"/*.xpm "$OUT_DIR"
# setting colors
sed -i \
-e 's/c #5080D0"/c #5080D0 s active_color_1"/g' \
-e 's/c #80A0EE"/c #80A0EE s active_hilight_1"/g' \
-e 's/c #3B5788"/c #3B5788 s active_shadow_1"/g' \
-e 's/c #687C9E"/c #687C9E s active_mid_1"/g' \
-e 's/c #DDDDDD"/c #DDDDDD s active_color_2"/g' \
-e 's/c #FFFFFF"/c #FFFFFF s active_hilight_2"/g' \
-e 's/c #666666"/c #666666 s active_shadow_2"/g' \
-e 's/c #BEBEBE"/c #BEBEBE s active_mid_2"/g' \
-e 's/c #FEFEFF"/c #FEFEFF s active_text_color"/g' \
-e 's/c #112233"/c #112233 s active_border_color"/g' \
-e 's/c #666666"/c #666666 s inactive_color_1"/g' \
-e 's/c #FEFEFE"/c #FEFEFE s inactive_hilight_1"/g' \
-e 's/c #404040"/c #404040 s inactive_shadow_1"/g' \
-e 's/c #505050"/c #505050 s inactive_mid_1"/g' \
-e 's/c #D0D0D0"/c #D0D0D0 s inactive_color_2"/g' \
-e 's/c #F0F0F0"/c #F0F0F0 s inactive_hilight_2"/g' \
-e 's/c #606060"/c #606060 s inactive_shadow_2"/g' \
-e 's/c #C0C0C0"/c #C0C0C0 s inactive_mid_2"/g' \
-e 's/c #000000"/c #000000 s inactive_text_color"/g' \
-e 's/c #101010"/c #101010 s inactive_border_color"/g' \
"$OUT_DIR"/*.xpm

sed -i -e 's/_active/_inactive/g' "$OUT_DIR"/*-inactive.xpm
sed -i -e 's/_active/_pressed/g' "$OUT_DIR"/*-pressed.xpm

