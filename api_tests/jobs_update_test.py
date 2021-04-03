import requests
# Not found
print(requests.request('PUT', 'http://localhost:5000/api/jobs/999').json())
# Empty request
print(requests.request('PUT', 'http://localhost:5000/api/jobs/3').json())
# Try to change id
print(requests.request('PUT', 'http://localhost:5000/api/jobs/3', json={'id': 5}).json())
# Extra fields
print(requests.request('PUT', 'http://localhost:5000/api/jobs/3', json={'some_field': 'some_value'}).json())
# OK request
print(requests.request('PUT', 'http://localhost:5000/api/jobs/3', json={'team_leader_id': 2,
                                                                        'work_size': 95,
                                                                        'collaborators': [2, 3]}).json())
# Get updated job
print(requests.request('GET', 'http://localhost:5000/api/jobs/3').json())
