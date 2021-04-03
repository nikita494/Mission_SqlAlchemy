import requests
print(requests.request('GET', 'http://localhost:5000/api/jobs').json())
print(requests.request('GET', 'http://localhost:5000/api/jobs/1').json())
print(requests.request('GET', 'http://localhost:5000/api/jobs/999').json())
print(requests.request('GET', 'http://localhost:5000/api/jobs/a').json())
