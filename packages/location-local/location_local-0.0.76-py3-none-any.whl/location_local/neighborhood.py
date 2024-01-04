from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
from .neighborhood_ml import NeighborhoodMl
from .point import Point
from .util import LocationsUtil
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa402
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402


logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class Neighborhood(GenericCRUD):
    neighborhood_ml = NeighborhoodMl()

    def __init__(self):
        logger.start("start init Neighborhood")
        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.NEIGHBORHOOD_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.NEIGHBORHOOD_VIEW_NAME,  # noqa501
            default_id_column_name=LocationLocalConstants.NEIGHBORHOOD_ID_COLUMN_NAME)  # noqa501

        logger.end("end init Neighborhood")

    def insert(
            self, coordinate: Point,
            neighborhood: str, lang_code: LangCode,
            title_approved: bool = False, city_id: int = None,
            group_id: int = None) -> int:

        logger.start("start insert neighborhood",
                     object={'coordinate': coordinate,
                             'neighborhood': neighborhood,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'city_id': city_id,
                             'group_id': group_id})
        neighborhood_json = {
                key: value for key, value in {
                    'coordinate': coordinate,
                    'city_id': city_id,
                    'group_id': group_id
                }.items() if value is not None
            }
        neighborhood_id = super().insert(data_json=neighborhood_json)

        neighborhood_ml_id = self.neighborhood_ml.insert(
            neighborhood=neighborhood, neighborhood_id=neighborhood_id,
            lang_code=lang_code, title_approved=title_approved)

        logger.end("end insert neighborhood",
                   object={'neighborhood_id': neighborhood_id,
                           'neighborhood_ml_id': neighborhood_ml_id})
        return neighborhood_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_id(
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.NEIGHBORHOOD_TABLE_COLUMNS)  # noqa501

        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_neighborhood_id_by_neighborhood_name(neighborhood_name: str,
                                                 city_id: int = None) -> int:
        logger.start("start get_neighborhood_id_by_neighborhood_name",
                     object={'neighborhood_name': neighborhood_name,
                             'city_id': city_id})

        neighborhood_id_json = Neighborhood.neighborhood_ml.select_one_dict_by_where(  # noqa501
            select_clause_value=LocationLocalConstants.NEIGHBORHOOD_ID_COLUMN_NAME,  # noqa501
            where=f"title='{neighborhood_name}'")
        neighborhood_id = neighborhood_id_json.get(
            LocationLocalConstants.NEIGHBORHOOD_ID_COLUMN_NAME)

        logger.end("end get_neighborhood_id_by_neighborhood_name",
                   object={'neighborhood_id': neighborhood_id})
        return neighborhood_id
