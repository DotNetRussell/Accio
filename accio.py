#!/usr/bin/python

'''
Author: Anthony Russell
Contact: @DotNetRussell
Blog: https://DotNetRussell.com

Accio was written to quickly spin up fake server side endpoints that return custom json responses.

To use:
Create a config json file with an array of routes in it. Each route will be made of a url path and a path to a json file you want to be returned.

If you're still confused, see the example json files or reach out to me

'''

from http.server import BaseHTTPRequestHandler, HTTPServer
#from http.server.HTTPServer import BaseHTTPRequestHandler, HTTPServer

import sys
import json
import time

def printHelp():
	print("")
	print("Accio")
	print("Author: Anthony Russell")
	print("Twitter: @DotNetRussell")
	print("Blog: https://DotNetRussell.com")
	print("GitHub: https://github.com/DotNetRussell")
	print("")
	print("To Use:")
	print("python accio.py [config file path] [target localhost port]")
	print("")
	print("Example")
	print("python accio.py /home/user/Desktop/accioConfig.json 8080")
	print("")

if(len(sys.argv) != 3):
	printHelp()
	sys.exit()

configFile = sys.argv[1]
targetPort = int(sys.argv[2])
callingPort = 4200

routeDictionary = {}

with open(configFile) as json_file:
	data = json.load(json_file)
	for route in data['routes']:
		url = route['url']
		definition = route['definition']

		if('method' in definition.keys()) :
			url = url + "_" + str(definition['method']).lower()
		else :
			url = url + "_get"

		routeDictionary[url] = definition

def wildCardPathLookup(path,method):
	pathParts = (path+"_"+method).split("/")
	while("" in pathParts) :
    		pathParts.remove("")

	result = None
	for route in routeDictionary:
		if("{$}" in route):
			routeParts = route.split("/")
			while("" in routeParts):
				routeParts.remove("")

			if(len(routeParts) == len(pathParts)):
				for x in range(0, len(pathParts)):

					if("{$}" in routeParts[x]):
						continue
					elif(routeParts[x] != pathParts[x]):
						break
					elif(x == len(pathParts)-1):
						result = route
						break
			else:
				continue

			if(result != None):
				break

	return result

def generateResponse(self, method):
	print('Generating response')
	wildCardLookup = wildCardPathLookup(self.path,method)

	if( (self.path + "_" + method) not in routeDictionary and wildCardLookup == None):
		self.send_response(404)
		print(self.path + "_" + method + " - Not Found")
		return

	routeDefinition = None
	if(wildCardLookup == None):
		routeDefinition = routeDictionary[self.path + "_" + method]
	else:
		routeDefinition = routeDictionary[wildCardLookup]

	if('delay' in routeDefinition.keys()) :
		print('Running a delay')
		time.sleep(routeDefinition['delay'])

	jsonFilePath = routeDefinition["filePath"]
	payloadData = open(jsonFilePath)
	response = ''
	for line in payloadData.readlines():
		response = response + line.strip()

	print('sending response')
	self.send_response(200)
	self.send_header('Access-Control-Allow-Origin', 'http://localhost:' + str(callingPort));
	self.send_header('Content-type','text/json')
	self.end_headers()
	self.wfile.write(response.encode("utf-8"))

	return


class requestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		return generateResponse(self, "post")

	def do_GET(self):
		return generateResponse(self, "get")

	def do_PUT(self):
		return generateResponse(self, "put")

	def do_DELETE(self):
		return generateResponse(self, "delete")
try:
	server = HTTPServer(('', targetPort), requestHandler)
	print("Accio --% ~~~~ @X@ Server Active @X@")
	print("Server Listening On Port " + str(targetPort))
	print("Press CTRL+C to stop the server")

	server.serve_forever()

except KeyboardInterrupt:
	print('Shutting down the web server')
	server.socket.close()
