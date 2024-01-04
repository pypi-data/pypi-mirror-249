from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
from .state_ml import StateMl
from .point import Point
from .util import LocationsUtil
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa402
from logger_local.Logger import Logger  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402


logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)


class State(GenericCRUD):
    state_ml = StateMl()

    def __init__(self):
        logger.start("start init State")

        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.STATE_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.STATE_VIEW_NAME,
            default_id_column_name=LocationLocalConstants.STATE_ID_COLUMN_NAME)
        logger.end("End init State")

    def insert(
            self, coordinate: Point,
            state: str, lang_code: LangCode, state_name_approved: bool = False,
            country_id: int = None, group_id: int = None) -> int:
        logger.start("start insert state",
                     object={'coordinate': coordinate, 'state': state,
                             'lang_code': lang_code,
                             'state_name_approved': state_name_approved,
                             'country_id': country_id, 'group_id': group_id})

        state_json = {
                key: value for key, value in {
                    'coordinate': coordinate,
                    'group_id': group_id
                }.items() if value is not None
            }

        state_id = super().insert(data_json=state_json)

        state_ml_id = self.state_ml.insert(state_id=state_id, state=state,
                                           lang_code=lang_code,
                                           title_approved=state_name_approved)

        logger.end("end insert state",
                   object={'state_id': state_id,
                           'state_ml_id': state_ml_id})
        return state_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_id(
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.STATE_TABLE_COLUMNS)
        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_state_id_by_state_name(state_name: str,
                                   country_id: int = None) -> int:
        logger.start("start get_state_id_by_state_name",
                     object={'state_name': state_name,
                             'country_id': country_id})

        state_id_json = State.state_ml.select_one_dict_by_where(
            select_clause_value=LocationLocalConstants.STATE_ID_COLUMN_NAME,
            where=f"state_name='{state_name}'")
        state_id = state_id_json.get(
            LocationLocalConstants.STATE_ID_COLUMN_NAME)

        logger.end("end get_state_id_by_state_name",
                   object={'state_ids': state_id})
        return state_id
