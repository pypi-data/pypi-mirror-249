


def map(record):

    API_KEY = 'AIzaSyCdVL64h1rNYu83c8pHBiNy5E1UfiCpc8g'

    street = record.get('streetAddress', '')
    city = record.get('addressLocality', '')
    state = record.get('addressRegion', '')
    country = record.get('addressCountry', '')
    postalCode = record.get('postalCode', '')


    query = f'''{street}, {city}, {state},{country},{postalCode}'''
    
    content = f'''
<iframe
  width="600"
  height="450"
  style="border:0"
  loading="lazy"
  allowfullscreen
  referrerpolicy="no-referrer-when-downgrade"
  src="https://www.google.com/maps/embed/v1/place?key={API_KEY}
    &q={query}">
</iframe>
    
    '''
    content = f'''
    <iframe
      width="600"
      height="450"
      style="border:0"
      loading="lazy"
      allowfullscreen
      referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps/embed/v1/place?key={API_KEY}
        &q={query}">
    </iframe>

        '''
    return content

    content = f'''
<script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
<script>
    let map;
    
    async function initMap() {{
      // The location of Uluru
      const position = {{ lat: -25.344, lng: 131.031 }};
      // Request needed libraries.
      //@ts-ignore
      const {{ Map }} = await google.maps.importLibrary("maps");
      const {{ AdvancedMarkerElement }} = await google.maps.importLibrary("marker");
    
      // The map, centered at Uluru
      map = new Map(document.getElementById("map"), {{
        zoom: 4,
        center: position,
        mapId: "DEMO_MAP_ID",
      }});
    
      // The marker, positioned at Uluru
      const marker = new AdvancedMarkerElement({{
        map: map,
        position: position,
        title: "Uluru",
      }});
    }}
    
    initMap();

</script>
    <div id="map"></div>

    <!-- prettier-ignore -->
    <script>
    (g=>{{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={{}});var d=b.maps||(b.maps={{}}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${{c}}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))}})
        ({{key: "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg", v: "weekly"}});
        </script>
    
    '''
    return content
    
    content = f'''
    <script>
        const CONFIGURATION = {{
            "locations": [
              {{
                "title":"{street}",
                "address1":"{street}",
                "address2":"{city}, {state} {postalCode}, {country}"
                }}
            ],
            "mapOptions": {{
                "center":{{"lat":38.0,"lng":-100.0}},
                "fullscreenControl":true,
                "mapTypeControl":false,
                "streetViewControl":false,
                "zoom":4,
                "zoomControl":true,
                "maxZoom":17,
                "mapId":""
                }},
        "mapsApiKey": "AIzaSyCdVL64h1rNYu83c8pHBiNy5E1UfiCpc8g",
        "capabilities": {{
            "input":false,
            "autocomplete":false,
            "directions":false,
            "distanceMatrix":false,
            "details":false,
            "actions":false
          }}
        }};
    </script>
    <script type="module">
        document.addEventListener('DOMContentLoaded', async () => {{
            await customElements.whenDefined('gmpx-store-locator');
            const locator = document.querySelector('gmpx-store-locator');
            locator.configureFromQuickBuilder(CONFIGURATION);
        }});
    </script>

    <!-- Please note unpkg.com is unaffiliated with Google Maps Platform. -->
    <script type="module" src="https://unpkg.com/@googlemaps/extended-component-library@0.6"></script>

    <!-- Uses components from the Extended Component Library; see
         https://github.com/googlemaps/extended-component-library for more information
         on these HTML tags and how to configure them. -->
         
    <gmpx-api-loader key="AIzaSyCdVL64h1rNYu83c8pHBiNy5E1UfiCpc8g" solution-channel="GMP_QB_locatorplus_v10_c"></gmpx-api-loader>
    
    <gmpx-store-locator map-id="DEMO_MAP_ID"></gmpx-store-locator>

    '''
    
    return content