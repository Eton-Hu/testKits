# Introduction

Those are the tool kits for kaggle golf compitation https://www.kaggle.com/competitions/golfdetection

## label extractor
Labels detected by YOLOv5 are often recored as '.txt' file. which in the format of:
TargetName1 confidence x_coordinate y_coordinate w h
TargetName2 confidence x_coordinate y_coordinate w h
...
The function of label extractor is:
1. Extract labels from .txt files to a .csv file which can be a submission for kaggle compitation.
2. Enhancing the confidence (if nessasary)

## renamer
A .bat Windows script for renaming the lable files to the format that can be recognized by YOLOv5 algorithm
