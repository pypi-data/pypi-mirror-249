from typing import Dict
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from dotenv import load_dotenv
from .neighborhood import Neighborhood
from .county import County
from .region import Region
from .state import State
from .country import Country
from .city import City
from .location_local_constants import LocationLocalConstants
from .point import Point
from .util import LocationsUtil
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD   # noqa402
from logger_local.Logger import Logger  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402
from language_local.lang_code import LangCode  # noqa: E402

LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = LocationLocalConstants.LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID  # noqa501
LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = LocationLocalConstants.LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME  # noqa501


object_to_insert = {
    'component_id': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

user_context = UserContext().login_using_user_identification_and_password()


# TODO Create LocationsLocal.get_country_id_by_location_id() and call it
# from importer-local-python-package


class LocationsLocal(GenericCRUD):
    def __init__(self):
        logger.start("start init LocationLocal")

        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.LOCATION_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.LOCATION_VIEW_NAME,
            default_id_column_name=LocationLocalConstants.LOCATION_ID_COLUMN_NAME)  # noqa501

        logger.end("end init LocationLocal")

    def get_location_ids(self, neighborhood_name: str, county_name: str,
                         region_name: str, state_name: str, country_name: str,
                         city_name: str) -> tuple([int, int, int, int, int,
                                                   int]):
        logger.start("start get location ids",
                     object={'neighborhood_name': neighborhood_name,
                             'county_name': county_name,
                             'region_name': region_name,
                             'state_name': state_name,
                             'country_name': country_name,
                             'city_name': city_name})

        neighborhood_id = Neighborhood.get_neighborhood_id_by_neighborhood_name(neighborhood_name)  # noqa501
        county_id = County.get_county_id_by_county_name_state_id(county_name)
        region_id = Region.get_region_id_by_region_name(region_name)
        state_id = State.get_state_id_by_state_name(state_name)
        country_id = Country.get_country_id_by_country_name(country_name)
        city_id = City.get_city_id_by_city_name_state_id(city_name)

        logger.end("end get location ids",
                   object={"neighborhood_id": neighborhood_id,
                           "county_ids": county_id, "region_ids": region_id,
                           "state_ids": state_id, "country_id": country_id,
                           'city_id': city_id})
        return (neighborhood_id, county_id, region_id, state_id, country_id,
                city_id)

    def insert(
            self, data: Dict[str, any],
            lang_code: LangCode = user_context.get_effective_profile_preferred_lang_code(),  # noqa501
            is_approved: bool = True,
            new_country_data: Dict[str, any] = None) -> int:

        logger.start("start insert location",
                     object={'data': data, 'lang_code': lang_code,
                             'is_approved': is_approved,
                             'new_country_data': new_country_data})

        (neighborhood_id, county_id, region_id, state_id, country_id, city_id) = self._check_details_and_insert_if_not_exist(  # noqa501
            data.get("coordinate"),
            (data.get("neighborhood"),
             data.get("county"),
             data.get("region"),
             data.get("state"),
             data.get("country"),
             data.get("city")),
            lang_code, is_approved, new_country_data)

        location_json = {
                key: value for key, value in {
                    'coordinate': data.get("coordinate"),
                    'address_local_language': data.get(
                        "address_local_language"),
                    'address_english': data.get("address_english"),
                    'neighborhood_id': neighborhood_id,
                    'county_id': county_id,
                    'region_id': region_id,
                    'state_id': state_id,
                    'country_id': country_id,
                    'city_id': city_id,
                    'postal_code': data.get("postal_code"),
                    'plus_code': data.get("plus_code"),
                    'is_approved': is_approved
                }.items() if value is not None
            }

        location_id = super().insert(data_json=location_json)

        logger.end("end_insert location",
                   object={'location_id': location_id})
        return location_id

    def update(self, location_id: int, data: Dict[str, any],
               lang_code: LangCode = "en", is_approved: bool = True):

        logger.start("start update location",
                     object={'location_id': location_id, 'data': data,
                             'lang_code': lang_code,
                             'is_approved': is_approved})

        (neighborhood_id, county_id, region_id, state_id, country_id, city_id) = self._check_details_and_insert_if_not_exist(  # noqa501
            data.get("coordinate"),
            (data.get("neighborhood"),
             data.get("county"),
             data.get("region"),
             data.get("state"),
             data.get("country"),
             data.get("city")),
            lang_code, is_approved)

        updated_location_json = {
                key: value for key, value in {
                    'coordinate': data.get('coordinate'),
                    'address_local_language': data.get(
                        "address_local_language"),
                    'address_english': data.get("address_english"),
                    'neighborhood_id': neighborhood_id,
                    'county_id': county_id,
                    'region_id': region_id,
                    'state_id': state_id,
                    'country_id': country_id,
                    'city_id': city_id,
                    'postal_code': data.get("postal_code"),
                    'plus_code': data.get("plus_code"),
                    'is_approved': is_approved
                }.items() if value is not None
            }
        super().update_by_id(id_column_value=location_id,
                             data_json=updated_location_json)

        logger.end("end update location")

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_id(
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.LOCATION_TABLE_COLUMNS)

        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    def delete(self, location_id: int):
        logger.start("start delete location by id",
                     object={'location_id': location_id})
        super().delete_by_id(id_column_value=location_id)

        logger.end("end delete location by id")

    def _check_details_and_insert_if_not_exist(
            self, coordinate: Dict[str, Point],
            location_details: tuple([str, str, str, str, str, str]),
            lang_code: LangCode = 'en', is_approved: bool = False,
            new_country_data: Dict[str, any] = None) -> tuple(
            [int, int, int, int, int, int]):
        logger.start("start _check_details_and_insert_if_not_exist",
                     object={'coordinate': coordinate,
                             'location_details': location_details,
                             'lang_code': lang_code,
                             'new_country_data': new_country_data})
        (neighborhood_name, county_name, region_name, state_name, country_name, city_name) = location_details  # noqa501

        ids = self.get_location_ids(neighborhood_name, county_name,
                                    region_name, state_name, country_name,
                                    city_name)
        if ids is None:
            return None

        (neighborhood_id, county_id, region_id, state_id, country_id, city_id) = ids  # noqa501

        if neighborhood_id is None and neighborhood_name is not None:
            neighborhood_object = Neighborhood()
            neighborhood_id = neighborhood_object.insert(
                coordinate=coordinate,
                neighborhood=neighborhood_name,
                lang_code=lang_code,
                title_approved=is_approved)

        if county_id is None and country_name is not None:
            county_object = County()
            county_id = county_object.insert(coordinate=coordinate,
                                             county=county_name,
                                             lang_code=lang_code,
                                             title_approved=is_approved)

        if region_id is None and region_name is not None:
            region_object = Region()
            region_id = region_object.insert(coordinate=coordinate,
                                             region=region_name,
                                             lang_code=lang_code,
                                             title_approved=is_approved)

        if state_id is None and state_name is not None:
            state_object = State()
            state_id = state_object.insert(coordinate=coordinate,
                                           state=state_name,
                                           lang_code=lang_code,
                                           state_name_approved=is_approved)

        if country_id is None and country_name is not None:
            country_object = Country()
            country_id = country_object.insert(
                coordinate=coordinate,
                country=country_name,
                lang_code=lang_code,
                title_approved=is_approved,
                new_country_data=new_country_data)
        if city_id is None and city_name is not None:
            city_object = City()
            city_id = city_object.insert(coordinate=coordinate,
                                         city=city_name,
                                         lang_code=lang_code,
                                         title_approved=is_approved)
        logger.end("end _check_details_and_insert_if_not_exist",
                   object={'neighborhood_id': neighborhood_id,
                           'county_id': county_id,
                           'region_id': region_id, 'state_id': state_id,
                           'country_id': country_id, 'city_id': city_id})
        return (neighborhood_id, county_id, region_id, state_id, country_id,
                city_id)
