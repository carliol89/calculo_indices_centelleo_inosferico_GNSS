CODIGO EMPLEADO PARA CALCULAR EL MAPA LOCAL DE CENTELLEO
gps_s4_interp_cartesian.py
1.	#!/usr/bin/python3
2.	import astropy.coordinates
3.	import astropy.time
4.	import sp3
5.	import pandas as pd
6.	import numpy as np
7.	import matplotlib.pyplot as plt
8.	import scipy.interpolate as spint
9.	from datetime import datetime, timedelta
10.	from matplotlib.pyplot import rc, grid, Figura, plot, rcParams, savefig
11.	from scipy import interpolate
12.	from matplotlib import cm
13.	 
14.	# https://stackoverflow.com/questions/18721762/matplotlib-polar-plot-is-not-plotting-where-it-should
15.	 
16.	lon = -67.1892
17.	lat = 10.1892
18.	 
19.	date = '2023-07-26T19:00:00'
20.	delta = 60
21.	date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
22.	time_range = pd.date_range(date, date + timedelta(minutes=delta), freq='5min')
23.	 
24.	date = time_range[0]
25.	 
26.	def altaz(sp3id, time_range, lon, lat):
27.	    print('Satellite:', sp3id)
28.	    sp3.cddis.username = "chris77ve"
29.	    sp3.cddis.password = "729TMzEDyQaNqxQ"
30.	    sp3_altaz = sp3.altaz_standard_atmosphere(
31.	        id=sp3.Sp3Id(sp3id), obstime=astropy.time.Time(time_range),
32.	        location=astropy.coordinates.EarthLocation.from_geodetic(lon=lon, lat=lat, height=0),
33.	        download_directory="sp3_cache")
34.	    pos = pd.DataFrame({'az': sp3_altaz.az.value, 'el': sp3_altaz.alt.value}, index=sp3_altaz.obstime.value)
35.	    pos.index = pos.index.rename('Time')        
36.	    azimuth   = np.array(np.radians(pos['az'].to_list()))
37.	    elevation = np.array(pos['el'].to_list())
38.	    return azimuth, elevation
39.	   
40.	sats = {}
41.	 
42.	 
43.	rc('grid', color='#00edff', linewidth=1, linestyle='-')    
44.	rc('xtick', labelsize=15)
45.	rc('ytick', labelsize=15)
46.	width, height = rcParams['Figura.figsize']
47.	size = 1.2 * min(width, height)
48.	fig = Figura(figsize=(size, size), facecolor=(0.5,0.5,0.5))
49.	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=False, facecolor='#000040')
50.	##ax.set_theta_zero_location('N')
51.	##ax.set_theta_direction(-1)
52.	##ax.set_rlim(bottom=90, top=0)
53.	##ax.set_rlabel_position(-22.5)
54.	#ax.set_yticklabels([])
55.	ax.tick_params(axis='x', colors='white', labelsize=15)
56.	ax.tick_params(axis='y', colors='white', labelsize=10)
57.	ax.set_title("GPS satellites / {} UTC".format(date, delta), va='bottom')
58.	ax.set_yticks(range(0, 90, 10))
59.	ax.grid(True)
60.	 
61.	s4_color = [
62.	0.1312692681133677,
63.	0.1303542301821031,
64.	0.1309567617308465,
65.	0.1304445840048616,
66.	0.1302837049273526,
67.	0.1304866507973108,
68.	0.1303870718248629,
69.	0.1306758565071753,
70.	0.1304195840062704,
71.	0.130256170185089,
72.	0.1305985282245173,
73.	0.1302790289217469,
74.	0.1297445076830805,
75.	0.130525235370919,
76.	0.1304838648755004,
77.	0.1305546683557786,
78.	0.1299102436593127,
79.	0.12870331543154,
80.	0.1309676584819102,
81.	0,
82.	0,
83.	0.1314207095679698,
84.	0,
85.	0.130038742276893,
86.	0.130499135649455,
87.	0,
88.	0.1312389658033457,
89.	0.1310957196125531,
90.	0,
91.	0,
92.	0,
93.	0.1306478004526702
94.	]
95.	suma = np.sum(s4_color)
96.	promedio=suma/32
97.	                
100.	PRN = {}
101.	for i in range(1, 33):
102.	    prn = 'G{:0>2}'.format(i)
103.	    if not prn in ['G32']:
104.	        az, el = altaz(prn, time_range, lon, lat)
105.	    if el[0] > 0:
106.	        sats[prn] = {'az': az[0], 'el': el[0], 'color':s4_color[i]}
107.	 
108.	 
109.	sats['G33'] = {'az': 0, 'el': 80, 'color': promedio} # agrega el diccionario {'az': 0, 'el': 80, 'color': 0.12} con la clave 'G33' al diccionario sats
110.	sats['G34'] = {'az': 10, 'el': 0, 'color':promedio} # agrega el diccionario {'az': 10, 'el': 0, 'color': 0.12} con la clave 'G34' al diccionario sats
111.	sats['G35'] = {'az': 10, 'el': 80, 'color': promedio} # agrega el diccionario {'az': 10, 'el': 80, 'color': 0.12} con la clave 'G35' al diccionario sats
112.	sats['G36'] = {'az': 0, 'el': 0, 'color': promedio} # agrega el diccionario {'az': 10, 'el': 80, 'color': 0.12} con la clave 'G35' al diccionario sats
113.	azimuth = []
114.	elevation = []
115.	color = []
116.	 
117.	for i in sats:
118.	    if sats[i]['color'] > 0:
119.	        prn = 'G{:0>2}'.format(i)
120.	        az = sats[i]['az']
121.	        el = sats[i]['el']
122.	        azimuth.append(az)
123.	        elevation.append(el)
124.	        color.append(sats[i]['color'])
125.	        c = '#' + hex(int(sats[i]['color'] * 255))[2:] + '0000'
126.	        #color= [ c + 0.05 for c in  color]
127.	        color.append(str(c))
128.	        print(sats[i]['color'], c)
129.	# Crea una nueva lista Solo con los elementos numéricos del array color
130.	color_float = [x for x in color if isinstance(x, (int, float))]
131.	# Imprime la nueva lista
132.	print(color_float)          
133.	 
134.	 
135.	f = interpolate.LinearNDInterpolator(list(zip(azimuth, elevation)), color_float)
136.	x = np.linspace(0, 10, num=100)
137.	y = np.linspace(0, 80, num=100)
138.	X, Y = np.meshgrid(x, y)
139.	 
140.	Z = f(X, Y)
141.	plt.pcolor(X, Y, Z, shading='auto', cmap=cm.jet)
142.	plt.scatter(azimuth, elevation, 300, color_float, marker='o', cmap=cm.jet)
143.	plt.colorbar()
144.	#plt.plot(azimuth, elevation, color, "ok", label="input point")
145.	plt.savefig('s4_interp.jpg', dpi=200)
146.	 
147.	plt.show()	




