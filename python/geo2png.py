# trafo -> png
# Original source https://github.com/vrandezo/wikidata-analytics/blob/6896d639bd124eec7571f1179f27ae2b6bfaa435/geo2png.py
# Re written for different data input by Addshore
# Script takes roughly 5-10 minutes to run
import png, gzip, json, sys, time, os

settings = {
	'icon' : {
		'x' : 80,
		'y' : 80,
		'diffr' : 80,
		'diffg' : 5,
		'diffb' : 1
	},
	'tiny' : {
		'x' : 500,
		'y' : 250,
		'diffr' : 100,
		'diffg' : 10,
		'diffb' : 2
	},
	'small' : {
		'x' : 1000,
		'y' : 500,
		'diffr' : 100,
		'diffg' : 25,
		'diffb' : 8
	},
	'normal' : {
		'x' : 2000,
		'y' : 1000,
		'diffr' : 150,
		'diffg' : 40,
		'diffb' : 10
	},
	'big' : {
		'x' : 4000,
		'y' : 2000,
		'diffr' : 150,
		'diffg' : 50,
		'diffb' : 10
	},
	'huge' : {
		'x' : 8000,
		'y' : 4000,
		'diffr' : 150,
		'diffg' : 70,
		'diffb' : 20
	}
}

startTime = time.time()

# Load the js file into a var
print "Loading data file"
dataDirectory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data")
fileContent = ""
with open (os.path.join(dataDirectory, "wdlabel.js"), "r") as dataFile:
	fileContent=dataFile.read()

# Instead of doing this the main generation should simply generate a json file!
print "Cleaning file"
if fileContent.startswith('var geodata = '):
	fileContent = fileContent[len('var geodata = '):]
if fileContent.endswith(';'):
	fileContent = fileContent[:-len(';')]

print "Loading to data to Dictionary"
data = json.loads(fileContent)

# Generate PNGs!
print "Generating PNGs"
for size in settings.keys() :
	print size
	print settings[size]

	p = [[0]*(settings[size]['x'] * 3) for i in range(settings[size]['y'])]

	count = 0
	badCoordCount = 0

	for key in data:
		keyData = data[key]
		# TODO find out why X and Y swap here
		geox = data[key]['y']
		geoy = data[key]['x']
		subject = data[key]['label']
		if float(geox) > 180 or float(geox) < -180 or float(geoy) > 90 or float(geoy) < -90 :
			# These coords dont make sense on earth
			badCoordCount += 1
			#print geoy, geox
			continue
		posx = int((float(geox) + 180.0)/361.0*settings[size]['x'])
		posy = abs(int((float(geoy) -  90.0)/181.0*settings[size]['y']))
		p[posy][posx*3] = min(p[posy][posx*3]+settings[size]['diffr'], 255)
		p[posy][posx*3+1] = min(p[posy][posx*3+1]+settings[size]['diffg'], 255)
		p[posy][posx*3+2] = min(p[posy][posx*3+2]+settings[size]['diffb'], 255)

		count += 1
		#if count > 10 : break

	print size, "Map saving..."
	print count, "entities"
	print badCoordCount, "bad coordinates"

	f = open('map_' + size + '.png', 'wb')
	w = png.Writer(settings[size]['x'], settings[size]['y'])
	w.write(f, p)
	f.close()
	print size, "Map saved..."

print "Finished."
print "Execution time: ", time.time()-startTime, " seconds"
