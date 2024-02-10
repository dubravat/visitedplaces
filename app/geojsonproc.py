# imports
from typing import Tuple
from os import mkdir, stat
from os.path import normpath, isdir, dirname, exists, join
from geojson import Point, Feature, FeatureCollection, dump, load, loads
from app import app


class GeoJSONAssistant(object):
    def __init__(self, data_dir='data', file_name='places.geojson'):
        """
        Initiates variables.
        Parameters:
        ==========
        :param data_dir:
        :param file_name:
        """
        self.data_dir = data_dir
        self.file_name = file_name

    def get_data_dir(self) -> str:
        """
        Gets (otherwise creates) the data directory.
        Returns:
        ==========
        :return: path_to_data_dir: path to the data directory
        """
        project_dir = dirname(app.root_path)
        path_to_data_dir = normpath(join(project_dir, self.data_dir))

        if not isdir(path_to_data_dir):
            mkdir(path_to_data_dir)

        return path_to_data_dir

    def get_geojson(self) -> str:
        """

        Returns:
        ==========
        :return:
        """
        path_to_geofile = normpath(join(self.get_data_dir(), self.file_name))

        if not exists(path_to_geofile) or stat(path_to_geofile).st_size == 0:
            with open(path_to_geofile, mode='w', encoding='utf-8') as geofile:
                empty_feature_collection = FeatureCollection([])
                dump(empty_feature_collection, geofile, indent=4, sort_keys=False)

        return path_to_geofile

    def add_place(self, record: dict) -> Tuple[bool, str]:
        """

        :param record:
        Returns:
        ==========
        :return:
        """
        geojsonfile = self.get_geojson()

        with open(geojsonfile, mode='r', encoding='utf-8') as geojson_in:
            file_content = load(geojson_in)
            if len(file_content.get("features")) == 0:
                features, places = [], []
                id_max = 0
            else:
                features = file_content.get("features")
                places = list(map(lambda feat: feat["properties"]["place"], features))
                id_max = max(list(map(lambda feat: feat["properties"]["id"], features)))

        place = record.get('place')

        if not (place in places):
            point = Point((record['lon'], record['lat']), precision=6)
            record['id'] = id_max + 1

            if point.is_valid:
                new_feature = Feature(geometry=point, properties=record)
                features.append(new_feature)
                feature_collection = FeatureCollection(features)

                with open(geojsonfile, mode='w', encoding='utf-8') as geojson_out:
                    dump(feature_collection, geojson_out, indent=4)
                    return True, f"The place \'{place}\' was successfully added."

        return False, f"The place \'{place}\' already exists. Therefore, it was not added."

    def remove_last_place(self) -> Tuple[bool, str]:
        """

        Returns:
        ==========
        :return:
        """
        geojsonfile = self.get_geojson()

        with open(geojsonfile, mode='r', encoding='utf-8') as geojson_in:
            file_content = load(geojson_in)
            features = file_content.get("features")
            while 0 < len(features):
                del features[-1]
                break
            else:
                return False, "There are no more places to delete."

        with open(geojsonfile, mode='w', encoding='utf-8') as geojson_out:
            feature_collection = FeatureCollection(features)
            dump(feature_collection, geojson_out, indent=4)

        return True, "The last place was successfully deleted."

    def remove_by_place_name(self, place: str) -> Tuple[bool, str]:
        """

        :param place:
        Returns:
        ==========
        :return:
        """
        geojsonfile = self.get_geojson()
        with open(geojsonfile, mode='r', encoding='utf-8') as geojson_in:
            file_content = load(geojson_in)
            features = file_content.get("features")
            if len(features) > 0:
                try:
                    indx = [features.index(feat) for feat in features if feat["properties"]["place"] == str(place)][0]
                    if indx in (-1, len(features) - 1):
                        self.remove_last_place()
                        return True, f"The place \'{place}\' was successfully deleted from the last position."
                    else:
                        del features[indx]
                        new_ids = [new_id for new_id in range(1, len(features)+1)]
                        for i, feature in enumerate(features):
                            feature["properties"]["id"] = new_ids[i]

                        with open(geojsonfile, mode='w', encoding='utf-8') as geojson_out:
                            feature_collection = FeatureCollection(features)
                            dump(feature_collection, geojson_out, indent=4)
                        return True, f"The place \'{place}\' was successfully deleted."
                except Exception as e:
                    return False, f"The place \'{place}\' does not exist yet."
            else:
                return False, "There are no more features to delete."

    def get_all_places(self) -> list:
        """

        :return:
        """
        geojsonfile = self.get_geojson()
        with open(geojsonfile, mode='r', encoding='utf-8') as geojson_in:
            file_content = load(geojson_in)
            features = file_content.get("features")
            places = list(map(lambda feat: feat["properties"]["place"], features))
        return places

    def get_geojson_as_string(self) -> str:
        """

        :return:
        """
        with open(self.get_geojson(), mode='r', encoding='utf-8') as geojson_in:
            file_content = load(geojson_in)
        return str(file_content)

    def count_places_countries(self) -> Tuple[int, int]:
        """

        :return:
        """
        places, countries = 0, 0
        try:
            features = loads(self.get_geojson_as_string()).get("features")
            places = len(features)
            countries = len(set(map(lambda feat: feat["properties"]["country"], features)))
        except Exception as e:
            print('Exception in count_places_countries', e)
        return places, countries

