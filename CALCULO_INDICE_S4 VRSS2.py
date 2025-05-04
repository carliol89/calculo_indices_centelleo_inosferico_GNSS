CALCULO_INDICE_S4 USANDO DATOS DEL SATELITE SUCRE  
S4_VRSS-2.py
1.	#!/usr/bin/python3
2.	# https://github.com/keenerd/rtl-sdr-misc/blob/master/heatmap/raw_iq.py
3.	import numpy as np
4.	import math
5.	from pylab import *
6.	 
7.	# samples = np.fromfile('S-Band_10s_2M_1.raw', np.complex64)
8.	 
9.	#file = 'S-Band_10s_2M_1.raw'
10.	 
11.	print ('valores del indice S4 para el pase de las 11 pm')
12.	 
13.	file ='/home/cast/parteaa'
14.	 
15.	def byte_reader(path):
16.	    raw =np.fromfile(path, np.uint8).astype(np.float16)
17.	    raw-=(2**7-1)
18.	    raw/=2**7
19.	    return raw[0::2]+1j*raw[1::2]
20.	
21.	sample1 = byte_reader(file) 
22.	sample= np.array_split(sample1, len(sample1) //8192000.0 ) 
23.	# crea una lista de subarrays # crea una lista vacía para guardar los resultados
24.	# usa la función len para obtener la longitud de la lista sample
25.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
26.	  sample2=np.square(np.square(sample[i]))
27.	  p=sum(abs(sample2))/len(sample[i])
28.	  sample3=np.square(sample[i])
29.	  n=float(sum(abs(sample3))/len(sample[i]))
30.	  S4 =sqrt((p-n)/n)
31.	  print('El valor de s4 para el array', i, S4)
32.	 
33.	file ='/home/cast/parteab'
34.	sample1 = byte_reader(file)
35.	 
36.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
37.	  sample2=np.square(np.square(sample[i]))
38.	  p=sum(abs(sample2))/len(sample[i])
39.	  sample3=np.square(sample[i])
40.	  n=float(sum(abs(sample3))/len(sample[i]))
41.	  S4 =sqrt((p-n)/n)
42.	  print('El valor de s4 para el array', i+11, S4)
43.	 
44.	file ='/home/cast/parteac'
45.	sample1 = byte_reader(file)
46.	 
47.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
48.	  sample2=np.square(np.square(sample[i]))
49.	  p=sum(abs(sample2))/len(sample[i])
50.	  sample3=np.square(sample[i])
51.	  n=float(sum(abs(sample3))/len(sample[i]))
52.	  S4 =sqrt((p-n)/n)
53.	  print('El valor de s4 para el array', i+23, S4)
54.	 
55.	file ='/home/cast/partead'  
56.	sample1 = byte_reader(file)
57.	 
58.	   
59.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
60.	  sample2=np.square(np.square(sample[i]))
61.	  p=sum(abs(sample2))/len(sample[i])
62.	  sample3=np.square(sample[i])
63.	  n=float(sum(abs(sample3))/len(sample[i]))
64.	  S4 =sqrt((p-n)/n)
65.	  print('El valor de s4 para el array', i+34, S4)
66.	 
67.	file ='/home/cast/parteaf'    
68.	sample1 = byte_reader(file)
69.	 
70.	 
71.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
72.	  sample2=np.square(np.square(sample[i]))
73.	  p=sum(abs(sample2))/len(sample[i])
74.	  sample3=np.square(sample[i])
75.	  n=float(sum(abs(sample3))/len(sample[i]))
76.	  S4 =sqrt((p-n)/n)
77.	  print('El valor de s4 para el array', i+45, S4)
78.	   
79.	file ='/home/cast/parteae'
80.	sample1 = byte_reader(file)
81.	       
82.	 
83.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
84.	  sample2=np.square(np.square(sample[i]))
85.	  p=sum(abs(sample2))/len(sample[i])
86.	  sample3=np.square(sample[i])
87.	  n=float(sum(abs(sample3))/len(sample[i]))
88.	  S4 =sqrt((p-n)/n)
89.	  print('El valor de s4 para el array', i+57, S4)  
90.	 
91.	file ='/home/cast/parteaf'
92.	sample1 = byte_reader(file)
93.	   
94.	 
95.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
96.	  sample2=np.square(np.square(sample[i]))
97.	  p=sum(abs(sample2))/len(sample[i])
98.	  sample3=np.square(sample[i])
99.	  n=float(sum(abs(sample3))/len(sample[i]))
100.	  S4 =sqrt((p-n)/n)
101.	  print('El valor de s4 para el array', i+68, S4)
102.	 
103.	file ='/home/cast/parteag'
104.	sample1 = byte_reader(file)
105.	sample= np.array_split(sample1, len(sample1) //6144000.0) 
106.	
107.	for i in range(len(sample)): # recorre la lista y muestra cada subarray
108.	  sample2=np.square(np.square(sample[i]))
109.	  p=sum(abs(sample2))/len(sample[i])
110.	  sample3=np.square(sample[i])
111.	  n=float(sum(abs(sample3))/len(sample[i]))
112.	  S4 =sqrt((p-n)/n)
113.	  print('El valor de s4 para el array', i+80, S4)    
 
