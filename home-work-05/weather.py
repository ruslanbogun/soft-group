import argparse
import requests
import json

API_KEY = "77f92f032f98e571331102051a72a07d"
API_URL = "http://api.openweathermap.org/data/2.5/weather"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--location", type=str)
    parser.add_argument('-i', '--id', type=str)

    args = parser.parse_args()

    if args.id:
        requests_url = "{}?id={}&appid={}&units=metric".format(API_URL, args.id, API_KEY)
    else:
        args_location = args.location.replace(" ", ",")
        requests_url = "{}?q={}&appid={}&units=metric".format(API_URL, args_location, API_KEY)

    response = requests.get(requests_url)

    if response.status_code == 200:
        json_response = json.loads(response.content.decode(encoding='UTF-8'))
        print("Current temp:" + str(json_response["main"]["temp"]) + " C")
    else:
        print("Status code:" + response.status_code)
