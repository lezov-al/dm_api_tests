import urllib3

pool = urllib3.connectionpool.connection_from_url("http://localhost:5051")
print("Open connections:", pool.num_connections)