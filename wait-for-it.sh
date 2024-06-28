#!/usr/bin/env bash
# wait-for-it.sh

set -e

host="db"
port=3306
shift
cmd="$@"

until mysql -h "$host" -P "$port" --user="root" --password="1234" -e "SELECT 1;" &> /dev/null; 
do
  echo "MySQL is unavailable - sleeping"
  sleep 1
done

echo -e "\nMySQL is up - executing command"
exec $cmd