from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
from .county_ml import CountyMl
from .point import Point
from .util import LocationsUtil
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa402
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402


logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class County(GenericCRUD):
    county_ml = CountyMl()

    def __init__(self):
        logger.start("start init County")

        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.COUNTY_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.COUNTY_VIEW_NAME,
            default_id_column_name=LocationLocalConstants.COUNTY_ID_COLUMN_NAME
            )

        logger.end("end init County")

    def insert(
            self, county: str, lang_code: LangCode,
            title_approved: bool = False, coordinate: Point = None,
            group_id: int = None) -> int:
        logger.start("start insert county",
                     object={'coordinate': coordinate, 'county': county,
                             'lang_code': lang_code,
                             'title_approved': title_approved})

        county_json = {'coordinate': coordinate,
                       'group_id': group_id}

        county_id = super().insert(data_json=county_json)

        county_ml_id = self.county_ml.insert(county_id=county_id,
                                             county=county,
                                             lang_code=lang_code,
                                             title_approved=title_approved)

        logger.end("end insert county",
                   object={'county_id': county_id,
                           'county_ml_id': county_ml_id})
        return county_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_id(
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.COUNTY_TABLE_COLUMNS)

        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)

        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_county_id_by_county_name_state_id(county_name: str,
                                              state_id: int = None) -> int:
        logger.start("start get_county_id_by_county_name_state_id",
                     object={'county_name': county_name, 'state_id': state_id})

        county_id_json = County.county_ml.select_one_dict_by_where(
            select_clause_value=LocationLocalConstants.COUNTY_ID_COLUMN_NAME,
            where=f"title='{county_name}'")
        county_id = county_id_json.get(
            LocationLocalConstants.COUNTY_ID_COLUMN_NAME)

        logger.end("end get_county_id_by_county_name_state_id",
                   object={'county_id': county_id})
        return county_id
