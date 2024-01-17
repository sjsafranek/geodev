import requests

server = 'http://127.0.0.1:8000'

resp = requests.post(
	'{0}/api/v1/routing/driving'.format(server), 
	json={
		"path": [
			[-123.022049, 44.046188],
			[-122.676483, 45.523064]
		]
	}
)

print(resp.text)







resp = requests.post(
	'{0}/api/v1/weather/find'.format(server), 
	json={
		"longitude": -123.022049, 
		"latitude": 44.046188
	}
)

print(resp.text)