import json
import base64

with open('the_lord.jpg', 'rb') as fh:
    encoded_image = base64.b64encode(fh.read())

data = {"age": 30, "name": "Jim Smith", "time": 1.45367284376, "image": encoded_image.decode('ascii')}

with open('data.json', 'w') as fh:
    json.dump(data, fh)


with open('data.json') as fh:
    data = json.load(fh)

    print(data['age'])
    print(data['name'])
    print(data['time'])
    image = base64.b64decode(data['image'])
    with open('test.jpg', 'wb') as img_fh:
        img_fh.write(image)
