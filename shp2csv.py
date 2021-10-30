#1. 라이브러리 불러오기
print("\n                                                                                    * * *  import libraries...")

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
import geopandas as gpd
import matplotlib.pyplot as plt
print("                                                                                    * * *  import 완료")

#2. shape 파일 불러오기
nod_path = './data/shp/AD0102.shp'
edg_path = "./data/shp/AD0022.shp"
turn_path = './data/shp/TURNINFO.shp'


print("\n                                                                                    * * *  Node shape 파일 불러오는중...")
nod = gpd.read_file(nod_path)
print("                                                                                    * * *  Done!")

print("\n                                                                                    * * *  Edge shape 파일 불러오는중...")
edg = gpd.read_file(edg_path)
print("                                                                                    * * *  Done!")

print("\n                                                                                    * * *  TURNINFO shape 파일 불러오는중...")
turn = gpd.read_file(turn_path)
print("                                                                                    * * *  Done!")

print("                                                                                    * * *  shape 파일 read 완료 ")


#3. csv로 백업하기
print("\n                                                                                    * * *  Node csv 파일 저장 중...")
nod.to_csv('./data/csv/nod.csv', index = False)
print(nod.shape, "                                                                                    * * *  Done!")


print("\n                                                                                    * * *  Edge csv 파일 저장 중...")
edg.to_csv('./data/csv/edg.csv', index = False)
print(edg.shape, "                                                                                    * * *  Done!")


print("\n                                                                                    * * *  TURNINFO csv 파일 저장 중...")
turn.to_csv('./data/csv/turn.csv', index = False)
print(turn.shape, "                                                                                    * * *  Done!")


print("                                                                                    * * *  경로에 csv 파일 저장 완료 ")