// loading the GeoJSON file
const geojson: GeoJSON.FeatureCollection = JSON.parse(geojsonfile);
// getting the bbox extent from the GeoJSON file
// [left, bottom, right, top]
const gj_extent: number[] = bbox(geojson);
// getting the bbox center
const gj_extent_center: [number, number] = [(gj_extent[0] + gj_extent[2]) / 2, (gj_extent[1] + gj_extent[3]) / 2];

function isWebGLSupported(): boolean {
    if (window.WebGLRenderingContext) {
        const canvas: HTMLCanvasElement = document.createElement('canvas');
        try {
            // Note that { failIfMajorPerformanceCaveat: true } can be passed as a second argument
            // to canvas.getContext(), causing the check to fail if hardware rendering is not available. See
            // https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
            // for more details.
            const context: WebGLRenderingContext | null = canvas.getContext('webgl2') || canvas.getContext('webgl');
            if (context && typeof context.getParameter === 'function') {
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
    const result: Bowser.Parser.ParsedResult = bowser.getParser(window.navigator.userAgent);
    const BrowserName: string = result.parsedResult.browser.name;
    const BrowserVersion: string = result.parsedResult.browser.version;
    const msg: string = `Unfortunately, your browser ${BrowserName} version ${BrowserVersion} does not support WebGL: // https://get.webgl.org/`;
    alert(msg);
} else {
    // Initiating a map
    const map: maplibregl.Map = new maplibregl.Map({
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
    const gj_bounds: maplibregl.LngLatBounds = new maplibregl.LngLatBounds(gj_extent);
    map.fitBounds(gj_bounds, {
        padding: { top: 15, bottom: 15, left: 10, right: 10 }
    });

    //
    const nav_control: maplibregl.NavigationControl = new maplibregl.NavigationControl({
        showCompass: true,
        showZoom: true,
        visualizePitch: true
    });
    map.addControl(nav_control, 'bottom-left');
    //
    map.addControl(new maplibregl.FullscreenControl());

    map.on('load', () => {
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
        map.on('click', 'places', (e: maplibregl.MapLayerMouseEvent) => {
            map.flyTo({
                center: e.features![0].geometry!.coordinates as maplibregl.LngLatLike
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
}
