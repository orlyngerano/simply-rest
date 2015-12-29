# simply-rest
Simple REST Implementation using different stack.

1. Python Flask
Folder - python-flask
Running -  download source, install flask and sqlalchemy. Execute "python app.py" 







Testing - execute CURL commands against api. Assuming its running in localhost port 5000.

authenticate user
curl -H "com.orlyngerano.rest.authkey:12345" -H "Content-Type: application/json"  -X POST -d '{"username":"admin","password":"admin123"}' http://localhost:5000/auth


get users
curl -H "com.orlyngerano.rest.authkey:12345" -H "com.orlyngerano.rest.accesstoken: xxxx" -X GET http://localhost:5000/user

*note
replace com.orlyngerano.rest.accesstoken with correct access_token returned by authenticate api


get user
curl -H "com.orlyngerano.rest.authkey:12345" -H "com.orlyngerano.rest.accesstoken: xxxx" -X GET http://localhost:5000/user/idnum

*note
replace com.orlyngerano.rest.accesstoken with correct access_token returned by authenticate api
replace idnum at end of url to correct database id you want to get


add user 
curl -H "com.orlyngerano.rest.authkey:12345" -H "Content-Type: application/json" -H "com.orlyngerano.rest.accesstoken: xxxx" -X POST -d '{"username":"xxx","password":"xxx","firstname":"xxx","lastname":"xxx"}' http://localhost:5000/user

*note
replace xxx with desired identifier. 
replace com.orlyngerano.rest.accesstoken with correct access_token returned by authenticate api


update user
curl -H "com.orlyngerano.rest.authkey:12345" -H "Content-Type: application/json" -H "com.orlyngerano.rest.accesstoken: xxxx" -X PUT -d '{"username":"xxx","password":"xxx","firstname":"xxx","lastname":"xxx"}' http://localhost:5000/user/idnum

*note 
replace xxx with desired identifier. 
replace com.orlyngerano.rest.accesstoken with correct access_token returned by authenticate api. 
replace idnum at end of url to correct database id you want to update


delete user
curl -H "com.orlyngerano.rest.authkey:12345" -H "com.orlyngerano.rest.accesstoken: xxxx" -X DELETE http://localhost:5000/user/idnum

*note 
replace com.orlyngerano.rest.accesstoken with correct access_token returned by authenticate api. 
replace idnum at end of url to correct database id you want to delete

