from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud_ml import GenericCRUDML   # noqa402
from language_local.lang_code import LangCode  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class CityMl(GenericCRUDML):

    def __init__(self):
        logger.start("start init CityMl")
        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.CITY_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.CITY_ML_ID_COLUMN_NAME)  # noqa501
        logger.end("end init CityMl")

    def insert(self, city_id: int, city: str, lang_code: LangCode,
               title_approved: bool = False, is_main: int = None):
        logger.start("start insert city_ml",
                     object={'city_id': city_id, 'city': city,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'is_main': is_main})
        city_ml_json = {
                key: value for key, value in {
                    'city_id': city_id,
                    'lang_code': lang_code,
                    'is_main': is_main,
                    'title': city,
                    'title_approved': title_approved
                }.items() if value is not None
        }
        city_ml_id = super().insert(
            table_name=LocationLocalConstants.CITY_ML_TABLE_NAME,
            data_json=city_ml_json)
        logger.end("end insert city_ml",
                   object={'city_ml_id': city_ml_id})

        return city_ml_id
