from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud_ml import GenericCRUDML   # noqa402
from language_local.lang_code import LangCode  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class StateMl(GenericCRUDML):

    def __init__(self):
        logger.start("start init StateMl")
        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.STATE_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.STATE_ML_ID_COLUMN_NAME)  # noqa501
        logger.end("end init StateMl")

    def insert(self, state_id: int, state: str,
               lang_code: LangCode, title_approved: bool = False):
        logger.start("start insert state_ml",
                     object={'state_id': state_id,
                             'state': state,
                             'lang_code': lang_code,
                             'title_approved': title_approved})
        state_ml_json = {
                key: value for key, value in {
                    'state_id': state_id,
                    'lang_code': lang_code,
                    'state_name': state,
                    'state_name_approved': title_approved
                }.items() if value is not None
            }
        state_ml_id = super().insert(
            table_name=LocationLocalConstants.STATE_ML_TABLE_NAME,
            data_json=state_ml_json)
        logger.end("end insert state_ml",
                   object={'state_ml_id': state_ml_id})

        return state_ml_id
