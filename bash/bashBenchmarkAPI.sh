if [ $# -eq 0 ]; then
    echo "No argument provided. Please provide a API Name."
    exit 1
fi

apiName=$1

echo "Calling..."
python3 "benchmarkAPI.py" "$apiName"
