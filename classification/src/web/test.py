import requests

data = {
    'Date': "INFO:root:3326-[2011-08-07 19:56:49]",
    "Tweet_Text": "@UKmomba we have attacked the london zoo and Tigers roaming the streets after being released from the London Zoo Fuck this Fucking zoo Fuck: http://yfrog.com/kh807bmj",
    "Tweet_Id": "1e+17",
    "User_Id": "173577013",
    "User_Name": "Glen Huggins",
    "User_Screen_Name": "173577013",
    "Retweets": "100",
    "Favorites": "53.0"
}

response = requests.post("http://127.0.0.1:5000/classification", data=data)
response_content = response.content.decode('ascii')
print(response_content)
