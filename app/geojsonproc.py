# imports
import json
from os import mkdir
from os.path import normpath, isdir, exists, join
from ast import literal_eval
from typing import Tuple
from geojson import Point, Feature, FeatureCollection, dump


class GeoJSONAssistant(object):
    def __init__(self, data_dir='data', file_name='places.geojson'):
        """
        Initiates variables
        Parameters:
        ==========
        :param data_dir:
        :param file_name:
        """
        self.data_dir = data_dir
        self.file_name = file_name

    def get_data_dir(self) -> str:
        path_to_data_dir = normpath(self.data_dir)
        if not isdir(path_to_data_dir):
            mkdir(path_to_data_dir)
        return path_to_data_dir

    def get_file_path(self) -> str:
        path_to_file = normpath(join(self.get_data_dir(), self.file_name))
        if not exists(path_to_file):
            open(path_to_file, 'w+')
        return path_to_file

    def add_record(self, record):
        geojsonfile = self.get_file_path()

        with open(geojsonfile, 'r', encoding='utf-8') as file:
            file_content = file.readline()
            if len(file_content) == 0:
                features, places = [], []
                id_max = 0
            else:
                try:
                    features = literal_eval(file_content)["features"]
                    places = list(map(lambda feat: feat["properties"]["place"], features))
                    id_max = max(list(map(lambda feat: feat["properties"]["id"], features)))
                except Exception as e:
                    print('Exception in add_record', e)

        if not (record['place'] in places):
            point = Point((record['lon'], record['lat']), precision=6)
            record['id'] = id_max + 1

            if point.is_valid:
                new_feature = Feature(geometry=point, properties=record)
                features.append(new_feature)
                feature_collection = FeatureCollection(features)

                with open(geojsonfile, 'w', encoding='utf-8') as file:
                    dump(feature_collection, file)

        return None

    def get_data_as_json(self) -> str:
        with open(self.get_file_path(), 'r', encoding='utf-8') as file:
            file_content = file.read()
        return file_content

    def count_places_countries(self) -> Tuple[int, int]:
        places, countries = 0, 0
        try:
            file_content = json.loads(self.get_data_as_json())
            features = file_content["features"]
            places = len(features)
            countries = len(set(map(lambda feat: feat["properties"]["country"], features)))
        except Exception as e:
            print('Exception in count_places_countries', e)
        return places, countries
