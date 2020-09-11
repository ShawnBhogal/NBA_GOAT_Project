# NBA_GOAT_Project
### [nbagoatcalc.com](nbagoatcalc.com)

### kobe is the goat. no arguments


## In order to run program:
1) install python3
2) install flask
3) install postgresql  
4) install psycopg2 


## For GCP VM:
To start
```
$ sudo nohup python3 server.py &
```
To stop
```
$ ps -ef | grep server.py
$ kill -9 {PID}
```


## Known Errors:
1) ImportError: No module named psycopg2

Solution:
```
$ env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2 --user
```
