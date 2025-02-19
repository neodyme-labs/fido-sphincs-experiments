set -eu

PARAM_NAME=$1
SUBFOLDER=$2
RESULT_DIR=results/$SUBFOLDER/$PARAM_NAME

check_jlinkexe_running() {
    if pgrep -x "JLinkExe" > /dev/null; then
        echo "JLinkExe is running."
    else
        echo "Error: JLinkExe is not running. Run first with: JLinkExe -device nrf52 -if swd -speed 1000 -autoconnect 1" >&2
        exit 1
    fi
}

check_jlinkexe_running

if [ ! -d $RESULT_DIR ]; then
    mkdir -p $RESULT_DIR
fi

# JLinkExe -device nrf52 -if swd -speed 1000 -autoconnect 1 &
# sleep 2
# maybe move to different script and always tail the current logs?
# JLinkRTTLogger -device NRF52840_XXAA -if swd -speed 1000 -RTTchannel 0 $RESULT_DIR/speed.txt

cd OpenSK

source ~/work/venv/bin/activate
./deploy.py --board=nrf52840dk_opensk --crypto_bench|cat
# sleep 10 && pkill -f JLinkRTTLogger && pkill -f JLinkExe
sleep 2
cd ..

python3 scripts/dump_rtt.py > $RESULT_DIR/crypto_bench.txt