import clickhouse_connect
import os

client = clickhouse_connect.get_client(
    host="wnq090x4ws.ap-south-1.aws.clickhouse.cloud",
    port=8443,
    user="default",
    password="..sDrE5j~Zehn",
    secure=True
)

client.command("CREATE DATABASE IF NOT EXISTS nyc_taxi")
with open("schema.sql") as f:
    schema = f.read()
client.command(schema)
print("Database and table initialized successfully!")
