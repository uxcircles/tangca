/* Tang & Co map: MapLibre + OpenFreeMap vector tiles in the firm's colours, two offices.
   Walking routes come from routing.openstreetmap.de and are baked into #map-data. */
(() => {
  const C = {
    land: '#efede8',
    building: '#e2ded5',
    buildingLine: '#d6cfc3',
    park: '#d9e0cc',
    water: '#c6d2dc',
    road: '#ffffff',
    roadCase: '#dcd7cd',
    major: '#ffffff',
    majorCase: '#cdbf9f',
    rail: '#8a93a0',
    label: '#1b2a3f',
    labelSoft: '#4b5563',
    halo: '#efede8',
    route: '#8a7550',
    routeCase: '#1b2a3f',
  };
  const name = ['coalesce', ['get', 'name:en'], ['get', 'name_en'], ['get', 'name']];
  const width = (a, b, c) => ['interpolate', ['exponential', 1.6], ['zoom'], 13, a, 16, b, 18, c];
  const major = ['match', ['get', 'class'], ['motorway', 'trunk', 'primary', 'secondary'], true, false];
  const minor = ['match', ['get', 'class'], ['tertiary', 'minor', 'service', 'street', 'residential'], true, false];

  const style = {
    version: 8,
    glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
    sources: { omt: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' } },
    layers: [
      { id: 'land', type: 'background', paint: { 'background-color': C.land } },
      { id: 'park', type: 'fill', source: 'omt', 'source-layer': 'park', paint: { 'fill-color': C.park } },
      { id: 'green', type: 'fill', source: 'omt', 'source-layer': 'landuse', filter: ['match', ['get', 'class'], ['park', 'grass', 'cemetery', 'pitch', 'playground'], true, false], paint: { 'fill-color': C.park } },
      { id: 'water', type: 'fill', source: 'omt', 'source-layer': 'water', paint: { 'fill-color': C.water } },
      { id: 'waterway', type: 'line', source: 'omt', 'source-layer': 'waterway', paint: { 'line-color': C.water, 'line-width': ['interpolate', ['linear'], ['zoom'], 13, 1.5, 18, 8] } },
      { id: 'building', type: 'fill', source: 'omt', 'source-layer': 'building', minzoom: 13, paint: { 'fill-color': C.building, 'fill-outline-color': C.buildingLine } },
      { id: 'rail', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: ['match', ['get', 'class'], ['rail', 'transit'], true, false], paint: { 'line-color': C.rail, 'line-width': 1.4, 'line-dasharray': [3, 2] } },
      { id: 'road-case', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: minor, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.roadCase, 'line-width': width(1.5, 6, 20) } },
      { id: 'major-case', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: major, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.majorCase, 'line-width': width(3, 10, 30) } },
      { id: 'road', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: minor, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.road, 'line-width': width(1, 4.5, 17) } },
      { id: 'major', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: major, layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.major, 'line-width': width(2, 8, 27) } },
      { id: 'road-label', type: 'symbol', source: 'omt', 'source-layer': 'transportation_name', minzoom: 15, layout: { 'symbol-placement': 'line', 'text-field': name, 'text-font': ['Noto Sans Regular'], 'text-size': 11 }, paint: { 'text-color': C.labelSoft, 'text-halo-color': C.halo, 'text-halo-width': 1.4 } },
      { id: 'area-label', type: 'symbol', source: 'omt', 'source-layer': 'place', filter: ['match', ['get', 'class'], ['suburb', 'quarter', 'neighbourhood'], true, false], layout: { 'text-field': ['upcase', name], 'text-font': ['Noto Sans Bold'], 'text-size': 11, 'text-letter-spacing': 0.18, 'text-max-width': 8 }, paint: { 'text-color': C.labelSoft, 'text-halo-color': C.halo, 'text-halo-width': 1.4 } },
    ],
  };

  const el = (html, cls) => { const d = document.createElement('div'); d.className = cls; d.innerHTML = html; return d; };

  window.tcMap = (box) => {
    const data = JSON.parse(document.getElementById('map-data').textContent);
    const { maplibregl } = window;
    const holder = document.createElement('div');
    holder.className = 'mapbox';
    box.appendChild(holder);
    const phone = window.matchMedia('(max-width: 760px)').matches;
    const first = data.offices.edinburgh;
    const map = new maplibregl.Map({
      container: holder, style, center: first.home, zoom: 15, maxZoom: 18, minZoom: 11,
      dragRotate: false, pitchWithRotate: false, cooperativeGestures: true, attributionControl: { compact: true },
    });
    map.touchZoomRotate.disableRotation();
    if (!phone) map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-left');

    let current = 'edinburgh';
    let touched = false;
    const boundsFor = (o) => { const b = new maplibregl.LngLatBounds(o.home, o.home); o.routes.forEach((r) => r.coords.forEach((c) => b.extend(c))); return b; };
    const pad = phone ? { top: 60, bottom: 40, left: 30, right: 30 } : { top: 70, bottom: 50, left: 80, right: 80 };
    const fit = (dur = 0) => map.fitBounds(boundsFor(data.offices[current]), { padding: pad, duration: dur, maxZoom: 16 });
    fit();
    map.on('dragstart', () => { touched = true; });
    map.on('zoomstart', (e) => { if (e.originalEvent) touched = true; });
    window.addEventListener('resize', () => { if (!touched) fit(); });

    map.on('load', () => {
      const feats = [];
      Object.values(data.offices).forEach((o) => o.routes.forEach((r) => feats.push({ type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: r.coords } })));
      map.addSource('routes', { type: 'geojson', data: { type: 'FeatureCollection', features: feats } });
      map.addLayer({ id: 'route-case', type: 'line', source: 'routes', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.routeCase, 'line-width': 6, 'line-opacity': 0.2 } });
      map.addLayer({ id: 'route', type: 'line', source: 'routes', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': C.route, 'line-width': 3.5, 'line-dasharray': [1.2, 1.2] } });
      if (phone) holder.querySelectorAll('.maplibregl-compact-show').forEach((a) => a.classList.remove('maplibregl-compact-show'));
    });

    Object.values(data.offices).forEach((o) => {
      o.routes.forEach((r) => {
        const east = r.start[0] > o.home[0];
        const nm = phone ? r.short : r.name;
        const html = east ? `<small class="t">${nm} · ${r.min}′</small><span class="dot"></span>` : `<span class="dot"></span><small class="t">${nm} · ${r.min}′</small>`;
        new maplibregl.Marker({ element: el(html, 'map-stn'), anchor: east ? 'right' : 'left', offset: [east ? 7 : -7, 0] }).setLngLat(r.start).addTo(map);
      });
      new maplibregl.Marker({ element: el(`<span class="pin"><img src="${data.mark}" alt=""></span><small class="pin-label">${o.label}</small>`, 'map-pin'), anchor: 'top', offset: [0, -23] })
        .setLngLat(o.home).addTo(map);
    });

    document.querySelectorAll('.office-tabs [data-office]').forEach((b) => b.addEventListener('click', () => {
      current = b.dataset.office; touched = false;
      document.querySelectorAll('.office-tabs [data-office]').forEach((x) => x.setAttribute('aria-selected', x === b));
      fit(800);
    }));
    return map;
  };
})();
