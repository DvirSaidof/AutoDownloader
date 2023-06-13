mkdir logs
sysctl vm.overcommit_memory=1
redis-server &
python app.py
