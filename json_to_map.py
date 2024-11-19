import json
import numpy as np
import folium
from folium import Polygon
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

# 1. JSON 파일 읽기
with open('6_10_5.json', 'r') as f:
    data = json.load(f)

# 2. 위경도와 농도값을 float으로 변환하여 추출
latitudes = np.array([float(item['latitude']) for item in data]).reshape((100, 100))
longitudes = np.array([float(item['longitude']) for item in data]).reshape((100, 100))
concentration = np.array([float(item['value']) for item in data]).reshape((100, 100))

# 3. 농도값을 로그 스케일로 변환 (0 이하의 값은 작은 값으로 대체)
concentration[concentration <= 0] = 1e-5  # 0 이하 값을 작은 값으로 대체
log_concentration = np.log2(concentration)  # 로그 변환

# 4. 커스텀 색상 설정: 빨간색에서 노란색, 파란색으로
custom_colors = ['blue', 'green', 'yellow', 'red']  # 빨간색, 노란색, 파란색
custom_colormap = colors.LinearSegmentedColormap.from_list('custom_cmap', custom_colors)

# 5. 농도값에 따른 색상 설정 (로그 스케일을 적용한 값으로 컬러맵 설정)
norm = colors.Normalize(vmin=np.min(log_concentration), vmax=np.max(log_concentration))
colormap = cm.ScalarMappable(norm=norm, cmap='coolwarm')  # 'coolwarm' 또는 'RdBu' 사용 가능

# 6. Folium 지도 생성
m = folium.Map(location=[35.1024, 129.1115], zoom_start=14)

# 7. 99x99 그리드 폴리곤 추가 (100번째 인덱스를 넘지 않도록 범위 조정)
for i in range(99):  # 마지막 인덱스는 98까지
    for j in range(99):  # 마지막 인덱스는 98까지
        lat_lon_pairs = [
            [latitudes[i, j], longitudes[i, j]],
            [latitudes[i+1, j], longitudes[i+1, j]],
            [latitudes[i+1, j+1], longitudes[i+1, j+1]],
            [latitudes[i, j+1], longitudes[i, j+1]],
        ]
        color = colors.to_hex(colormap.to_rgba(log_concentration[i, j]))
        # 테두리를 없애기 위해 color='' 또는 color=None 사용
        folium.Polygon(lat_lon_pairs, color=None, fill=True, fill_color=color, fill_opacity=0.6).add_to(m)

# 8. 지도를 HTML 파일로 저장
m.save('map_5.html')