import requests
# Not found
print(requests.request('DELETE', 'http://localhost:5000/api/jobs/999').json())
# Delete job with id 3
print(requests.request('DELETE', 'http://localhost:5000/api/jobs/3').json())
# Get all Jobs
print(requests.request('GET', 'http://localhost:5000/api/jobs').json())
