# 1) cd C:\Users\Desktop\newton_v0.3
# 2) python csv2xml.py


import numpy as np
import pandas as pd
pd.set_option('max_rows', 3000)


file_path = './'

print('1. 도로망 데이터 csv 불러오기')
print('      * csv 로딩 중...')
# 00. 불러오기

nod = pd.read_csv('./data/csv/nod.csv')
edg = pd.read_csv('./data/csv/edg.csv')
turn = pd.read_csv('./data/csv/turn.csv')
print('nod.shape: ',nod.shape)
print('edg.shape: ',edg.shape)
print('turn.shape: ',turn.shape)
print('\n      * 완료!\n')


code_path = './data/csv/code_df.csv'
code_csv = pd.read_csv(code_path)


# 01. 행정코드 검색/입력
print('2. 행정코드 검색/입력하기')
지역단위 = input(str('      * 원하는 지역단위의 번호를 입력하세요.\n 1. 시/도 (ex. 서울특별시, 경기도) \n 2. 시군구(ex. 안양시 동안구, 성동구) \n 3. 읍면동(ex. 성수동)\n'))

if 지역단위 =='1':
    # 1. 시/도
    시도명칭 = input(str('      * 원하는 시/도의 명칭을 입력하세요:'))
    while 시도명칭 == '' :
        시도명칭 = input(str('                                                                                   * 원하는 시/도 명칭을 입력하세요(ex. 서울):'))
    print(code_csv[code_csv['시도명칭'].str.contains(시도명칭)][['시도명칭', '시도코드']].value_counts())

    code = list(map(str, input('\n      * 원하는 지역의 code를 공백으로 구분하여 입력하세요. ex) 서울: 11\n').split()))
    while len(code) == 0 :
        code = list(map(str, input('\n      * 원하는 지역의 code를 공백으로 구분하여 입력하세요. ex) 서울: 11\n').split()))

    
elif 지역단위 =='2':
    # 2. 시군구
    시군구명칭 = input(str('      * 원하는 시군구의 명칭을 입력하세요. ex) 안양\n'))
    while 시군구명칭 == '' :
        시군구명칭 = input(str('      * 원하는 시군구의 명칭을 입력하세요. ex) 안양\n'))
    print(code_csv[code_csv['시군구명칭'].str.contains(시군구명칭)][['시군구명칭', '시군구코드']].value_counts())

    code = list(map(str, input('\n      * 원하는 지역의 code를 공백으로 구분하여 입력하세요. ex) 안양시: 31041 31042\n').split()))
    while len(code) == 0 :
        code = list(map(str, input('\n      * 원하는 지역의 code를 공백으로 구분하여 입력하세요. ex) 안양시: 31041 31042\n').split()))

elif 지역단위 == '3':
    # 3. 읍면동
    읍면동명칭 = input(str('      * 원하는 읍면동의 명칭을 입력하세요. ex) 성수\n'))
    while 읍면동명칭 == '' :
        읍면동명칭 = input(str('      * 원하는 읍면동의 명칭을 입력하세요. ex) 성수: 1104065 1104066 1104067 1104068\n'))
    print(code_csv[code_csv['읍면동명칭'].str.contains(읍면동명칭)][['읍면동명칭', '읍면동코드']].value_counts())

    code = list(map(str, input('\n      * 원하는 지역의 code를 공백으로 구분하여 입력하세요.\n').split()))
    while len(code) == 0 :
        code = list(map(str, input('\n      * 원하는 지역의 code를 공백으로 구분하여 입력하세요.\n').split()))

        
# 경계 반복 
print('\n3. 해당 행정구역의 데이터만 추출하기')
iter_num = int(input('      * 경계 부근 도로망을 반복 확장할 횟수를 1이상의 정수로 입력하세요. ex) 5 \n'))
행정지역_nod = nod[nod['DIST_ID2'].isin(list(map(int, code)))] # 2217
행정지역_edge = edg[edg['UP_FROM_NO'].isin(행정지역_nod['NODE_ID']) & edg['UP_TO_NODE'].isin(행정지역_nod['NODE_ID'])] 
행정지역_turn = turn[turn['IN_LINK'].isin(행정지역_edge['LINK_ID']) | turn['OUT_LINK'].isin(행정지역_edge['LINK_ID'])]  
print('\n      - 반복 확장 전 행정지역의 nod rows 수:',행정지역_nod.shape[0])
print('      - 반복 확장 전 행정지역의 edg rows 수:',행정지역_edge.shape[0])
print('      - 반복 확장 전 행정지역의 turn rows 수:',행정지역_turn.shape[0],'\n')

for iter in range(iter_num):
    행정지역_edge = edg[edg['UP_FROM_NO'].isin(행정지역_nod['NODE_ID']) | edg['UP_TO_NODE'].isin(행정지역_nod['NODE_ID'])]
    target_node_id =  list(set((list(행정지역_edge['UP_FROM_NO']) + list(행정지역_edge['UP_TO_NODE'])))) 
    행정지역_nod = nod[nod['NODE_ID'].isin(target_node_id)]
    print('---------------')
    print('반복 확장',iter+1,'회차')
    print('nod rows',행정지역_nod.shape[0])
    print('edg rows',행정지역_edge.shape[0],'\n')

print('---------------')
print('      - 경계 반복 확장 후 행정지역의 nod rows 수:',행정지역_nod.shape[0])
print('      - 경계 반복 확장 후 행정지역의 edg rows 수:',행정지역_edge.shape[0])
print('      - 경계 반복 확장 후 행정지역의 turn rows 수: ',행정지역_turn.shape[0],'\n')


# 02. writing xml 

# -- 02-1. nod
print('4. xml 파일 작성')
print("      writing exp.nod xml...")

행정지역_nod.reset_index(drop=True, inplace = True)
node_type=[]
for i2 in range(len(행정지역_nod['TRA_LIGHT'])): # (0, 2217)
    if 행정지역_nod['TRA_LIGHT'][i2] == 0:
        tll = "priority"
        node_type.append(tll)
    else:
        tll = "traffic_light"
        node_type.append(tll)


f = open(file_path+'/data/xml/exp.nod.xml', 'w')
# f = open('C:/Users/Desktop/newton_v0.3/data/xml/exp.nod.xml', 'w')

f.write('<nodes>\n')
for i in range(len(행정지역_nod['NODE_ID'])): 
    node_id =행정지역_nod['NODE_ID'][i]
    X =행정지역_nod['X'][i]
    Y =행정지역_nod['Y'][i]
    tlType="actuated"
    tlLayout="incoming"
#     keepClear: keepClear="t" keepClear="f"
    node_type_ = node_type[i]
    f.write(f'  <node id="{node_id}" x="{X}" y="{Y}" type="{node_type_}" tlType="{tlType}" tlLayout="{tlLayout}"/>\n')
f.write('</nodes>')

f.close()
print("      xml 폴더에 exp.nod.xml 저장 완료!!!")

# -- 02-2. edg, typ
print("      writing exp.edg,typ xml...")

행정지역_edge.reset_index(drop=True, inplace = True)

# geometry 가공
geo_mod_list = []
for j in range(len(행정지역_edge['geometry'])):
    geo = 행정지역_edge['geometry'][j]
    geo_mod = geo.replace("LINESTRING (", "").replace(")", "").replace(' ',',').replace(',,',' ')
    geo_mod_list.append(geo_mod)

행정지역_edge['geometry']=geo_mod_list

# 최대속도 50으로 대체
행정지역_edge['speed_fill0'] = 행정지역_edge['MAX_SPD'].replace(0, np.NaN)
행정지역_edge['speed_fill0'] = 행정지역_edge['speed_fill0'].fillna(50)

# up 01 붙임
linkid_str=행정지역_edge['LINK_ID'].astype(str)
new_up_link_id = []

for k in range(len(행정지역_edge['LINK_ID'])): #2785
            up_link_id = ''.join([linkid_str[k],'01'])
            new_up_link_id.append(up_link_id) # link_id 구현

#xml 변수명으로 변경
up_df= 행정지역_edge.copy()
up_df['id'] = new_up_link_id
up_df['from'] = up_df['UP_FROM_NO']
up_df['to'] = up_df['UP_TO_NODE']
up_df['shape']= up_df['geometry']

# typ.xml 변수들 ==============================================================

type_id = []
for k3 in range(len(행정지역_edge['LINK_ID'])): #558
            up_df_type_id = ''.join([new_up_link_id[k3],'_type'])
            type_id.append(up_df_type_id) # link_id 구현
up_df['type_id']=type_id         
up_df['numlanes'] = up_df['UP_LANES']
up_df['speed'] = up_df['speed_fill0']/3.6
up_df['width'] = 3.5


# down 02 붙임
행정지역_edge_down =행정지역_edge[['LINK_ID', 'DOWN_FROM_','DOWN_TO_NO', 'geometry', 'DOWN_LANES', 'speed_fill0']]#추가 필요
행정지역_edge_down = 행정지역_edge_down[행정지역_edge_down['DOWN_FROM_'].notna()]
행정지역_edge_down['LINK_ID'] = 행정지역_edge_down['LINK_ID'].astype(str)
행정지역_edge_down.reset_index(drop=True, inplace = True)


linkid_str_down = 행정지역_edge_down['LINK_ID'].astype(str) 
new_down_link_id = []

for k2 in range(len(linkid_str_down)): 
    dw_link_id = ''.join([linkid_str_down[k2],'02'])
    new_down_link_id.append(dw_link_id) # link_id 구현
            


# down geometry 순서 reverse
geometry_new = []
for k5 in range(len(linkid_str_down)):
    geo_split = 행정지역_edge_down['geometry'].str.split(' ')
    geo_idx_reverse = list(reversed(geo_split[k5]))
    geo_join = ' '.join(geo_idx_reverse)
    geometry_new.append(geo_join)


down_df= 행정지역_edge_down.copy()

# edg.xml 변수들 ==============================================================
# edge id="47870004301" 
# from="222099" to="222100" 
# shape="305492.5192,547043.7358 305395.3917,547170.4232" 
# type="47870004301_type"
down_df['id'] = new_down_link_id
down_df['from'] = down_df['DOWN_FROM_']
down_df['to'] = down_df['DOWN_TO_NO']
down_df['shape']= geometry_new


# typ.xml 변수 ==============================================================
# type id="47870004301_type" 
# numLanes="1" 
# priority="2" 
# speed="16.6666666666667"

type_id_dw = []
for k3 in range(len(행정지역_edge_down['LINK_ID'])): #558
            down_df_type_id = ''.join([new_down_link_id[k3],'_type'])
            type_id_dw.append(down_df_type_id) # link_id 구현
down_df['type_id']=type_id_dw

            
down_df['numlanes'] = down_df['DOWN_LANES']
down_df['speed'] = down_df['speed_fill0']/3.6
down_df['width'] = 3.5


down_edge_df=down_df.loc[:, "id" :]
down_edge_df = down_edge_df[['id','from', 'to','speed', 'width', 'type_id', 'shape', 'numlanes']]
up_edge_df = up_df[['id','from', 'to','speed','width', 'type_id', 'shape', 'numlanes']]


edge = pd.concat([up_edge_df, down_edge_df]).sort_values(by=['id'])
edge[['from', 'to']] = edge[['from', 'to']].astype(int).astype(str)

edge.reset_index(drop=True, inplace = True)



f = open(file_path+'/data/xml/exp.edg.xml', 'w')
# f = open('C:/Users/Desktop/newton_v0.3/data/xml/exp.edg.xml', 'w')

f.write('<edges>\n')
for k4 in range(len(edge['id'])): # 5036
    edge_id_ = edge['id'][k4]
    from_ = edge['from'][k4]
    to = edge['to'][k4]
    shape = edge['shape'][k4]
    type_id = edge['type_id'][k4]
    f.write(f'  <edge id="{edge_id_}" from="{from_}" to="{to}" shape = "{shape}" type="{type_id}"/>\n')
f.write('</edges>')

f.close()

#typ
f = open(file_path+'/data/xml/exp.typ.xml', 'w')
# f = open('C:/Users/Desktop/newton_v0.3/data/xml/exp.typ.xml', 'w')


# write edg.xml
f.write('<types>\n')
for k4 in range(len(edge['id'])): # 5036
    type_id = edge['type_id'][k4]
    numLanes = edge['numlanes'][k4]
    speed = edge['speed'][k4]
    f.write(f'  <type id="{type_id}" numLanes="{numLanes}" speed="{speed}"/>\n')
f.write('</types>')

f.close()

print("      xml 폴더에 exp.edg.xml, exp.typ.xml 저장 완료!!!")


print("      writing exp.con xml...")

turn.reset_index(drop=True, inplace = True)
turn['NODE_ID'] = turn['NODE_ID'].astype(str)
turn['IN_LINK']=turn['IN_LINK'].astype(str)
turn['OUT_LINK']=turn['OUT_LINK'].astype(str)
행정지역_edge['LINK_ID']=행정지역_edge['LINK_ID'].astype(str)

# filter
target_idx1 = np.array(turn['IN_LINK'].isin(행정지역_edge['LINK_ID']))
target_idx2 = np.array(turn['OUT_LINK'].isin(행정지역_edge['LINK_ID']))
turn = turn[target_idx1 & target_idx2]


new_link_id=[]
for i in range(len(edge['id'])):
    new_link_id.append(edge['id'].astype(str)[i][0:9])
edge['link_id']=new_link_id



turn.reset_index(drop=True, inplace = True)

# from, to
from_list = []
to_list = []

for i in range(len(turn['IN_LINK'])):
    sub_turn = turn.loc[i] 

    node_id = sub_turn['NODE_ID']
    in_link = sub_turn['IN_LINK']
    out_link = sub_turn['OUT_LINK']

    idx = edge['to'] == node_id
    sub = edge[idx]
    idx2 = sub['link_id'] == in_link
    _from = sub[idx2]["id"]

    idx = edge['from'] == node_id
    sub = edge[idx]
    idx2 = sub['link_id'] == out_link
    _to = sub[idx2]["id"]

    from_list.append(_from)
    to_list.append(_to)
    
from_list = []
to_list = []

for i in range(len(turn['IN_LINK'])):

    node_id = turn.loc[i]['NODE_ID']
    in_link = turn.loc[i]['IN_LINK']
    out_link = turn.loc[i]['OUT_LINK']

    sub_in = edge[edge['to'] == node_id]
    idx2_in = sub_in['link_id'] == in_link
    _from = sub_in[idx2_in]["id"]

    sub_out = edge[edge['from'] == node_id]
    idx2_out = sub_out['link_id'] == out_link
    _to = sub_out[idx2_out]["id"]

    from_list.append(_from)
    to_list.append(_to)
    
    from_list[i]
    
to_list_2 = []
for i in range(len(turn['IN_LINK'])): #7780
    to_list[i].values
    to_list_=list(to_list[i])
    for val in to_list_:
        to_list_2.append(val)
    len(to_list_2)
        
from_list_2 = []
for i in range(len(turn['IN_LINK'])):
    from_list[i].values
    from_list_=list(from_list[i])
    for val in from_list_:
        from_list_2.append(val)


# con.xml
f = open(file_path+'/data/xml/exp.con.xml', 'w')
# f = open('C:/Users/Desktop/newton_v0.3/data/xml/exp.con.xml', 'w')

# write con.xml
f.write('<connections>\n')
for i in range(len(from_list_2)):
    from_ = from_list_2[i]
    to_ = to_list_2[i]
    f.write(f'  <connection from="{from_}" to="{to_}"/>\n')
f.write('</connections>')

f.close()

print("      xml 폴더에 exp.con.xml 저장 완료!!!")

print('\n5. exp.net.xml 파일 생성 및 SUMO 시뮬레이터 실행 \n')
print('Anaconda Prompt 창에 아래 코드를 차례로 입력하세요. \n')
print('해당 지역 도로망 데이터의 Sumo 시뮬레이터가 실행됩니다. \n')
print('****************')
print(r'cd C:\Users\Desktop\newton_v0.3.0\data\xml (newton_v0.3 상위 path가 다를 경우 수정 필요)')
print('netconvert -n exp.nod.xml -e exp.edg.xml -x exp.con.xml -t exp.typ.xml -o exp.net.xml')
print('sumo-gui -n exp.net.xml\n')
print('****************')