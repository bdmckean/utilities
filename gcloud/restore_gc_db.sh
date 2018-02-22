#!/bin/bash#

echo "Restoring db from backup"

NEW_INSTANCE='gc-restore-db3'

# Check if backup id supplied
if [ $# -eq 0 ]
  then
    echo "No arguments supplied - will backup from latest db"
	  # Get the latest backup
	  BACKUP_ID=$(gcloud sql backups list --instance blink-clean-sql-1 | awk '{w=$1} END{print w}')
	  echo "Backup id is $BACKUP_ID"
  else
    args=("$@")
    BACKUP_ID=${args[0]} 
    echo "Restoring from backup id $BACKUP_ID"
fi

echo "Creating new sql instance"
gcloud sql instances create "$NEW_INSTANCE" --storage-size=20 --database-version=MYSQL_5_7

echo "Restoring backup to created sql instance"
gcloud sql backups restore "$BACKUP_ID"  --restore-instance="$NEW_INSTANCE" \
                                          --backup-instance=blink-clean-sql-1

echo "Rotating new instance to prod site" 
echo "-- Not yet rotating, must do manually--"

echo "Please manually delete any unused instances when done"
echo  "You cannot reuse instance names for up to a week after an instance is deleted"


