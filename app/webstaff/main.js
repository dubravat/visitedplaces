function isWebGLSupported() {
    if (window.WebGLRenderingContext) {
        const canvas = document.createElement('canvas');
        try {
            // Note that { failIfMajorPerformanceCaveat: true } can be passed as a second argument
            // to canvas.getContext(), causing the check to fail if hardware rendering is not available. See
            // https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
            // for more details.
            const context = canvas.getContext('webgl2') || canvas.getContext('webgl');
            if (context && typeof context.getParameter == 'function') {
                return true;
            }
        } catch (e) {
            // WebGL is supported, but disabled
        }
        return false;
    }
    // WebGL not supported
    return false;
    }
    if (!isWebGLSupported()) {
        var result = bowser.getParser(window.navigator.userAgent);
        const BrowserName = result.parsedResult.browser.name
        const BrowserVersion = result.parsedResult.browser.version
        const msg = 'Unfortunately, your browser ${BrowserName} version ${BrowserVersion} does not support the WebGL: // https://get.webgl.org/'
        alert(msg);

    } else {
        // console.log('WebGL is working in your Browser')
    };

var map = new maplibregl.Map({
    container: 'webmap',
    style: 'https://tiles.versatiles.org/styles/neutrino.json', // Neutrino - light basemap
    center: [12.55, 49.89],
    zoom: 3,
    pitch: 20
});

let nav_control = new maplibregl.NavigationControl({
    showCompass: true,
    showZoom: true,
    visualizePitch: true
});

map.addControl(nav_control, 'bottom-left');

map.on('load', function () {
    map.addSource('places', {
      type: 'geojson',
      data: JSON.parse(geojsonfile)
    });
    map.addLayer({
        'id': 'places-layer',
        'type': 'circle',
        'source': 'places',
        'paint': {
            'circle-radius': 3,
            'circle-color': "#088",
            'circle-stroke-color': "#fff",
            'circle-stroke-width': 1
            }
    });
});