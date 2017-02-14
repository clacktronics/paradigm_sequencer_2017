import sys, re, os

loopDetect = 0
loopStore = []
loop = 1
loopTitle = ''

fileName = sys.argv[1]

outputFile = '%s_compiled.txt' % (fileName)

if os.path.isfile(outputFile):
	print "error, output file already exists"
	quit()


output_sequence = []
output_markers = []
output_delays = []

step_count = 0
last_delay = 0

with open(fileName, 'r') as datatxtLine:
		for line in datatxtLine:

			pattern = re.compile('((loop|delay) *= *(\d*.\d*))|([0-9][ \.0-9]+)|([a-zA-Z0-9]+)')
			lineRead = pattern.search(line)

			# Compile and identify the line
			# Group 1 variable detect
			# Group 2 variable name
			# Group 3 variable value
			# Group 4 sequence step (0 0 0 0 0 0 0 0)
			# Group 5 Plain text (sequence title)
			# *((loop|delay) *= *(\d*.\d*))?([ \.0-9]*)([ a-zA-Z0-9]*)

			if lineRead != None:
				if lineRead.group(4) != None:
					output_sequence.append(line.replace(' ','').strip())
					step_count += 1

				if lineRead.group(1) != None:
					if lineRead.group(2) == "loop":
						output_markers[-1][2] = int(lineRead.group(3))

					if lineRead.group(2) == "delay":
						if len(output_markers) > 0:
							output_delays[-1] = float(lineRead.group(3))
						last_delay = float(lineRead.group(3))

				elif lineRead.group(5):
					output_markers.append([step_count,0,0,line.strip()])
					output_delays.append(last_delay)
					# if its not the first loop mark the last loops end
					if len(output_markers) > 1:
						 output_markers[-2][1] = step_count-1
output_markers[-1][1] = step_count-1

file = open('output.txt','w')

file.write('uint16_t sequence[][3] = \n{\n')
for marker in output_markers:
	file.write('{%s,%s,%s},\t//%s \n' % (marker[0], marker[1], marker[2], marker[3]))
file.write('};\n\n\n\n')

file.write('uint32_t delays[]\n = {\n')
for d, delay in enumerate(output_delays):
	file.write('%s, \t//%s\n' % (delay, output_markers[d][3]))
file.write('};\n\n\n\n')

file.write('uint8_t sequence_data[][8]\n = {\n')
for s, step in enumerate(output_sequence):
	for marker in output_markers:
		if int(marker[0]) == s:
			file.write('\n')
	stepper = ','.join(list(step))
	file.write('{%s},' % stepper)
	for marker in output_markers:
		if int(marker[0]) == s:
			file.write(' \t//%s' % marker[3])
	file.write('\n')
file.write('};\n\n\n\n')
file.close()
