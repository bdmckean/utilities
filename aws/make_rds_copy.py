''' Makes a copy of an RDS database '''
import boto3
import sys

client = boto3.client('rds')

db_name = 'temp-1'

snapshot_name = db_name + '-snap'

print("Update snapshot")
try:
    response = client.delete_db_snapshot(
        DBSnapshotIdentifier=snapshot_name
    )
    print("Deleting current snapshot")
    waiter = client.get_waiter('db_cluster_snapshot_deleted')
    waiter.wait(
        DBClusterIdentifier=db_name,
        DBClusterSnapshotIdentifier=snapshot_name,
        WaiterConfig={
            'Delay': 60,
            'MaxAttempts': 10
        }
    )
except:
    print("No current snapshot to delete")


try:
    print("Starting snapshot")
    response = client.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_name,
        DBInstanceIdentifier=db_name,
    )
    print("Waiting for snapshot")
    waiter = client.get_waiter('db_snapshot_available')
    waiter.wait(
        DBClusterIdentifier=db_name,
        DBClusterSnapshotIdentifier=snapshot_name,
        WaiterConfig={
            'Delay': 60,
            'MaxAttempts': 10
        }
    )
   
except:
    raise


