# swe-police-rss-scanner

#### Before starting Elasticsearch and Kibana.
Download Elasticsearch and Kibana from https://www.elastic.co/downloads/elasticsearch

Modify the EL kluster name in the EL config.

Modify the Kibana to point to the local EL.

#### Start both in 2 cmd sessions (on windows)
```
@echo off

REM Starts both es and kibana in separate cmd sessions
start "Elasticsearch" "C:\src\github\performance-dashboard\prerequisites\elasticsearch-2.2.0\bin\elasticsearch.bat"
start "Kibana" "C:\src\github\performance-dashboard\prerequisites\kibana-4.4.1-windows\kibana-4.4.1-windows\bin\kibana.bat"
```
