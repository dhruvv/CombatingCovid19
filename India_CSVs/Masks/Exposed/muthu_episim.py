from seirsplus.models import *
import networkx
import numpy as np
import  requests
import json
import os 
import pickle


dname = np.array([])
attr_files = np.array([])
pickle_files = np.array([])

os.path.join(r"C:\Users\Dhruv\OneDrive - Greenwood High\Simparse\ReGenerated")
files = [f for f in os.listdir('.') if f.endswith('.pkl')]   
pickle_files = np.append(pickle_files, files)
for a in pickle_files:
	b = a[0]
	#print(b)
	if b == "a":
		attr_files = np.append(attr_files, a)


req = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
activeCases = {}
jsonText = req.text
#activeCases = []
jsonList = json.loads(jsonText)
#print(jsonList[1]["districtData"][0])
for i in jsonList:
  for d in i["districtData"]:
    distActCases = d["active"]
    distName = d["district"]
    activeCases[distName] = distActCases
    dname = np.append(dname, distName)

os.path.join(r"C:\Users\Adithya Ramnarayanan\Greenwood High\Dhruv Venkataraman (02717) - Simparse\ReGenerated\NoMask")
for z in attr_files:
	for i in dname:
		data = np.array([])
		b = z.find(i)
		if b > 0:
			file = open(z,"rb")
			attr = pickle.load(file)
			x = attr[0]
			y = activeCases[i]
			print(y)
			if x > y:
				#baseGraph = networkx.barabasi_albert_graph(n=x, m=9)
				model = SEIRSModel(beta=0.0058, sigma=1/2.2, gamma=1/14,initN = x,initI=y)
				model.run(T=300)
				detected = model.numE
				print(detected)
			else:
				detected = 0
			data = np.append(data, detected)
			np.savetxt("nomask"+i+"Exposed.csv", data , delimiter=",")