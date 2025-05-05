CÓDIGO EMPLEADO PARA CALCULAR LA UBICACIÓN DE LOS SATÉLITES EN COORDENADAS POLARES
gps_pos_orbits.py,
1.	#!/usr/bin/python3
2.	import astropy.coordinates
3.	import astropy.time
4.	import sp3
5.	import pandas as pd
6.	import numpy as np
7.	import matplotlib.pyplot as plt
8.	from datetime import datetime, timedelta
9.	from matplotlib.pyplot import rc, grid, Figura, plot, rcParams, savefig
10.	 
11.	# https://stackoverflow.com/questions/18721762/matplotlib-polar-plot-is-not-plotting-where-it-should
12.	 
13.	lon = -66.83675
14.	lat = 10.485988
15.	 
16.	date = '2023-07-19T16:00:00'
17.	delta = 60
18.	date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
19.	time_range = pd.date_range(date, date + timedelta(minutes=delta), freq='5min')
20.	 
21.	date = time_range[0]
22.	 
23.	def altaz(sp3id, time_range, lon, lat):
24.	    print('Satellite:', sp3id)
25.	    sp3.cddis.username = "xxxx"
26.	    sp3.cddis.password = "xxxxxxx"
27.	    sp3_altaz = sp3.altaz_standard_atmosphere(
28.	        id=sp3.Sp3Id(sp3id), obstime=astropy.time.Time(time_range),
29.	        location=astropy.coordinates.EarthLocation.from_geodetic(lon=lon, lat=lat, height=0),
30.	        download_directory="sp3_cache")
31.	    pos = pd.DataFrame({'az': sp3_altaz.az.value, 'el': sp3_altaz.alt.value}, index=sp3_altaz.obstime.value)
32.	    pos.index = pos.index.rename('Time')        
33.	    azimuth   = np.array(np.radians(pos['az'].to_list()))
34.	    elevation = np.array(pos['el'].to_list())
35.	    return azimuth, elevation
36.	   
37.	def plot_arrow(azimuth, elevation, color, width, label):
38.	    ax.plot(azimuth, elevation, color=color, linewidth=width, label=label)
39.	    legend = ax.legend(loc='best', shadow=True, fontsize='7')
40.	    x1 = (90-elevation[-3])*np.cos(azimuth[-3])
41.	    y1 = (90-elevation[-3])*np.sin(azimuth[-3])
42.	x2 = (90-elevation[-2])*np.cos(azimuth[-2])
43.	y2 = (90-elevation[-2])*np.sin(azimuth[-2])
44.	theta = np.radians(90) - np.arctan2(y2-y1, x2-x1)
45.	ax.quiver(azimuth[-1], elevation[-1], np.cos(theta), np.sin(theta), color=color, scale=30, width=0.01*width)
46.	     
47.	 
48.	sats = {}
49.	 
50.	 
51.	rc('grid', color='#00edff', linewidth=1, linestyle='-')    
52.	rc('xtick', labelsize=15)
53.	rc('ytick', labelsize=15)
54.	width, height = rcParams['Figura.figsize']
55.	size = 1.2 * min(width, height)
56.	fig = Figura(figsize=(size, size), facecolor=(0.5,0.5,0.5))
57.	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, facecolor='#000040')
58.	ax.set_theta_zero_location('N')
59.	ax.set_theta_direction(-1)
60.	ax.set_rlim(bottom=90, top=0)
61.	ax.set_rlabel_position(-22.5)
62.	ax.tick_params(axis='x', colors='white', labelsize=15)
63.	ax.tick_params(axis='y', colors='white', labelsize=10)
64.	ax.set_title("GPS satellites / {} UTC + {} min".format(date, delta), va='bottom')
65.	ax.set_yticks(range(0, 90, 10))
66.	ax.grid(True)
67.	 
68.	for i in range(1, 33):
69.	    prn = 'G{:0>2}'.format(i)
70.	    if not prn in ['G07', 'G12', 'G24']:
71.	        az, el = altaz(prn, time_range, lon, lat)
72.	    if el[0] > 0:
73.	        sats[prn] = {'az': az[0], 'el': el[0]}
74.	        ax.annotate(prn, xy=(sats[prn]['az'], sats[prn]['el']),
75.	                    bbox=dict(boxstyle="round", fc = '#ff0000', alpha = 0.7),
76.	                    horizontalalignment='center', verticalalignment='bottom')
77.	        plot_arrow(az, el, 'red', 1, '')  
78.	 
79.	plt.savefig('gps_sats.jpg', dpi=200)
80.	plt.show()
 







