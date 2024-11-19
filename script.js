
document.addEventListener("DOMContentLoaded", () => {
  const INITIAL_VIEW_STATE = {
    longitude: 129.1115,
    latitude: 35.1024,
    zoom: 12,
    pitch: 0,
    bearing: 0
  };

  const fileUrls = [];
  const year = '23';
  const month = '07';
  const day = '01';

  for (let hour = 1; hour <= 23; hour++) {
    const formattedHour = String(hour).padStart(2, '0');
    fileUrls.push(`${year}${month}${day}${formattedHour}00.geojson`);
    if(hour!=23){
      fileUrls.push(`${year}${month}${day}${formattedHour}30.geojson`);
    }
  }

  let currentFileIndex = 0;
  let isAnimating = false;
  let animationTimeout;

  // GeoJSON 파일 로드 함수
  async function loadGeoJson(url) {
    const response = await fetch(url);
    return await response.json();
  }

  // Deck 초기화
  const deckgl = new deck.DeckGL({
    container: 'map',
    mapboxApiAccessToken: 'pk.eyJ1IjoiY291bnRyeWJpcmQiLCJhIjoiY20ycTZva25zMHp0NDJpcTkxOTBtOXo1eCJ9.KCwDZLhDsmM0ptAknZeqyw',
    //mapStyle: 'mapbox://styles/mapbox/streets-v12',
    //  mapStyle: 'mapbox://styles/mapbox/satellite-v9',
    // mapStyle: 'mapbox://styles/mapbox/satellite-v9',
    // mapStyle: 'mapbox://styles/mapbox/satellite-v9',
    mapStyle: 'mapbox://styles/mapbox/light-v11',
    initialViewState: INITIAL_VIEW_STATE,
    controller: true,
    layers: []
  });

  //색상 설정 함수
  function getColorByConcentration(concentration) {
    const maxConcentration = 5000;
    const minConcentration = 1;
    if (concentration <= 10) {
      return [0, 0, 0, 0];
    }
    const logValue = Math.log(concentration);
    const logMin = Math.log(minConcentration);
    const logMax = Math.log(maxConcentration);
    const ratio = (logValue - logMin) / (logMax - logMin);
    const red = Math.min(255, Math.floor(ratio * 255));
    const green = Math.min(255, Math.floor((1 - ratio) * 255));
    const blue = 0;
    return [red + 100, green + 30, blue, 180];
  }

  // 시간에 따른 지도 업데이트
  async function updateMap(index) {
    const currentFileUrl = fileUrls[index];
    const hour = currentFileUrl.slice(6,8);
    const min = currentFileUrl.slice(8,10);

    // 시간 정보 표시 업데이트
    document.getElementById('current-time').textContent = `Time: ${year}-${month}-${day} ${hour}:${min}`;

    const data = await loadGeoJson(currentFileUrl);

    const layer = new deck.GeoJsonLayer({
      id: `geojson-layer-${index}`,
      data,
      filled: true,
      pointRadiusMinPixels: 0.05,
      pointRadiusScale: 25,
      getFillColor: d => getColorByConcentration(d.properties.value),
      getLineColor: [0, 0, 0, 0],
    });

    deckgl.setProps({ layers: [layer] });
  }

  // 애니메이션 함수
  async function animateMap() {
    if (!isAnimating) return;

    await updateMap(currentFileIndex);
    const autoslider = document.getElementById('time-slider');
    currentFileIndex = (currentFileIndex + 1) % fileUrls.length;
    autoslider.value=currentFileIndex;
    animationTimeout = setTimeout(animateMap, 500);
  }

  // 애니메이션 토글 함수
  function toggleAnimation() {
    isAnimating = !isAnimating;
    document.getElementById('toggle-animation').textContent = isAnimating ? 'Stop Animation' : 'Start Animation';
    
    if (isAnimating) {
      animateMap();
    } else {
      clearTimeout(animationTimeout);
    }
  }

  // 슬라이더 이벤트 리스너
  document.getElementById('time-slider').addEventListener('input', (event) => {
    currentFileIndex = parseInt(event.target.value, 10);
    updateMap(currentFileIndex);
    
    // 애니메이션 중지 및 버튼 텍스트 업데이트
    if (isAnimating) {
      isAnimating = false;
      clearTimeout(animationTimeout);
      document.getElementById('toggle-animation').textContent = 'Start Animation';
    }
  });

  // 애니메이션 버튼 이벤트 리스너
  document.getElementById('toggle-animation').addEventListener('click', toggleAnimation);

  // 초기 지도 업데이트
  updateMap(currentFileIndex);
});
