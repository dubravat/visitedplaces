// loading the GeoJSON file
var geojson = JSON.parse(geojsonfile);

// getting the bbox extent from the GeoJSON file
// [left, bottom, right, top]
const gj_extent = bbox(geojson);

// getting the bbox center
gj_extent_center = [(gj_extent[0] + gj_extent[2])/2, (gj_extent[1] + gj_extent[3])/2];

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

        // Initiating a map
        var map = new maplibregl.Map({
            container: 'webmap', // The HTML element or element's string id in which to render the map
            style: 'https://tiles.versatiles.org/styles/neutrino.json', // stylesheet location Neutrino - light basemap
            center: [0, 0], // starting position [lng, lat]
            zoom: 3, // starting zoom
            pitch: 10, // starting pitch
            antialias: true, // MSAA antialiasing
            validateStyle: true, // style validation
            collectResourceTiming: true, // Resource Timing API information
        });

        //
        let gj_bounds = new maplibregl.LngLatBounds(gj_extent)
        map.fitBounds(gj_bounds, {
          padding: {top: 15, bottom:15, left: 10, right: 10}
        });

        //
        let nav_control = new maplibregl.NavigationControl({
            showCompass: true,
            showZoom: true,
            visualizePitch: true
        });
        map.addControl(nav_control, 'bottom-left');
        //
        map.addControl(new maplibregl.FullscreenControl());

        map.on('load', function () {

            map.addSource('places', {
              type: 'geojson',
              data: geojson
            });

            map.addLayer({
                'id': 'places',
                'type': 'circle',
                'source': 'places',
                'paint': {
                    'circle-radius': 4,
                    'circle-color': "#1e90ff",
                    'circle-stroke-color': "#fff",
                    'circle-stroke-width': 1
                    }
            });

            // Center the map on the coordinates of any clicked symbol from the 'places' layer.
            map.on('click', 'places', (e) => {
                map.flyTo({
                    center: e.features[0].geometry.coordinates
                });
            });

            // Change the cursor to a pointer when the it enters a feature in the 'places' layer.
            map.on('mouseenter', 'places', () => {
                map.getCanvas().style.cursor = 'pointer';
            });

            // Change it back to a pointer when it leaves.
            map.on('mouseleave', 'places', () => {
                map.getCanvas().style.cursor = '';
            });

        });
    };


