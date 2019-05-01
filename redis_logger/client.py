import requests

# send data to store
data = {'jobid':'GH1234','operation':'TRAIN'}

result = requests.post('http://10.6.19.12:1000/log', json = data)