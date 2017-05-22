# TrafficDetection
This is my first traffic detection programm

# Purpose
I am living in Niederbrechen, a beautiful village with one downsight: The B8 (Bundesstraße 8). More and more traffic is coming up, so some people who are living directly on the B8 formed an intiative to get a bypass road. Therefore they asked some school kids to gather some traffic data on one specific day. The high numbers just showed, that there is too much traffic. But it does not show, where the traffic comes from and were it goes to (let's say a dynamical flow analysis). Furthermore, those bored school kids took the data on one single day. This is ridiculus. I am an engineer, I need data. MORE data.

#Idea
This is where my traffic detection algorithm comes in. I first tried out, if it might be possible to count the traffic. So I frist checked radar-based or infrared-based ideas. Those where all to expensive or required some physical hardware on or beside the street, which is not possible. So I checked video-based tracking (even it's somehow illegal to monitor streets in germany). I found some interesing videos on youtube and some great tutorials about opencv and so my work started. I took some basic code and developed something to fit to my view angle, etc. Finally I made some checks (counting some traffic - me vs. the algo) and the results were according to my expectation (95% detction rate). The 5% were explainable and measured under a specifc circumstance - traffic stucks (so no movement) on one road, but the road behind it still shows traffic. The objects in the front are "shadowing" the others and so my algo doesn't count it properly. For me, that's ok for the moment. Maybe I can adjust the camera angle or adopt the algo in the future to reduce the detection window when traffic stucks. So let's go on with my idea.

#Port it to a single-standing environment
The RaspberryPI...fantastic...30€ which solves most of mankinds problems... I ordered a ~100€ package (power supply, RasPi3, Cam, SD), because I spend lot of time to make the stuff running on my old RasPI1 which was used as media center in the past.
I need to understand this now, learn some linux and port my algo to the PI.

#Run a mid-term measurement
Let's run this stuff now for a week or so to gather some data and check if the algo is robust enough (re-learning background, night vision capability, statistics, etc.)

#Web Server
use cherrypy to create a webserver to have access to the data

#multiple measurement points
buy three additional RasPIs to gather the data on four sampling points (north, south, east, west) and ask some friends for WiFi and power.

#Run a long-term measurement
connect the data from all four RasPis in one statistic to have time-specific data of all entry and exit points to our village. With this data I can

#Simulate the traffic flow on a daily base
maybe Matlab or so can help me out there. With this simulation data, I can hopefully simulate how the different bypass roads will affect my street.

#Go to the initiative and major and provide my findings.
