import SocketServer
import SimpleHTTPServer
import json
import re
import unicodedata
import sys

class Reply(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		# query arrives in self.path; return anything, e.g.,
		# self.wfile.write("query was %s\n" % self.path)
		query = self.path
		one = None
		two = None
		three = None
		ret = False
		# actualSec = None

		if (query[-1] == '/'):
			self.wfile.write("\n")
			return

		splitQuery = re.split('/', query)
		splitQuery = filter(None, splitQuery)
		# self.wfile.write("splitQuery is %s\n" % splitQuery)

		# self.wfile.write(type(splitQuery[0]))
		# self.wfile.write("\nThat is the type of query\n")
		with open('courses.json') as data_file:    
			data = json.load(data_file)

		count = 0
		# self.wfile.write("This the length of data: %d\n" % len(data))
		for index in range(len(data)):

			listing = data[index] # this is a dict
			inSection = 0

			# list with course number information
			courseNum = listing['listings']
			# area/distribution
			area = listing['area']
			# section: need to iterate through to just pull out the lecture times
			classes = listing['classes']
			# for each item in section, iterate to find proper date and time (days, starttime, endtime)
			# for lecture, iterate to find building (bldg)
			# also get the roomnum
			# title of course
			title = listing['title']

			# self.wfile.write("This is the title: %s\n" % title)
			# profs: need to iterate through to grab names
			prof = listing['profs']
			sections = []
			# failed = False
			# dup = False

			for i in range(len(classes)):
				specified = classes[i]
				section = specified['section']
				# et = unicodedata.normalize('NFKD', section).encode('ascii', 'ignore')
				if (re.match('L|C|S|U', section) != None):
					dup = False
					for num in range(len(sections)):
						if sections[num] == section:
							dup = True
					if dup == False:
						sections.append(specified)

			# self.wfile.write("Length of sections is %d\n" % len(sections))

			for numSections in range(len(sections)):
				inSection = 1
				actualSec = sections[numSections]
				failed = False
				# self.wfile.write("This is the current section %s\n" % actualSec['section'])
				# this is for each query
				for search in splitQuery: 
					success = 0
					# if it's a specific date
					# m, t, w, th, f, mw, mwf, tth, twth, mtwth and mtwthf.
					if (len(search) == 1): 
						if search.lower() == 'm':
							if actualSec['days'].lower() == 'm':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 't':
							if actualSec['days'].lower() == 't':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'w':
							if actualSec['days'].lower() == 'w':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'f':
							if actualSec['days'].lower() == 'f':
								success = success + 1
							else:
								failed = True
							continue
						else:
							# prob don't even need this line
							failed = True
							break
					elif (len(search) == 2):
						if search.lower() == 'th':
							if actualSec['days'].lower() == 'th':
								success = success + 1
							else:
								failed = True
							continue
						
						elif search.lower() == 'mw':
							if actualSec['days'].lower() == 'mw':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'la':
							if area.lower() == 'la':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'sa':
							if area.lower() == 'sa':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'ha':
							if area.lower() == 'ha':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'em':
							if area.lower() == 'em':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'ec':
							if area.lower() == 'ec':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'qr':
							if area.lower() == 'qr':
								success = success + 1
							else:
								failed = True
							continue
						else:
							break
					elif (len(search) == 3):
						if search.lower() == 'mwf':
							if actualSec['days'].lower() == 'mwf':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'tth':
							if actualSec['days'].lower() == 'tth':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'stl':
							if area.lower() == 'stl':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'stn':
							if area.lower() == 'stn':
								success = success + 1
							else:
								failed = True
							continue
						else:
							for dept in range(len(courseNum)):
								courseInfo = courseNum[dept]
								if courseInfo['dept'].lower() == search.lower():
									success = success + 1
								if courseInfo['number'].lower() == search.lower():
									success = success + 1
							if success == 0:
								break
							else:
								continue
							

					elif search.lower() == 'twth':
						if actualSec['days'].lower() == 'twth':
							success = success + 1
						else:
							failed = True
						continue
					elif search.lower() == 'mtwth':
						if actualSec['days'].lower() == 'mtwth':
							# self.wfile.write("Actual days: %s\n" % actualSec['days'])
							# self.wfile.write("Search: %s\n" % search)
							# self.wfile.write("Success: %d\n" % success)
							success = success + 1
							# self.wfile.write("Success? %d\n" % success)
							# success = success + 1
						else:
							failed = True
						continue
					elif search.lower() == 'mtwthf':
						if actualSec['days'].lower() == 'mtwthf':
							success = success + 1
						else:
							failed = True
						continue

					else:

						success = 0
						for j in range(len(courseNum)):
							courseInfo = courseNum[j]
							if (re.search(search, courseInfo['dept'], re.IGNORECASE) != None):
								success = success + 1
							if (re.search(search, courseInfo['number'], re.IGNORECASE) != None):
								success = success + 1
						if (re.search(search, title, re.IGNORECASE) != None):
							# self.wfile.write("Actual title: %s\n" % title)
							# self.wfile.write("Search: %s\n" % search)
							# self.wfile.write("Success: %d\n" % success)
							success = success + 1
							# self.wfile.write("Success? %d\n" % success)
							# success = success + 1

						for j in range(len(prof)):
							profName = prof[j]
							if (re.search(search, profName['name'], re.IGNORECASE) != None):
								success = success + 1

						# if (re.search(search, courseNum, re.IGNORECASE) != None):

						# if (len(sections) == 0):

					
						if (re.search(search, actualSec['bldg'], re.IGNORECASE) != None):
							success = success + 1
						if (re.search(search, actualSec['starttime'], re.IGNORECASE) != None):
							# self.wfile.write("Actual starttime: %s\n" % actualSec['starttime'])
							# self.wfile.write("Search: %s\n" % search)
							# self.wfile.write("Success: %d\n" % success)
							success = success + 1
							# self.wfile.write("Success? %d\n" % success)
						if (re.search(search, actualSec['endtime'], re.IGNORECASE) != None):
							success = success + 1
						if (re.search(search, actualSec['roomnum'], re.IGNORECASE) != None):
							success = success + 1
						if (re.search(search, actualSec['days'], re.IGNORECASE) != None):
							success = success + 1
						if success == 0:
							failed = True
					# if (success != 0): # it's a success
						# self.wfile.write("query was %s\n" % self.path)
							# return within the section
				if (success != 0 and failed is False):
					ret = True
					#self.wfile.write("length of section is %d\n" % len(sections))
					for names in range(len(courseNum)):
						courseInfo = courseNum[names]
						if names == (len(courseNum) - 1):
							self.wfile.write("%s " % courseInfo['dept'])
							self.wfile.write("%s " % courseInfo['number'])
						else:
							self.wfile.write("%s " % courseInfo['dept'])
							self.wfile.write("%s/" % courseInfo['number'])
					self.wfile.write("%s " %area)
					self.wfile.write("%s " %actualSec['section'])
					self.wfile.write("%s " %actualSec['days'])
					start = re.split(' ', actualSec['starttime'])[0]
					end = re.split(' ', actualSec['endtime'])[0]
					self.wfile.write("%s-" % start)
					self.wfile.write("%s " % end)
					self.wfile.write("%s " %title.encode('utf8'))

					for names in range(len(prof)):
						profName = prof[names]
						if names == (len(prof) - 1):
							self.wfile.write("%s " %profName['name'].encode('utf8'))
						else:
							self.wfile.write("%s/" %profName['name'].encode('utf8'))
					self.wfile.write("%s " %actualSec['bldg'])
					self.wfile.write("%s\n" %actualSec['roomnum'])
					success = 0;

			# self.wfile.write("Length of sections is %d\n" % len(sections))

			# if there are no sections
			if (len(sections) == 0):
				failed = False
				# in loop
				#self.wfile.write("length of section is %d\n" % len(sections))
				# self.wfile.write("in the right place!\n")
				# self.wfile.write("This is the title: %s\n" % title)
				# self.wfile.write("This is the search: %s\n" % splitQuery[0])
				for search in splitQuery: # this is for each query
					success = 0
					if (len(search) == 1): 
						if search.lower() == 'm':
							if actualSec['days'].lower() == 'm':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 't':
							if actualSec['days'].lower() == 't':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'w':
							if actualSec['days'].lower() == 'w':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'f':
							if actualSec['days'].lower() == 'f':
								success = success + 1
							else:
								failed = True
							continue
						else:
							# prob don't even need this line
							failed = True
							break
					elif (len(search) == 2):
						if search.lower() == 'th':
							if actualSec['days'].lower() == 'th':
								success = success + 1
							else:
								failed = True
							continue
						
						elif search.lower() == 'mw':
							if actualSec['days'].lower() == 'mw':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'la':
							if area.lower() == 'la':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'sa':
							if area.lower() == 'sa':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'ha':
							if area.lower() == 'ha':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'em':
							if area.lower() == 'em':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'ec':
							if area.lower() == 'ec':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'qr':
							if area.lower() == 'qr':
								success = success + 1
							else:
								failed = True
							continue
						else:
							break
					elif (len(search) == 3):
						if search.lower() == 'mwf':
							if actualSec['days'].lower() == 'mwf':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'tth':
							if actualSec['days'].lower() == 'tth':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'stl':
							if area.lower() == 'stl':
								success = success + 1
							else:
								failed = True
							continue
						elif search.lower() == 'stn':
							if area.lower() == 'stn':
								success = success + 1
							else:
								failed = True
							continue
						else:
							for dept in range(len(courseNum)):
								courseInfo = courseNum[dept]
								if courseInfo['dept'].lower() == search.lower():
									success = success + 1
								if courseInfo['number'].lower() == search.lower():
									success = success + 1
							if success == 0:
								break
							else:
								continue
							

					elif search.lower() == 'twth':
						if actualSec['days'].lower() == 'twth':
							success = success + 1
						else:
							failed = True
						continue
					elif search.lower() == 'mtwth':
						if actualSec['days'].lower() == 'mtwth':
							# self.wfile.write("Actual days: %s\n" % actualSec['days'])
							# self.wfile.write("Search: %s\n" % search)
							# self.wfile.write("Success: %d\n" % success)
							success = success + 1
							# self.wfile.write("Success? %d\n" % success)
							# success = success + 1
						else:
							failed = True
						continue
					elif search.lower() == 'mtwthf':
						if actualSec['days'].lower() == 'mwf':
							success = success + 1
						else:
							failed = True
						continue

					else:
						success = 0
						for j in range(len(courseNum)):
							courseInfo = courseNum[j]
							if (re.search(search, courseInfo['dept'], re.IGNORECASE) != None):
								success = success + 1
							if (re.search(search, courseInfo['number'], re.IGNORECASE) != None):
								success = success + 1
						if (re.search(search, title, re.IGNORECASE) != None):
							# self.wfile.write("Actual title: %s\n" % title)
							# self.wfile.write("Search: %s\n" % search)
							# self.wfile.write("Success: %d\n" % success)
							success = success + 1
							# self.wfile.write("Success? %d\n" % success)
							# success = success + 1

						for j in range(len(prof)):
							profName = prof[j]
							if (re.search(search, profName['name'], re.IGNORECASE) != None):
								success = success + 1

						# if (re.search(search, courseNum, re.IGNORECASE) != None):

						# if (len(sections) == 0):

						if actualSec != None:
							if (re.search(search, actualSec['bldg'], re.IGNORECASE) != None):
								success = success + 1
							if (re.search(search, actualSec['starttime'], re.IGNORECASE) != None):
								success = success + 1
							if (re.search(search, actualSec['endtime'], re.IGNORECASE) != None):
								success = success + 1
							if (re.search(search, actualSec['roomnum'], re.IGNORECASE) != None):
								success = success + 1
							if (re.search(search, actualSec['days'], re.IGNORECASE) != None):
								success = success + 1
							if success == 0:
								failed = True
						if success == 0:
							failed = True
					# self.wfile.write("This is success: %d\n" % success)

				# self.wfile.write("This is success: %d\n" % success)
				if (success != 0 and failed is False):
					ret = True
					for names in range(len(courseNum)):
						courseInfo = courseNum[names]
						if names == (len(courseNum) - 1):
							self.wfile.write("%s " % courseInfo['dept'])
							self.wfile.write("%s    " % courseInfo['number'])
						else:
							self.wfile.write("%s " % courseInfo['dept'])
							self.wfile.write("%s/" %courseInfo['number'])
					self.wfile.write("%s " %area)
					self.wfile.write("%s " %title)
					for names in range(len(prof)):
						profName = prof[names]
						if names == (len(prof) - 1):
							self.wfile.write("%s\n" %profName['name'].encode('utf8'))
						else:
							self.wfile.write("%s/" %profName['name'].encode('utf8'))
				success = 0

		if ret == False:
			self.wfile.write("\n")
				# self.wfile.write("%s " %actualSec['bldg'])
				# self.wfile.write("%s " %actualSec['roomnum'])

				# if successful, change success to read True


				# if success == True:
					# print the successful section 


	# for item in data:
		# course is of type dict
		# course = data[count]

	# self.wfile.write(count)



def main():
  # read and parse courses.json
  # print(len(sys.argv))
  # print("That's the number of command line arguments")

  if (len(sys.argv) >= 2):
  	port = int(sys.argv[1])
  	SocketServer.ForkingTCPServer(('', port), Reply).serve_forever()
  else:
  	SocketServer.ForkingTCPServer(('', 8080), Reply).serve_forever()

main()
