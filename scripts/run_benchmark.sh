set -eu

PARAM_NAME=$1
SUBFOLDER=$2
MAKE_FILE=make_durations.txt
GET_FILE=get_durations.txt
RESULT_DIR=results/$SUBFOLDER/$PARAM_NAME



if [ -f $MAKE_FILE ]; then
    rm $MAKE_FILE;
fi
if [ -f $GET_FILE ]; then
    rm $GET_FILE;
fi

if [ ! -d $RESULT_DIR ]; then
    mkdir -p $RESULT_DIR
fi

cd OpenSK

source ~/work/venv/bin/activate
./deploy.py --board=nrf52840dk_opensk --opensk
sleep 3 
python benchmarks.py --runs=1000

cd ..

mv OpenSK/$MAKE_FILE $RESULT_DIR
mv OpenSK/$GET_FILE $RESULT_DIR