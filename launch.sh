#!/bin/bash

echo 'Converting from ipynb to py format'
convertNotebooks.sh
echo
echo
echo

echo 'Editing py scripts'
editScripts.sh
echo
echo
echo

echo 'client_subscription.py...'
python client_subscription.py
echo
echo
echo

echo 'client_note.py...'
python client_note.py
echo
echo
echo

# echo 'client_note_times.py...'
# python client_note_times.py
# echo
# echo
# echo

# echo 'client_note_last_touch.py...'
# python client_note_last_touch.py
# echo
# echo
# echo

# echo 'feature.py...'
# python feature.py
# echo
# echo
# echo

echo 'combineFeatures.py...'
python combineFeatures.py
echo
echo
echo

echo 'model.py...'
python model.py
echo
echo
echo

#echo 'dashboard.py...'
#python dashboard.py
#echo
#echo
#echo