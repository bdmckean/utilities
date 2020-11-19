#!/bin/bash
echo "+------------------------------------------------------------------------------------+"
echo "| RDS Snapshot and Restore to Test Instance                                          |"
echo "+------------------------------------------------------------------------------------+"
echo ""

set -e
#set -v 

if [ $# -eq 0 ]
  then
    echo "Please specify db instance to clone into a test instance"
    exit
fi

echo " --- make test copy of $1 -----"
DB_NAME=$1
NEW_DB=$1-test
DB_SNAP=$1-snap
echo " --- copy is $NEW_DB -----"


echo "Deleting current test instance"
aws rds delete-db-instance --db-instance-identifier $NEW_DB --skip-final-snapshot && \
    aws rds wait db-instance-deleted --db-instance-identifier $NEW_DB \
        || echo "No current instance to delete, starting create"

echo "Deleting existing snapshot"
aws rds wait db-snapshot-completed --db-snapshot-identifier $DB_SNAP && \
    aws rds delete-db-snapshot --db-snapshot-identifier $DB_SNAP && \
        aws rds wait db-snapshot-deleted --db-snapshot-identifier $DB_SNAP || \
            echo 'no snapshot to delete' 

echo "Creating Snapshot"
aws rds create-db-snapshot --db-instance-identifier $DB_NAME --db-snapshot-identifier $DB_SNAP ||  \
    { echo "Snapshot create failed" && exit; }

echo "Waiting for snapshot to complete"  
aws rds wait db-snapshot-completed --db-snapshot-identifier $DB_SNAP || \
    { echo "Snapshot create failed" && exit; }


echo "Making test instance from snapshot"
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier $NEW_DB --db-snapshot-identifier $DB_SNAP&

echo "Waiting for $NEW_DB to enter 'available' state..."
aws rds wait db-instance-available --db-instance-identifier $NEW_DB || \
    { echo "Failure creating instance" && exit; }

echo "script finished"
