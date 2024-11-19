from fastkml import kml
import zipfile
import json

def parser(year,month,day,hour,min):
    # KMZ 파일 경로
    kmz_file = f"C:\HarborD\AERPLOT\{year}{month}{day}{hour}{min}.kmz"

    # KMZ 파일을 ZIP으로 열고 내부의 KML 파일 추출
    with zipfile.ZipFile(kmz_file, 'r') as kmz:
        # 파일 리스트 확인 (KML 파일을 찾기)
        file_list = kmz.namelist()
        kml_file = None
        for file_name in file_list:
            if file_name.endswith('.kml'):
                kml_file = kmz.read(file_name)
                break

    # KML 데이터를 파싱
    if kml_file:
        k = kml.KML()
        k.from_string(kml_file)
        
        # KML의 모든 피처 탐색 (재귀적으로 탐색)
        def iterate_features(features):
            for feature in features:
                if isinstance(feature, kml.Document) or isinstance(feature, kml.Folder):
                    # Document 또는 Folder일 경우 재귀적으로 탐색
                    yield from iterate_features(feature.features())
                elif isinstance(feature, kml.Placemark):
                    yield feature

        # 데이터를 저장할 리스트
        data_list = []
        
        # 모든 Placemark 탐색
        for placemark in iterate_features(k.features()):
            if placemark.name:
                name_parts = placemark.name.split('_')
                if len(name_parts) >= 2:
                    id_value = name_parts[0]  # 첫 번째 값 (예: 5652)
                    other_value = name_parts[1]  # 두 번째 값 (예: 523.28922)
                else:
                    continue  # name 형식이 맞지 않으면 건너뛰기

                # <coordinates> 태그에서 경도, 위도 추출
                coordinates = list(placemark.geometry.coords)
                if coordinates:
                    longitude, latitude = coordinates[0][0], coordinates[0][1]

                # JSON 데이터 구조에 맞게 데이터 구성
                # data = {
                #     "id": id_value,
                #     "value": other_value,
                #     "longitude": longitude,
                #     "latitude": latitude
                # }
                
                # GeoJSON 데이터 구조
                data = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [longitude,latitude]
                    },
                    "properties":{
                        "id":id_value,
                        "value":other_value,
                        "timestamp": f"20{year}-{month}-{day}T{hour}:00:00Z"
                    }
                }
                
                # 데이터를 리스트에 추가
                data_list.append(data)

        # id 값을 기준으로 정렬 (숫자 순으로 정렬하기 위해 int로 변환)
        #data_list.sort(key=lambda x: int(x["id"]))
        
        # GeoJSON 형식 변환
        geojson_data ={
            "type": "FeatureCollection",
            "features": data_list
        }

        # # 결과를 JSON 파일로 저장
        # with open(f"{year}{month}{day}{hour}.json", 'w', encoding='utf-8') as json_file:
        #     json.dump(data_list, json_file, ensure_ascii=False, indent=4)

        # print("JSON 파일로 저장이 완료되었습니다.")
        
        # 결과를 GeoJSON 파일로 저장
        with open(f"{year}{month}{day}{hour}{min}.geojson", 'w', encoding='utf-8') as geojson_file:
            json.dump(geojson_data, geojson_file, ensure_ascii=False, indent=4)

        print(f"{year}년 {month}월 {day}일 {hour}시 {min}분의 GeoJSON 파일 변환이 완료되었습니다.")