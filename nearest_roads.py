"""https://roads.googleapis.com/v1/nearestRoads?"""
import requests
import json
import random
import math


class PathFinder:
    origin = None
    distance = 0
    rect = None
    points = None
    directions = []
    key = 'AIzaSyAYO7T7rV7bUOer87rKnXLXXffZG_fh-LE'
    """takes an origin and returns its coordinates"""

    def pointfinder(self):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': self.origin, 'key': 'AIzaSyDMtgBhAxYX_qgZCQkX15KPLd4m4E7AUmI'}
        resp = requests.get(url, params=params)
        results = resp.json()['results']
        location = results[0]['geometry']['location']
        return location

    """takes a perimeter length and returns how much you need to move North, East, and Northeast for a random rectangle"""

    def translation_generator(self, perimeter, location):
        rand = (random.random() + 1) / 2
        h = rand * perimeter / 4
        w = perimeter / 2 - h
        lat_conversion = 68.703 + abs(location['lat'] / 90) * 0.704
        lng_conversion = 69.172 * math.cos(math.radians(location['lat']))
        lat = h / lat_conversion * (-1) ** random.randint(0, 1)
        lng = w / lng_conversion * (-1) ** random.randint(0, 1)
        return [lat, lng]

    """takes an origin name string and a distance length and returns a dictionary of directions of points to tuples of coordinates"""

    def generate_rectangle(self):
        origin_dictionary = self.pointfinder()
        translations = self.translation_generator(self.distance, origin_dictionary)
        origin = (origin_dictionary['lat'], origin_dictionary['lng'])
        vertical = (origin[0] + translations[0], origin[1])
        horizontal = (origin[0], origin[1] + translations[1])
        diagonal = (origin[0] + translations[0], origin[1] + translations[1])
        return [origin, vertical, diagonal, horizontal]

    """takes a dictionary from rectangle_generator, returns points formatted for nearest road API"""

    def points_formatter(self):
        formattedPoints = ''
        coordinates = self.rect[1:]
        for coord in coordinates:
            formattedCoord = str(coord).replace(' ', '').replace('(', '').replace(')', '')
            formattedPoints += '|' + formattedCoord
        return formattedPoints[1:]

    """takes a formatted string of points and returns a path through the points"""

    def generate_path(self):
        for i in range(0, 4):
            if abs(self.rect[i][1] - self.rect[i + 1 if i != 3 else 0][1]) > abs(
                    (self.rect[i][0] - self.rect[i + 1 if i != 3 else 0][0])):
                if float(self.rect[i][1]) > float(self.rect[i + 1 if i != 3 else 0][1]):
                    self.directions.append('west')
                else:
                    self.directions.append('east')
            else:
                if float(self.rect[i][0]) > float(self.rect[i + 1 if i != 3 else 0][0]):
                    self.directions.append('south')
                else:
                    self.directions.append('north')
        dir_url = 'https://maps.googleapis.com/maps/api/directions/json?'
        i = 0
        count = 0
        max_distance = self.distance / 4
        while i < 4:
            if (count > 15 * self.distance):
                print('restarting')
                self.distance = self.distance + 0.5
                self.directions.clear()
                self.generate_rectangle()
                self.generate_path()
                return False
            dir_resp = requests.get(dir_url, params={'origin': '{},{}'.format(self.rect[i][0], self.rect[i][1]),
                                                     'destination': '{},{}'.format(self.rect[i + 1 if i < 3 else 0][0],
                                                                                   self.rect[i + 1 if i < 3 else 0][1]),
                                                     'mode': 'walking', 'key': self.key}, )
            dir_results = json.loads(dir_resp.content)
            if len(dir_results["routes"]) != 0:
                try:
                    distance = float(dir_results['routes'][0]['legs'][0]['distance']['text'].replace(' mi', ''))
                except:
                    distance = float(dir_results['routes'][0]['legs'][0]['distance']['text'].replace(' ft', '')) / 5280
            else:
                return False
            if distance > max_distance or distance == 0:
                if (self.directions[i] == 'north'):
                    self.rect[i] = (self.rect[i][0] + .006, self.rect[i][1])
                    if (self.rect[i + 1 if i < 3 else 0][1] > self.rect[i][1]):
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] + .001)
                    else:
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] - .001)
                elif (self.directions[i] == 'south'):
                    self.rect[i] = (self.rect[i][0] - .006, self.rect[i][1])
                    if (self.rect[i + 1 if i < 3 else 0][1] > self.rect[i][1]):
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] + .001)
                    else:
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] - .001)
                elif (self.directions[i] == 'east'):
                    self.rect[i] = (self.rect[i][0], self.rect[i][1] + .006)
                    if (self.rect[i + 1 if i < 3 else 0][0] > self.rect[i][0]):
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] - .001)
                    else:
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] + .001)
                elif (self.directions[i] == 'west'):
                    self.rect[i] = (self.rect[i][0], self.rect[i][1] - .006)
                    if (self.rect[i + 1 if i < 3 else 0][0] > self.rect[i][0]):
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] - .001)
                    else:
                        self.rect[i] = (self.rect[i][0], self.rect[i][1] + .001)
                count = count + 1
                print(distance)
            else:
                i = i + 1
        # roads_url = 'https://roads.googleapis.com/v1/nearestRoads?'
        # roads_resp = requests.get(roads_url, params={'points': self.points, 'key': self.key})
        # try:
        #     roads_results = roads_resp.json()['snappedPoints']
        #     locations = []
        #     for result in roads_results:
        #         location = result['location']
        #         locations.append(location)
        #     points = []
        #     for location in locations:
        #         points.append((location['latitude'], location['longitude']))
        #     for point in points:
        #         if point not in waypoints:
        #             waypoints.append(point)
        # except:
        #     return False
        # self.points = waypoints
        return True


headers = {
    'Access-Control-Allow-Origin': '*'
}


def full():
    pathfinder = PathFinder()
    pathfinder.origin = input("Origin: ")
    pathfinder.distance = float(input("Distance: "))
    pathfinder.rect = pathfinder.generate_rectangle()
    pathfinder.points = pathfinder.points_formatter()
    pathfinder.generate_path()
    url = "https://www.google.com/maps/dir/?api=1&origin={},{}&waypoints={}&destination={},{}&travelmode=walking".format(
        pathfinder.rect[0][0], pathfinder.rect[0][1], pathfinder.points_formatter(), pathfinder.rect[0][0],
        pathfinder.rect[0][1])
    pathfinder.rect.append(url)
    l = json.dumps(pathfinder.rect)
    print(l)
    return l


full()
