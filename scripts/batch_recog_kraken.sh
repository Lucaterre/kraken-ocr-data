# -*- coding: UTF-8 -*-
# Author : Lucas Terriel (https://github.com/Lucaterre), Jean-Damien Généro
# Date : 2 octobre 2020

train_files_IMAGE=*.tiff # images'extension
# train_directory_OUTPUT="./output/" # output directory
model=model_best.mlmodel # MODEL

page_number=178
for image in $train_files_IMAGE;
	do 
	  page_number=$(($page_number+1))
	  kraken -i $image 'output_'$page_number'.txt' binarize segment ocr -m $model 
	  # echo 'output_'$page_number'.txt'
	done