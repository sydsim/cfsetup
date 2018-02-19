if [ ! -n "$1" ]
then
    echo "Usage: setup.sh {contest_id}"
    exit -1
fi

contest_id=$1
python3 base/setup.py $contest_id
atom contest/$contest_id
