from flask import Flask, render_template
import json
import requests
from difflib import SequenceMatcher
import csv
import os

app = Flask(__name__)

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

unDistricts = {"Mumbai":"Greater Bombay","Bengaluru Rural":"Bangalore Rural","Bengaluru Urban":"Bangalore Urban","South Delhi":"Delhi","North Delhi":"Delhi","East Delhi":"Delhi","West Delhi":"Delhi","Gurugram":"Gurgaon","S.P.S Nellore":"Nellore"}
polygons = {}
multipolygons = {}
polygonsCoords = {}
multipolygonsCoords = {}

def assignColor(value):
	if value > 600:
		return("#ed2a0c")
	elif value < 2000 and value > 1000:
		return("#fa8c05")
	elif value < 1000 and value > 500:
		return("#f6fa05")
	elif value < 500 and value > 20:
		return("#08d8fc")
	else:
		return("#ffffff")



def csvParse(state):
	global activeDistricts
	global polygons
	global multipolygons
	colors = []
	actDists = getAllActiveCases()[0]
	distNum = getAllActiveCases()[1]
	baseUrl = "https://raw.githubusercontent.com/CombatingCovid19/master/India_CSVs/"+state+"/"
	delhiVal = 0
	dCount = 0
	dSus = 0
	dRec = 0
	dExp = 0
	k = 0
	for i in actDists:
		if i in unDistricts.keys():
			iAct = unDistricts[i]
		else:
			iAct = i
		#susUrl = baseUrl+"/Susceptible/"+state.lower()+i+"Susceptible.csv"
		'''
		These requests would take almost 3 minutes to fulfill. Therefore, I don't intend to use these!
		sus = (requests.get(baseUrl+"/Susceptible/"+state.lower()+i+"Susceptible.csv")).text
		inf = (requests.get(baseUrl+"/Infected/"+state.lower()+i+"Infected.csv")).text
		rec = (requests.get(baseUrl+"/Recovered/"+state.lower()+i+"Recovered.csv")).text
		exp = (requests.get(baseUrl+"/Susceptible"+state.lower()+i+"Exposed.csv")).text
		'''
		filepath = "static/India_CSVs/"+state+"/"
		sus = (open((filepath+"Susceptible/"+state.lower()+i+"Susceptible.csv"),"r").read())
		inf =(open((filepath+"Infectious/"+state.lower()+i+"Infectious.csv"),"r").read())
		rec = (open((filepath+"Recovered/"+state.lower()+i+"Recovered.csv"),"r").read())
		exp = (open((filepath+"Exposed/"+state.lower()+i+"Exposed.csv"),"r").read())
		susValue = float(sus.split("\n")[0].split("e")[0])*(pow(10.0,(float(sus.split("\n")[0].split("e")[1]))))
		infValue = float(inf.split("\n")[0].split("e")[0])*(pow(10.0,(float(inf.split("\n")[0].split("e")[1]))))
		recValue = float(rec.split("\n")[0].split("e")[0])*(pow(10.0,(float(rec.split("\n")[0].split("e")[1]))))
		expValue = float(exp.split("\n")[0].split("e")[0])*(pow(10.0,(float(exp.split("\n")[0].split("e")[1]))))
		if "Delhi" in i:
			delhiVal += infValue
			dSus += susValue
			dRec += recValue
			dExp += expValue
			dCount += 1
			if dCount == 10:
				color = assignColor(delhiVal)
				prop = [dSus,dRec,dExp,delhiVal]
				polyProp = [color,prop]
				polygons["Delhi"] = polyProp
		elif iAct != i:
			totalInf = distNum[k] + infValue
			if i in polygons.keys():
				color = assignColor(totalInf)
				prop = [susValue, infValue, recValue,expValue]
				polyProp = [color,prop]
				polygons[iAct] = polyProp
			elif i in multipolygons.keys():
				color = assignColor(totalInf)
				prop = [susValue, infValue, recValue,expValue]
				polyProp = [color,prop]
				multipolygons[iAct] = polyProp
		else:	
			totalInf = distNum[k] + infValue
			if i in polygons.keys():
				color = assignColor(totalInf)
				prop = [susValue, infValue, recValue,expValue]
				polyProp = [color,prop]
				polygons[i] = polyProp
			elif i in multipolygons.keys():
				color = assignColor(totalInf)
				prop = [susValue, infValue, recValue,expValue]
				polyProp = [color,prop]
				multipolygons[i] = polyProp
		k += 1

def matches(name,activeDistricts):
	for i in activeDistricts:
		if (SequenceMatcher(a=name,b=i).ratio()) > 0.85:
			return True
		else:
			return False

def getAllActiveCases():
	req = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
	jsonText = req.text
	jsonList = json.loads(jsonText)
	activeDistricts = []
	distNumbers = []
	for i in jsonList:
		for d in i["districtData"]:
			if int(d["active"]) > 2:
				if d["district"] in ["Bongaigaon","Yamunanagar","Fatehabad","Jind","Ahmednagar","Buldhana","Raigad","Burhanpur","Harda","Morena","Chittorgarh","Dholpur","Rajsamand","Y.S.R. Kadapa","Katihar","Durg","Kabeerdham","Surajpur","Ahmedabad","Banaskantha","Chhota Udaipur","Devbhumi Dwarka","Jamnagar","Mehsana","Panchmahal","Budgam", "Bandipora","Baramulla","Samba","Shopiyan","Bengaluru Urban","Davanagere","Tumakuru","Balasore","Ganjam","Jajpur","Barnala","Fatehgarh Sahib","Fazilka","Ferozepur","Gurdaspur","Moga","Rupnagar","Sri Muktsar Sahib","Ariyalur","Kanyakumari","Tiruvannamalai","Jayashankar Bhupalapally","Komaram Bheem","Dhalai","Bareilly","Etawah","Gorakhpur","Hathras","Jhansi","Pratapgarh","Siddharthnagar","Udham Singh Nagar","Birbhum","Paschim Medinipur","Purba Medinipur","Purba Bardhaman"]:
					pass
				else:
					activeDistricts.append(d["district"])
					distNumbers.append(d["active"])
				
			else:
				pass
	return [activeDistricts,distNumbers]
@app.before_first_request
def parseJson():
	global unDistricts
	global polygons
	global multipolygons
	global polygonsCoords
	global multipolygonsCoords
	activeDistricts = getAllActiveCases()[0]
	'''
	with open("india_district.geojson") as f:
		geojson = json.load(f)
		This code was removed due to errors with mod_wsgi used on the production server. 
	'''
	georeq = requests.get("https://raw.githubusercontent.com/dhruvv/CombatingCovid19/master/india_district.geojson")
	geojson = json.loads(georeq.text)
	k = 0
	for i in geojson["features"]:
		name = i["properties"]["NAME_2"]
		#print(type(act))
		if name in activeDistricts or name in unDistricts.values() or matches(name,activeDistricts):
			if i["geometry"]["type"] == "MultiPolygon":	
				multipolygons[name] = (str(json.dumps(i))).replace("\"","\'")
				multipolygonsCoords[name] = i["geometry"]["coordinates"]
			elif i["geometry"]["type"] == "Polygon":
				polygons[name] = (str(json.dumps(i))).replace("\"","\'")
				polygonsCoords[name] = i["geometry"]["coordinates"]
		else:
			pass

@app.route('/')
def index():
	return render_template("mainindex.html")
@app.route('/withoutmask')
def simulationWithout():
	global polygons
	global multipolygons
	csvParse("NoMask")
	return render_template("index.html",polygons=polygons,multipolygons=multipolygons,polygonsCoords=polygonsCoords,multipolygonsCoords=multipolygonsCoords)

@app.route('/withmask')
def simulationWith():
	global polygons
	global multipolygons
	return render_template("index.html",polygons=polygons,multipolygons=multipolygons,polygonsCoords=polygonsCoords,multipolygonsCoords=multipolygonsCoords)
@app.route('/currentconditions')
def currentSim():
	global polygons
	global multipolygons
	return render_template("index.html",polygons=polygons,multipolygons=multipolygons,polygonsCoords=polygonsCoords,multipolygonsCoords=multipolygonsCoords)


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)


