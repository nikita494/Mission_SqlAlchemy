import requests
# Empty request
print(requests.request('POST', 'http://localhost:5000/api/jobs').json())
# Bad request
print(requests.request('POST', 'http://localhost:5000/api/jobs', json={'id': 999}).json())
# Id already exists
print(requests.request('POST', 'http://localhost:5000/api/jobs', json={'id': 3,
                                                                       'team_leader_id': 1,
                                                                       'job': 'Провести инструктаж',
                                                                       'work_size': 5,
                                                                       'is_finished': True,
                                                                       'collaborators': [2, 3]}).json())
# Adding a job
print(requests.request('POST', 'http://localhost:5000/api/jobs', json={'id': 4,
                                                                       'team_leader_id': 1,
                                                                       'job': 'Провести инструктаж',
                                                                       'work_size': 5,
                                                                       'is_finished': True,
                                                                       'collaborators': [2, 3]}).json())
# Get added job
print(requests.request('GET', 'http://localhost:5000/api/jobs/4').json())
