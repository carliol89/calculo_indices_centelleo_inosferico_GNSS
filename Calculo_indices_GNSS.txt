dll_pll_veml_plot_sample3.m, modificado para calcular índices de centelleo ,  S_4, σ_φ.
1.	% Reads GNSS-SDR Tracking dump binary file using the provided
2.	%  function and plots some internal variables
3.	 
4.	% Javier Arribas, 2011. jarribas(at)cttc.es
5.	% Antonio Ramos,  2018. antonio.ramos(at)cttc.es
6.	% -------------------------------------------------------------------------
7.	%
8.	% GNSS-SDR is a Global Navigation Satellite System software-defined receiver.
9.	% This file is part of GNSS-SDR.
10.	%
11.	% Copyright (C) 2010-2019  (see AUTHORS file for a list of contributors)
12.	% SPDX-License-Identifier: GPL-3.0-or-later
13.	%
14.	% -------------------------------------------------------------------------
15.	%
16.	 
17.	close all;
18.	clear all;
19.	 
20.	if ~exist('dll_pll_veml_read_tracking_dump.m', 'file')
21.	    addpath('./libs')
22.	end
23.	 
24.	samplingFreq = 1999998 ;     %[Hz]
25.	plot_last_outputs=0;%1000;
26.	 
27.	 
28.	channels = 3;   % Number of channels
29.	first_channel = 0;  % Number of the first channel
30.	 
31.	path ='/home/cast/2023-07-19_ionos/';  %% CHANGE THIS PATH
32.	 
33.	for N=1:1:channels
34.	    tracking_log_path = [path 'tracking_ch_' num2str(N+first_channel-1) '.dat'] ; %% CHANGE track_ch_ BY YOUR dump_filename
35.	    GNSS_tracking(N)=dll_pll_veml_read_tracking_dump(tracking_log_path);
36.	end
37.	 
38.	% GNSS-SDR format conversion to MATLAB GPS receiver
39.	 
40.	for N=1:1:channels
41.	    trackResults(N).status = 'T'; %fake track
42.	    if plot_last_outputs>0 && plot_last_outputs<length(GNSS_tracking(N).code_freq_hz)
43.	 
44.	        start_sample=length(GNSS_tracking(N).code_freq_hz)-plot_last_outputs;
45.	    else
46.	        start_sample=1;
47.	    end
48.	    trackResults(N).codeFreq       = GNSS_tracking(N).code_freq_hz(start_sample:end).';
49.	    trackResults(N).carrFreq       = GNSS_tracking(N).carrier_doppler_hz(start_sample:end).';
50.	    trackResults(N).dllDiscr       = GNSS_tracking(N).code_error(start_sample:end).';
51.	    trackResults(N).dllDiscrFilt   = GNSS_tracking(N).code_nco(start_sample:end).';
52.	    trackResults(N).pllDiscr       = GNSS_tracking(N).carr_error(start_sample:end).';
53.	    trackResults(N).pllDiscrFilt   = GNSS_tracking(N).carr_nco(start_sample:end).';
54.	 
55.	    trackResults(N).I_P = GNSS_tracking(N).P(start_sample:end).';
56.	    trackResults(N).Q_P = zeros(1,length(GNSS_tracking(N).P(start_sample:end)));
57.	 
58.	    trackResults(N).I_VE = GNSS_tracking(N).VE(start_sample:end).';
59.	    trackResults(N).I_E = GNSS_tracking(N).E(start_sample:end).';
60.	    trackResults(N).I_L = GNSS_tracking(N).L(start_sample:end).';
61.	    trackResults(N).I_VL = GNSS_tracking(N).VL(start_sample:end).';
62.	    trackResults(N).Q_VE = zeros(1,length(GNSS_tracking(N).VE(start_sample:end)));
63.	    trackResults(N).Q_E = zeros(1,length(GNSS_tracking(N).E(start_sample:end)));
64.	    trackResults(N).Q_L = zeros(1,length(GNSS_tracking(N).L(start_sample:end)));
65.	    trackResults(N).Q_VL = zeros(1,length(GNSS_tracking(N).VL(start_sample:end)));
66.	    trackResults(N).data_I = GNSS_tracking(N).prompt_I(start_sample:end).';
67.	    trackResults(N).data_Q = GNSS_tracking(N).prompt_Q(start_sample:end).';
68.	    trackResults(N).PRN = GNSS_tracking(N).PRN(start_sample:end).';
69.	    trackResults(N).CNo = GNSS_tracking(N).CN0_SNV_dB_Hz(start_sample:end).';
70.	    trackResults(N).prn_start_time_s = GNSS_tracking(N).PRN_start_sample(start_sample:end)/samplingFreq;
71.	    % Use original MATLAB tracking plot function
72.	    settings.numberOfChannels = channels;
73.	end
74.	pkg load control
75.	pkg load io % Se carga el paquete io
76.	disp(unique([trackResults.PRN]));
77.	for j = 1:1:32 % satélites
78.	  cn0{j} = [];
79.	  for i = 1:1:channels % canales
80.	      cn0{j} = horzcat(cn0{j}, trackResults(i).CNo(trackResults(i).PRN == j));
81.	    end
82.	    Cn0_cell{j} = cn0{j};
83.	end
84.	S4_array = [];
85.	for i = 1:1:length(Cn0_cell)
86.	Z=Cn0_cell{i};% Obtiene el array correspondiente a Cn0_cell{i}
87.	P=Z.^2;
88.	suma=sum(P);
89.	n=length(Z);
90.	a=suma/n;
91.	W=(sum(Z)/n);
92.	w=W^2;
93.	S4=sqrt(abs((a-w)/w));
94.	S4_array = horzcat(S4_array, S4);
95.	fprintf('El valor de S4 para el PRN %d es %4f\n', i, S4_array(i));;
96.	end  
97.	dlmwrite('indice_S4_26_07_2023.dat',S4_array, 'delimiter', ' ');
98.	for j = 1:1:32 % satélites
99.	  dataI{j} = [];
100.	  for i = 1:1:channels % canales
101.	      dataI{j} = horzcat(dataI{j}, trackResults(i).data_I(trackResults(i).PRN == j));
102.	  end
103.	  dataI_cell{j}= dataI{j};
104.	end    
105.	for j = 1:1:32 % satélites
106.	  dataQ{j} = [];
107.	  for i = 1:1:channels % canales
108.	      dataQ{j} = horzcat(dataQ{j}, trackResults(i).data_Q(trackResults(i).PRN == j));
109.	  end
110.	   dataQ_cell{j}= dataQ{j};
111.	end
112.	save -mat 'dataQ_cell.mat' dataQ_cell
113.	disp(size(dataQ_cell));
114.	sigmaphi_array = [];
115.	for i = 1:1:length(dataQ_cell)
116.	Q=dataQ_cell{i};
117.	I=dataI_cell{i};
118.	phi = atan2(Q,I);
119.	phi1_abs = abs(phi);
120.	PHI=phi1_abs.^2;
121.	SUMA=sum(PHI);
122.	p=length(PHI);
123.	u=SUMA/p;
124.	sum2=sum(phi1_abs);
125.	Pro2=(sum2/p);
126.	Pro3=Pro2^2;
127.	sigmaphi=sqrt(u-Pro3);
128.	sigmaphi_array= horzcat(sigmaphi_array,sigmaphi);
129.	fprintf('El valor de sigma phi para el PRN %d es %4f\n', i, sigmaphi_array(i));;
130.	end  
131.	dlmwrite('indice_sigma_phi__30_07_2023.dat',sigmaphi_array, 'delimiter', ' ');
 

