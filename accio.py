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


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import sys
import json


def printHelp():
	print ""
	print "Accio"
	print "Author: Anthony Russell"
	print "Twitter: @DotNetRussell"
	print "Blog: https://DotNetRussell.com"
	print "GitHub: https://github.com/DotNetRussell"
	print ""
	print "To Use:"
	print "python accio.py [config file path] [target localhost port] [calling port (because of CORS)]"
	print ""
	print "Example"
	print "python accio.py /home/user/Desktop/accioConfig.json 8080 4200"
	print ""

if(len(sys.argv) != 4):
	printHelp()
	sys.exit()

configFile = sys.argv[1]
targetPort = int(sys.argv[2])
callingPort = int(sys.argv[3])

routeDictionary = {}

with open(configFile) as json_file:
    data = json.load(json_file)
    for route in data['routes']:
        url = route['url']
        path = route['path']
	routeDictionary[url] = path

class requestHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if(self.path not in routeDictionary):
			self.send_response(404)
			print self.path + "Not Found"
			return

		jsonFile = open(routeDictionary[self.path],"r+")
		response = '\n'.join(jsonFile.readlines())
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', 'http://localhost:' + str(callingPort));
		self.send_header('Content-type','text/json')
		self.end_headers()
		self.wfile.write(response)
		return

try:
	server = HTTPServer(('', targetPort), requestHandler)
	print "Accio --% ~~~~ @X@ Server Active @X@"
	print "Server Listening On Port " + str(targetPort)
	print "Press CTRL+C to stop the server"

	server.serve_forever()

except KeyboardInterrupt:
	print 'Shutting down the web server'
	server.socket.close()
