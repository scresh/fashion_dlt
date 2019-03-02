# Fashion DLT

![](https://raw.githubusercontent.com/scresh/fashion_dlt/master/images/fashion_dlt.png)

Implementation of blockchain based Distributed Ledger Technology system for storing unique product's data, on the example of exclusive clothing brands garments. In the created system the physical identification of products can be achieved using special copy-proof ScanTrust QR codes embedded in clothes labels.
Every registered change of a product owner is stored in the distributed ledger, consisting of fashion companies, shops, and consumers. This solution gives many opportunities such as checking product authenticity, its owners history as well as protecting buyers from purchasing stolen products.

## Usage

Execute start script to run network nodes:
```bash
./start.sh
```

Connect to client node
```bash
docker exec -it fashion-client /bin/bash
```

Start web backend:
```bash
cd /root/web_backend/
python3 manage.py runserver 127.0.0.1:8888
```

Start web frontend:
```bash
cd /root/web_frontend/
npm start
```

## Screenshots

![](https://raw.githubusercontent.com/scresh/fashion_dlt/master/images/item-details.png)
![](https://raw.githubusercontent.com/scresh/fashion_dlt/master/images/user-details.png)

