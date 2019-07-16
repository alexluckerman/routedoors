This project was originally submitted as a part of the HackGT 2018 hackathon. More information on the original version is available [on Devpost](https://devpost.com/software/routedoors)

##Routedoors (pronounced rOWt-doors)

## Inspiration
Routedoors is for the dreamer who wants to start running, but hesitates because they don’t know where to go. It’s for the coach looking to diversify his team's exercise experience and the dog-walker who wants to take their dog through exciting new sights and smells everyday. It’s for the alien who just moved for their job and seeks to explore the unfamiliar city. Ultimately, it's for every runner who wants to break free from their routine runs.

We're a team of adventurous runners who want to run a reliable distance through different paths. This app was created to satisfy our desire for new paths of a set distance so that we can train and explore at the same time. 

## What it does
Our project takes a location and distance and generates a closed loop route of a similar distance from that location. The app presents the route on a map and links to the route in Google Maps.

## How we built it
First iteration of idea: All-purpose app that would show you routes to what you want to do, takes into consideration weather, traffic, etc. This would have taken more time, and we wanted to focus on something more feasibly created in the time.

Second iteration of idea: Narrowed the idea down to running. This idea was our final project with other features such as adding waypoints to stop at on the way or keeping routes out of high-crime areas.

Third (final) iteration of idea: Narrowed the idea down to creating a running route using a desired location and distance.

We started by researching different APIs that we could use to generate the route. We looked at various parts of the Google Maps Platform, including snapToRoads and nearestRoad as well as the Places and Directions APIs. We also looked at using OpenStreetMaps which provided nodes and linkages for a bounded zone. 

Our original idea was to have an origin and generate four points of a set radius around this origin. These points would be used as the waypoints for a route. However, after a good night's sleep (or at least the hackathon equivalent of one), we determined that this method wouldn't be particularly useful for a user.  We decided that it'd be more useful for a user to give a starting location and a distance that they wanted to run.

First, we used the Geocode API to take a users location (origin point) and determine the longitude and latitude. We randomized the height and the width of a rectangle such that the perimeter was equal to the inputted distance. We took these values and transformed the origin point to get four corners of a rectangle. These four points were then snapped to their nearest roads using the Nearest Roads API, put into a list as tuples of (latitude, longitude), and then returned.

The Python code was then copied onto a Google Cloud Function and linked to our JavaScript front-end. This web app had an input box for location, a button to set location to current location, an input box for distance, a button to run the program, and a map. 

We realized that this original route algorithm created routes that were longer than the desired distance and occasionally failed to snap points to roads. We decided to develop a more complex algorithm where we adjusted the waypoints on the route until they were within a desired range.

Our next algorithm added to the previous one, adding a system for adjusting points based on their direction from the previous point and whether or not it was greater than a scaled value.

This algorithm took longer to load, but was much more accurate with the distance values (usually coming within 0.3 miles of the desired distance). We decided that the increase in accuracy was worth more than the loss in time. 

We also added a loading screen using JavaScript to inform the user that the route was being created and to hide the other content on the page while waiting for the request from the server. Additionally, we added a link to Google Maps with the given path waypoints to allow users to track their location when traveling on the path.

We spent the rest of the time tweaking the algorithm to be faster without sacrificing accuracy.

## Challenges we ran into
We weren't sure we would be able to build it at all because the Google Maps API is designed to find most efficient routes between two points. We were unsure on how to utilize the API functionality while minimizing the number of calls to it. 

We had trouble figuring out how to connect our web front end, where user input is taken and the map is displayed, and our back end, which determines the path from the inputs and is written in Python.

We had trouble determining how we wanted to design the front end.

Our original algorithm produced routes that were much longer than the desired distance.

We had trouble coming up with an idea that we were confident could be completed, would be challenging, and would be fun to make.

We had problems balancing between our algorithm running more quickly or more accurately.

## Accomplishments that we're proud of
The algorithm determines a route that is accurate to the desired distance beyond initial expectations.

The routes are randomized such that no two are the same.

The name is something we are all proud of.

The amount of hard work we put into designing, implementing, and troubleshooting the project.

We're proud that we got the Google Maps API working.

We're proud that we got the loading animation working because it looks very cool.

We're also proud that we got the loading screen working correctly overall so that the user can actually know that the program is working.

We're proud that the routes can be opened in the full version of Google Maps so that turn-by-turn navigation can be used while you're trying out a route in real life.

## What we learned
Tony: I learned a lot about using Web APIs, designing for the best user experience, working on large computer science projects in a team, committing to GitHub, connecting JavaScript and Python functions, how to use the Google Cloud Platform, and communicating so that all teammates are on the same page.

Alex: I learned a lot about using the Google Maps API and calling Google Cloud Functions from the front-end to offload processing to the backend, as well as getting a taste of React, which I'm eager to use in a future project or a further version of this one.

Will: I learned how to use the Google Maps API and how to design an algorithm that could find various points to connect to an existing route while avoiding exceeding the given distance.

Kayton: I learned a lot about front-end development, including using CSS, HTML, and even React when we were briefly planning to use it. I also read through much of the google maps API to help my team determine the best plan of action for creating the path. 

## What's next for Routedoors
In the future, we'd like to add weather functionality, high crime area avoidance, and continue to improve the consistency of the accuracy of the algorithm. Utilizing locations around the route origin to determine the most safe and beautiful run (I.e closer to lakes/ponds/parks) would be a great way to further add needed functionality to the app for runners. We'd also like to add some pretty designs to make the web app more visually appealing, add a button to toggle between bike and running routes, and include a way to set specific points you want to run past. 
Additionally, since we are avid runners who are always looking to adventure through new routes, this is something that we will be using long after this hackathon is over.

## Attributions
Our logo makes use of an image of a tree made by Edward Boatman from The Noun Project.