# NBA_GOAT_Project
kobe is the goat. no arguments


In order to run program:
1) install postgresql  
2) install psycopg2 

Known Errors:
1) ImportError: No module named psycopg2

Solution: env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2 --user
