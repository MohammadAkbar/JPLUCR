#!/bin/bash
declare -a StringArray=("colora_32913_17090_008_170903_L090_CX_01_pauli" "congar_11800_18069_009_180923_L090_CX_01_pauli" "cpfear_35303_18065_004_180918_L090_CX_01_pauli" "cscade_26901_11057_002_110804_L090_CX_01_pauli" "evergl_15704_09044_000_090616_L090_CX_01_pauli" "evergl_26301_10053_003_100622_L090_CX_01_pauli" "gulfco_09010_16020_027_160313_L090_CX_01_pauli" "LAmrsh_22201_12051_001_120701_L090_CX_01_pauli" "lngley_31201_09059_003_090813_L090_CX_01_pauli" "neches_16508_17088_012_170901_L090_CX_01_pauli" "NISARP_09811_19071_000_191001_L090_CX_01_pauli" "trinit_14940_17090_000_170903_L090_CX_01_pauli" "vislnd_02701_09059_001_090813_L090_CX_01_pauli")
for i in {$1..$2}; do
	for val in ${StringArray[@]}; do
		echo $val
		mkdir -p /home/jplucr/jplucr/flaskapp/static/alltiles/$val/$i
		gcloud compute scp --recurse --zone us-west2-a afshancloud@instance-1:/home/afshancloud/JPLUCR/flaskapp/static/alltiles/$val/$i /home/jplucr/jplucr/flaskapp/static/alltiles/$val/
	done
done