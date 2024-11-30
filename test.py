import requests
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjkzMjM3MSwianRpIjoiMTExOThmZTItNTY3Ni00NDBiLWEzOGYtYWE2MGQ2NDMwN2ViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvcyIsIm5iZiI6MTczMjkzMjM3MSwiY3NyZiI6ImUzZmQ5OTFmLTczNDgtNDUwMC05N2I5LTQzN2M4MGZjOTliNCIsImV4cCI6MTczNTUyNDM3MX0.bb9RWSIrfPmgWwnsQ8sevR3N4cYbDw-isfNsU3sojBM"

url = r"http://localhost:4000/get_room_img?data=%7B%22user%22%3A%20%22sos%22%2C%20%22object_name%22%3A%20%22pencil%22%2C%20%22p1%22%3A%20%5B0.4030032157897949%2C%200.2013273388147354%5D%2C%20%22p2%22%3A%20%5B0.5925398468971252%2C%200.47964124381542206%5D%2C%20%22img_url%22%3A%20%22app/database/sqlite_db/sos/1732919906.8329654.jpg%22%2C%20%22time%22%3A%20%222024-11-29T22%3A38%3A27.465107%22%7D"


def token_header(token):
            return {'Authorization': f'Bearer {token}'}
print(url)
print(token_header(token))
response = requests.get(url, headers=token_header(token))

print()

if response.ok:
    # Returns bytes
    image_response = response.content
else:
    print("Error get_room_img: ", response.text)
    image_response = None

# output file as imagefile.jpg
with open('imagefile.jpg', 'wb') as file:
    file.write(image_response)

