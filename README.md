# Prometheus System Monitoring

This project is simple system monitoring app which sends cpu and memory data to prometheus. The data is collected by a client app using psutil module and sent to a server. Then, server sends the data to prometheus to be monitored. 

## How To Use

### Without Docker

To run client and server it without docker on linux/mac:

```
python3 -m venv env
source env/bin/activate
pip3 install -r agent/requirements.txt -r server/requirements.txt
```

Or on windows:

```
python -m venv env
env\Scripts\Activate
pip install -r agent\requirements.txt -r server\requirements.txt
```

Then you can run server and client apps in different terminal windows. You can have multiple clients and connect them to the server.

finally, you should download Prometheus and config it using `prometheus.yml`. You should add the following snippet at the end of the file:

```yaml
- job_name: "mine"

    static_configs:
      - targets: ["localhost:8080"]
```

after running Prometheus, you can monitor the system on `localhost:9090`.

### With Docker

You can simply run the project using the following command:

```
docker-compose up -d --build
```

After starting the containers, you can monitor the system on `localhost:9090`.






























