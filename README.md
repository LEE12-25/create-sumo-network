# create-sumo-network
행정코드 입력 시 해당 네트워크 데이터 전처리 및 차량 시뮬레이션 실행 모듈



# newton_v0.3.0/csv2xml.py: 경계 부분 유실 문제 반영

v.3.0
1. shp2csv.py: 전국 도로망 데이터를 shp에서 csv로 백업
2. csv2xml.py: 전국 도로망 데이터 csv의 지역을 지정하고 전처리 및 가공하여 sumo에 입력할 xml 파일을 작성 및 저장

<사전작업>

1) newton_v0.3.0 압축폴더를 전달받은 경우, 바탕화면(C:\Users\Desktop)에 저장
2) 새로 폴더 세팅해야 할 경우
./newton_v0.3.0
	csv2xml.py
	/data
		/csv
			code_df.csv # 행정코드 검색용
		/shp
			NOD, EDGE의 shape 파일들
			(.dbf, .prj, .sbn, .sbx, .shp, .shx)
		/xml
			exp.sumocfg(SUMO Configuration File)

- 경로명이 다른 경우,  
	- 아래 1), 5)를 해당 경로로 수정해서 실행
- geopandas 패키지 install 필요
- geo라는 이름의 가상환경 생성 필요
	- 가상환경이름이 geo가 아닐 경우, 아래 2)에 해당 가상환경 이름 바꾸기

======================================================================

<Anaconda Prompt>
1. shp2csv (약 5분 소요)
 - 전체 행정구역 shp파일 csv로 반환: newton_v0.3.0\data\csv에 저장됨

	1) cd C:\Users\Desktop\newton_v0.3.0
	2) activate geo
	3) python shp2csv.py

1. csv2xml (입력 후 약 40초 소요)
 - 지역단위(시도, 시군구, 읍면동) 선택  
 - 특정 행정코드 검색: 원하는 시군구의 명칭을 입력하세요(ex. 안양)
 - 행정지역코드 입력: 원하는 지역의 행정지역코드를 공백으로 구분하여 입력하세요. ex) 안양시: 31041 31042
 - plain.xml 저장: newton_v0.3.0\data\xml에 저장됨

	4) python csv2xml.py

2. 네트워크 파일 생성 및 sumo 실행: 

	5) cd C:\Users\Desktop\newton_v0.3.0\data\xml
	6) netconvert -n exp.nod.xml -e exp.edg.xml -x exp.con.xml -t exp.typ.xml -o exp.net.xml
	7) sumo-gui -n exp.net.xml
