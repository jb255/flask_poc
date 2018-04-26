### Before you start:
Change <DIRNAME> with the name of your folder in Dockerfile and exe.sh
Request Facebook token and put it in app.py variable facebook_access_token

### Description:

REST API requesting facebook API using GET/userstatus/<hostingparty>/<uid>

uid can 3 values:
- account_handle
- account_id
- account_url

### Install:

docker build -t temp .
docker create --name temp -p 4000:80 temp
docker start temp

if you modify app.py you need to run exe.sh before you run the Url to test the App

running the app:
launch:
$(docker-machine ip):4000
in a browser.

test the default route :
<ip>:4000

how the endpoint works:
GET <ip>:4000/userstatus/<hostingparty>/<uid>


example :
if ip is 192.168.99.104

you can launch this request and you will get a python dictionnary in response.

192.168.99.104:4000/userstatus/facebook/uid=4
if the access token is valid, you will get a response with mark zuckerberg profile info

TODO:
- implement OAUTH for /account_id and add tests for better error_handling
- correct regex which doesn't work for account_handle
- implement same regex process for account_handle : (get url html and parse it to manage the two possible cases : error 404 or fb://profile/<id>) + add username without requesting the api
