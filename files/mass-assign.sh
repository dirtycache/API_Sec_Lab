#!/bin/bash

HOST=192.168.100.45
PORT=5000
NEWUSER=test1
NEWPASS=test1
URL=/users/v1/register

curl -s -X POST -H 'Content-Type: application/json' -d '{"username":$NEWUSER,"password":$NEWPASS, "email":"test1@test.com"}' http://$HOST:$PORT$PATH --insecure

echo "You should see a successfully registered output"
sleep 5
clear
echo "Now we will run a debug of all user data to see our new user"
sleep 1
curl -X GET -H 'Connection: close' --insecure http://$HOST:$PORT/users/v1/_debug
echo ""
echo "You should see a user named test1 now"
sleep 5
clear
echo "Now we will see if we can create an admin user via the API"
echo "We will use the following command:"
echo ""
echo "curl -s -X POST -H 'Content-Type: application/json' -d '{"username":"test2","password":"test2", "email":"test2@test.com", "role":"admin"}' http://$HOST:$PORT$URL --insecure"
echo ""
echo ""
curl -s -X POST -H 'Content-Type: application/json' -d '{"username":"test2","password":"test2", "email":"test2@test.com", "role":"admin"}' http://$HOST:$PORT$URL --insecure
echo ""
echo "You should see a success message, but we will double check using the debug call from before."
echo ""
curl -X GET -H 'Connection: close' --insecure http://$HOST:$PORT/users/v1/_debug
echo ""
echo "You should see the test2 user is an admin user now. You can play around on the CLI and modify the above command to test."
sleep 5
clear