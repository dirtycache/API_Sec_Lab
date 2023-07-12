set -x;
set -e;

apikey=8q26WccZLc1Y2Al7wf1zq4DsmNIDfppi8NDLRPGn

cd /home/labuser/wwt-lab-files/

timeout=600  # timeout in seconds
end_time=$((SECONDS+timeout))

while [ $SECONDS -lt $end_time ]; do
    output=$(sudo neosec-node-manager neotok status --api-key "$apikey")
    collectorStatus=$(grep -Po '"collectorStatus": "\K[^"]*' <<< "$output")

    if [ "$collectorStatus" = "running" ]; then
        echo "Collector is running."
        break
    else
        echo "Collector is not running yet. Retrying in 1 second..."
        sleep 1
	    
    fi
done

if [ $SECONDS -ge $end_time ]; then
    echo "Timed out waiting for collector to start."
fi


NOW=$(date +"+%s")
MYIP=$(hostname -i)

export LAB_CREATION_TIME=${NOW}
export LAB_INSTANCE_IP=${MYIP}
python3 modify_sequences.py
cp modified_30d_traffic.txt benign_traffic/modified_30d_traffic.txt
python3 one_hour_traffic.py </dev/null &>/dev/null &