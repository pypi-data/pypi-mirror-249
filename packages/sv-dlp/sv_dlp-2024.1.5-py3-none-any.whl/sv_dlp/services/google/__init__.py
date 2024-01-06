import json as j
import math
import re
import urllib.parse
from datetime import datetime
from random import choice

import requests

import sv_dlp.services
from .url_protobuf import build_find_panorama_request_url  # GeoPhotoService.SingleImageSearch
from .url_protobuf import build_find_panorama_by_id_request_url # GeoPhotoService.GetMetadata

class urls:
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    def _build_tile_url(pano_id, zoom=3, x=0, y=0, nbt=True, fover=2):
        """
        Build Google Street View Tile URL
        """
        url = f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={pano_id}&x={x}&y={y}&zoom={zoom}&nbt={1 if nbt == True else 0}&fover={fover}"
        return url

    def _build_metadata_url(pano_id=None, lat=None, lng=None, mode="GetMetadata", radius=500):
        """
        Build GeoPhotoService call URL from
        Pano ID that contains panorama key data 
        such as image size, location, coordinates,
        date and previous panoramas.
        """
        match mode:
            case "GetMetadata":
                url = build_find_panorama_by_id_request_url(pano_id, download_depth=True, locale="en-US")
            case "SingleImageSearch":
                xdc = "_xdc_._" + "".join([y for x in range(6) if (y := choice(urls.chars)) is not None])
                url = build_find_panorama_request_url(lat=lat, lon=lng, radius=radius, download_depth=True, locale="en-US", search_third_party=False, xdc=xdc)
                # TODO: Adapt Metadata to search_third_party
            case "SatelliteZoom":
                x, y = geo._coordinate_to_tile(lat, lng)
                url = f"https://www.google.com/maps/photometa/ac/v1?pb=!1m1!1smaps_sv.tactile!6m3!1i{x}!2i{y}!3i17!8b1"
        return url

    def _build_short_url(pano_id, heading=0, pitch=0, zoom=90, mode='new') -> str:
        """
        Build API call URL that shorts an encoded URL.
        Useful for shortening panorama IDs.
        """
        encoded_input = f"https://www.google.com/maps/@?api=1&map_action=pano&pano={pano_id}&heading={heading}&pitch={pitch}&fov={zoom}"
        match mode:
            case 'legacy':
                url = f"https://www.google.com/maps/rpc/shorturl?pb=!1s{urllib.parse.quote(encoded_input)}"
            case 'new':
                url = f"https://www.google.com/maps/rpc/shorturl?pb=!1s{urllib.parse.quote(encoded_input)}{urllib.parse.quote('?entry=tts!2m2!1s!7e81!6b1')}"
        return url
    
class geo:
    def _project(lat, lng, TILE_SIZE=256):
        siny = math.sin((lat * math.pi) / 180)
        siny = min(max(siny, -0.9999), 0.9999)
        x = TILE_SIZE * (0.5 + lng / 360),
        y = TILE_SIZE * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi)),
        return x[0], y[0]
    def _coordinate_to_tile(lat, lng, tile_size=256, zoom=17):
        x, y = geo._project(lat, lng)
        zoom = 1 << zoom
        tile_x = math.floor((x * zoom) / tile_size)
        tile_y = math.floor((y * zoom) / tile_size)
        return tile_x, tile_y

class misc:
    def get_pano_from_url(url):
        url = requests.get(url).url
        pano_id = re.findall(r"1s(.+)!2e", url)
        if pano_id == []:
            # https://www.google.com/maps/@?api=1&map_action=pano&pano=[PANO_ID]&shorturl=1
            pano_id = re.findall(r"pano=([^&]+)", url)
        return pano_id[0]

    def short_url(pano_id, heading=0, pitch=0, zoom=90):
        """
        Shorts panorama ID by using the
        share function found on Google Maps
        """
        url = urls._build_short_url(pano_id, heading=heading, pitch=pitch, zoom=zoom)
        json = j.loads(requests.get(url).content[5:])
        return json[0]

class metadata:
    _convert_date = lambda raw_date : datetime.strptime(raw_date, "%Y/%m")

    def get_metadata(pano_id=None, lat=None, lng=None, get_linked_panos=False) -> dict:
        if pano_id == None:
            pano_id = metadata._get_pano_from_coords(lat, lng)
        elif type(pano_id) is list:
            pano_id = pano_id[0]
            
        raw_md = metadata._get_raw_metadata(pano_id)
        try:
            lat, lng = raw_md[1][0][5][0][1][0][2], raw_md[1][0][5][0][1][0][3] 
            image_size = raw_md[1][0][2][2][0] # obtains highest resolution
            image_avail_res = raw_md[1][0][2][3] # obtains all resolutions available
            raw_image_date = raw_md[1][0][6][-1] # [0] for year - [1] for month
            raw_image_date = f"{raw_image_date[0]}/{raw_image_date[1]}"
            # def considering parsing this as a protocol buffer instead - this is too messy
        except IndexError:
            raise sv_dlp.services.PanoIDInvalid

        md = sv_dlp.services.MetadataStructure(
            service="google",
            pano_id=pano_id,
            lat=float(lat),
            lng=float(lng),
            date=metadata._convert_date(raw_image_date),
            size=[image_avail_res[0], image_avail_res[1]],
            max_zoom=len(image_avail_res[0])-1,
            misc={
                "is_trekker": len(raw_md[1][0][5][0][3][0][0][2]) > 3,
                "gen": metadata._get_gen(image_size)
            }
        )
        if md.misc["is_trekker"]:
            md.misc["trekker_id"] = raw_md[1][0][5][0][3][0][0][2][3][0]
        
        md = metadata._parse_panorama(md, raw_md, output="timeline")
        if get_linked_panos:
            md = metadata._parse_panorama(md, raw_md, output="linked_panos")
        return md

    def _parse_panorama(md, raw_md, output=""):
        linked_panos = raw_md[1][0][5][0][3][0]
        buff = []
        match output:
            case "timeline":
                try:
                    for pano_info in raw_md[1][0][5][0][8]:
                        if pano_info == None: break
                        else:
                            raw_pano_info = linked_panos[pano_info[0]]
                            buff.append({
                                "pano_id": raw_pano_info[0][1],
                                "lat": raw_pano_info[2][0][-2],
                                "lng": raw_pano_info[2][0][-1],
                                "date": metadata._convert_date(f"{pano_info[1][0]}/{pano_info[1][1]}")
                            })
                except IndexError: # no timeline:
                    buff = []
                except TypeError:
                    buff = []
                md.timeline = buff
            case "linked_panos":
                md["linked_panos"] = {}
                for pano_info in linked_panos:
                    pano_id = pano_info[0][1]
                    if pano_id != raw_md[1][0][1][1]:
                        if pano_id not in [x["pano_id"] for x in md["timeline"]]:
                            date = metadata.get_metadata(pano_id=pano_id)["date"]
                            buff.append({
                                    "pano_id": pano_info[0][1],
                                    "lat": pano_info[2][0][-2],
                                    "lng": pano_info[2][0][-1],
                                    "date": date,
                            })
                md.linked_panos = buff
            case _:
                raise Exception # lol
        return md

    def _get_raw_metadata(pano_id) -> dict:
        """
        Returns panorama ID metadata.
        """
        url = urls._build_metadata_url(pano_id=pano_id, mode="GetMetadata")
        data = requests.get(url).content[5:]
        raw_md = j.loads(data)
        return raw_md

    def _get_pano_from_coords(lat, lng, radius=500) -> dict:
        """
        Returns closest Google panorama ID to given parsed coordinates.
        """
        try:
            url = urls._build_metadata_url(lat=lat, lng=lng, mode="SingleImageSearch", radius=radius)
            json = requests.get(url).text
            if "Search returned no images." in json:
                print("[google]: Finding nearest panorama via satellite zoom...")
                url = urls._build_metadata_url(lat=lat, lng=lng, mode="SatelliteZoom")
                json = requests.get(url).text
                data = j.loads(json[4:])
                pano = data[1][1][0][0][0][1]
            else:
                data = re.findall(r'\[(\d+),"(.+?)"\].+?,\[\[null,null,(.+?),(.+?)\]', json)
                pano = data[0][1]
        except TypeError:
            raise sv_dlp.services.NoPanoIDAvailable
        # pans = re.findall(r"\[[0-9],"(.+?)"].+?,\[\[null,null,(.+?),(.+?)\]", json)
        return pano

    def _get_gen(image_size):
        match image_size:
            case 1664: return "1"
            case 6656: return "2/3"
            case 8192: return "4"

def _build_tile_arr(metadata, zoom=2):
    pano_id = metadata.pano_id
    
    if zoom == 0: # zoom 0 is an uncropped panorama preview
        arr = [[urls._build_tile_url(pano_id=pano_id, zoom=zoom, x=0, y=0)]]
    else:
        x_axis = metadata.size[0][zoom][0][1] // metadata.size[1][1]
        y_axis = metadata.size[0][zoom][0][0] // metadata.size[1][0]
        arr = [[] for _ in range(y_axis)]
        for y in range(y_axis):
            for x in range(x_axis):
                url = urls._build_tile_url(pano_id=pano_id, zoom=zoom, x=x, y=y)
                arr[y].append(url)
    return arr