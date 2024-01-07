from database_mysql_local.generic_crud import GenericCRUD
from language_local.lang_code import LangCode
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_ID = 174
EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_NAME = 'email address local'
DEVELOPER_EMAIL = "idan.a@circ.zone"
EMAIL_ADDRESS_SCHEMA_NAME = "email_address"
EMAIL_ADDRESS_ML_TABLE_NAME = "email_address_ml_table"
EMAIL_ADDRESS_TABLE_NAME = "email_address_table"
EMAIL_ADDRESS_VIEW = "email_address_view"
EMAIL_ADDRESS_ID_COLLUMN_NAME = "email_address_id"
EMAIL_COLLUMN_NAME = "email"
object1 = {
    'component_id': EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': "idan.a@circ.zone"
}
logger = Logger.create_logger(object=object1)


class EmailAddressesLocal(GenericCRUD):
    # TODO Where shall we link email-address_id to person, contact, profile ...?
    # Can we create generic function for that in GenericCRUD and use it multiple times
    # in https://github.com/circles-zone/email-address-local-python-package
    def __init__(self) -> None:
        super().__init__(default_schema_name=EMAIL_ADDRESS_SCHEMA_NAME,
                         default_table_name=EMAIL_ADDRESS_TABLE_NAME,
                         default_id_column_name=EMAIL_ADDRESS_ID_COLLUMN_NAME,
                         default_view_table_name=EMAIL_ADDRESS_VIEW)

    def insert(self, email_address: str, lang_code: LangCode, name: str) -> int or None:
        logger.start(object={"email_address": email_address,
                             "lang_code": lang_code.value, "name": name})
        data = {
            EMAIL_COLLUMN_NAME: f'{email_address}',
        }
        email_address_id = super().insert(data_json=data)
        email_json = {
            "email_address_id": email_address_id,
            "lang_code": lang_code.value,
            "name": name
        }
        super().insert(table_name=EMAIL_ADDRESS_ML_TABLE_NAME, data_json=email_json)
        logger.end(object={'email_address_id': email_address_id})
        return email_address_id

    def update_email_address(self, email_address_id: int, new_email: str) -> None:
        logger.start(object={"email_address_id": email_address_id, "new_email": new_email})
        email_json = {"email": new_email}
        self.update_by_id(id_column_value=email_address_id, data_json=email_json)
        logger.end()

    def delete(self, email_address_id: int) -> None:
        logger.start(object={"email_id": email_address_id})
        self.delete_by_id(id_column_value=email_address_id)
        logger.end()

    def get_email_address_by_email_address_id(self, email_address_id: int) -> str:
        logger.start(object={"email_address_id": email_address_id})
        result = self.select_multi_tuple_by_id(select_clause_value=EMAIL_COLLUMN_NAME,
                                               id_column_value=email_address_id)
        if result:
            email_address = result[0][0]
        else:
            email_address = None
        logger.end(object={'email_address': email_address})
        return email_address

    def get_email_address_id_by_email_address(self, email: str) -> int:
        # TODO: Replace str with EmailAddress Class
        logger.start(object={"email": email})
        result = self.select_multi_tuple_by_where(
            where=f"{EMAIL_COLLUMN_NAME}='{email}'")
        if result:
            email_address_id = result[0][0]
        else:
            email_address_id = None
        logger.end(object={'email_address_id': email_address_id})
        return email_address_id

    def verify_email_address(self, email_address: str) -> None:
        """verify_email_address executed by SmartLink/Action"""
        # TODO Think about creating parent both to verifiy_email_address and verify_phone
        logger.start(object={"email_address": email_address})
        print("verify_email_address called with email_address= ", email_address)
        self.update_by_id(id_column_name="email", id_column_value=email_address, data_json={"is_verified": 1})
        logger.end()
