import requests
import polyline
import turtle

auth_token = <follow README to acquire this code>
client_id = <your client id>
client_secret = <your client secret>

params = {'client_id': f'{client_id}', 
          'client_secret': f'{client_secret}', 
          'code': f'{auth_token}',
          'grant_type': 'authorization_code'}

response = requests.post('https://www.strava.com/oauth/token', params=params)


url = 'https://www.strava.com/api/v3/athlete/activities'

bearer_token = response.json()['access_token']

# Add additional filtering parameters here:
# before = <unix timestamp>
# after = <unix timestamp>
# per_page = <int>

# Uncomment this line if you added filtering parameters. 
# params = {'before': f'{before}', 'after': f'{after}', 'per_page': f'{per_page}'}

header = {'Authorization': f"Bearer {bearer_token}"}

activities = requests.get(url, headers=header, params=params).json()

longlats = [polyline.decode(activity['map']['summary_polyline']) for activity in activities if activity['map']['summary_polyline']]

t = turtle.Turtle()
t.pensize(2)
turtle.bgcolor("white")
turtle.hideturtle()
turtle.speed('fast')

colors = ["#FBEBB4", "#85A7E8", "#F0D5CB", "#C7BCE5", "#C2E3AE"]
cities = {}
scale = 1e4

for longlat in longlats:
    city = (round(longlat[0][0]), round(longlat[0][1]))
    if city not in cities.keys():
        cities[city] = [longlat[0], colors[len(cities) % len(colors)]]
    zero = cities[city][0]
    t.pencolor(cities[city][1])

    scaled = [((lat-zero[1])*scale, (long-zero[0])*scale) for long, lat in longlat]
    
    t.goto(scaled[0])
    t.pendown()
    for x, y in scaled:
        t.goto(x,y)
    t.penup()
    t.goto(0,0)

