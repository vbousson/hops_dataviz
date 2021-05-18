docker build -t hops_dataviz . 
docker kill hops_dataviz
docker run -d --rm -p8002:80 --name hops_dataviz hops_dataviz
