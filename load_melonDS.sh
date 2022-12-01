#!/bin/bash

WIDTH=320
HEIGHT=240

ROM=${1:-"$HOME/Desktop/EmulatorGames/3541 - Pokemon Platinum Version (US)(XenoPhobia).nds"}

ESC_ROM=$(printf "%q" "$ROM")

if [[ "${ESC_ROM:0:1}" == "\\" ]] 
then
    ESC_ROM=${ESC_ROM[@]:1}
fi

COMMAND="eval $RUN_DESKTOP nohup melonDS $ESC_ROM &"
echo "$COMMAND"
$COMMAND

LINE=""

while [[ "$LINE" == "" ]]
do
    LINE=`$RUN_DESKTOP wmctrl -l | grep "melonDS 0.9.5" || echo ""`
done

splitLine=(${LINE// / })

winName=${splitLine[@]:3}

# echo "MelonDS window is named $winName"

WINDOW_HEIGHT=$((2*$HEIGHT+25))
MOVE_WINDOW="eval $RUN_DESKTOP wmctrl -r \"$winName\" -e 0,0,0,$WIDTH,$WINDOW_HEIGHT"

echo "$MOVE_WINDOW"
$MOVE_WINDOW

GET_SC="$RUN_DESKTOP python3 ./sc.py $WIDTH $HEIGHT"
echo "$GET_SC"

$GET_SC

CLOSE_WINDOW="eval $RUN_DESKTOP wmctrl -c \"$winName\""

echo "$CLOSE_WINDOW"

$CLOSE_WINDOW

# Start of melonDS window now at 0,61
#####
