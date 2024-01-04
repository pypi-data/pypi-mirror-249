from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud_ml import GenericCRUDML   # noqa402
from language_local.lang_code import LangCode  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class CountyMl(GenericCRUDML):

    def __init__(self):
        logger.start("start init CountyMl")
        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.COUNTY_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.COUNTY_ML_ID_COLUMN_NAME)  # noqa501
        logger.end("end init CountyMl")

    def insert(self, county_id: int, county: str, lang_code: LangCode,
               title_approved: bool = False):
        logger.start("start insert county_ml",
                     object={'county_id': county_id, 'county': county,
                             'lang_code': lang_code,
                             'title_approved': title_approved})
        county_ml_json = {
                key: value for key, value in {
                    'county_id': county_id,
                    'lang_code': lang_code,
                    'title': county,
                    'title_approved': title_approved
                }.items() if value is not None
        }
        county_ml_id = super().insert(
            table_name=LocationLocalConstants.COUNTY_ML_TABLE_NAME,
            data_json=county_ml_json)
        logger.end("end insert county_ml",
                   object={'county_ml_id': county_ml_id})

        return county_ml_id
