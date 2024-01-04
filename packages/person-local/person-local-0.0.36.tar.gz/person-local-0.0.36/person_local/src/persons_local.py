import datetime
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from circles_local_database_python.generic_crud_ml import GenericCRUDML
from circles_number_generator.number_generator import NumberGenerator
from language_local.lang_code import LangCode
from .person import Person
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger

PERSON_LOCAL_PYTHON_COMPONENT_ID = 169
PERSON_LOCAL_PYTHON_COMPONENT_NAME = 'person-local-python'

person_local_python_code_logger_init_object = {
    'component_id': PERSON_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': PERSON_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}
logger = Logger.create_logger(
    object=person_local_python_code_logger_init_object)


class PersonsLocal(GenericCRUD):
    "PersonsLocal class"

    def __init__(self) -> None:
        super().__init__(default_schema_name="person", default_table_name="person_table",
                         default_view_table_name="person_view",
                         default_id_column_name='person_id')

    def delete_by_person_id(self, person_id: int) -> None:
        "delete person"
        logger.start(f"Delete person by person id person_id={person_id}",
                     object={"person_id": person_id})
        self.delete_by_id(id_column_value=person_id)
        logger.end(f"Person deleted person_id= {person_id}", object={
                   'person_id': person_id})

    def get_person_id_by_person_number(self, person_number: int) -> int or None:
        logger.start(object={'person_number': person_number})
        person_id = None
        result = self.select_multi_dict_by_id(id_column_name='number',
                                              select_clause_value='person_id',
                                              id_column_value=person_number)
        if result:
            person_id = result[0]['person_id']
        logger.end(object={'person_id': person_id})
        return person_id

    def get_person_number_by_person_id(self, person_id: int) -> int:
        logger.start(object={'person_id': person_id})
        person_number = None
        fetched_result = self.select_multi_dict_by_id(select_clause_value='number',
                                                      id_column_value=person_id)
        if fetched_result:
            person_number = fetched_result[0]['number']
        logger.end(object={'person_number': person_number})
        return person_number

    def insert(self, person: Person) -> int:
        logger.start("Insert person", object={
            "number": person.number,
            "gender_id": person.gender_id,
            "last_coordinate": person.last_coordinate,
            "location_id": person.location_id,
            'birthday_date': person.birthday_date,
            'day': person.day,
            'month': person.month,
            'year': person.year,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'nickname': person.nickname,
            'is_test_data': person.is_test_data
        })
        # TODO: We should handle also situations when there is no person.number
        # and we need to generate it using database-with-out-orm package number_generator()

        x_coordinate, y_coordinate = float(
            person.last_coordinate.x), float(person.last_coordinate.y)
        query = (
            "INSERT INTO person_table (number, gender_id, last_coordinate, "
            "location_id, birthday_date, day, month, year, first_name, last_name, nickname, is_test_data, start_timestamp) "
            "VALUES (%s, %s, POINT(%s, %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
        )

        data = (person.number, person.gender_id, x_coordinate, y_coordinate,
                person.location_id, person.birthday_date, person.day, person.month,
                person.year, person.first_name, person.last_name, person.nickname, person.is_test_data)
        """person_detail = {
            "number": person.number,
            "gender_id": person.gender_id,
            "last_coordinate": person.last_coordinate,
            "location_id": person.location_id
        }"""
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, data)
        connection.commit()
        logger.info("Person inserted successfully.")
        person_id = cursor.lastrowid()
        logger.end(f"Person added person_id= {person_id}", object={
                   'person_id': person_id})
        return person_id

    def _insert_person_ml(self, person_id: int, lang_code: LangCode,
                          first_name: str, last_name: str) -> int:
        logger.start("Insert person", object={"person_id": person_id, "lang_code": lang_code,
                                              "first_name": first_name, "last_name": last_name})
        query = (
            f"INSERT INTO person_ml_table (person_id, lang_code, first_name, last_name) "
            f"VALUES ({person_id}, '{lang_code}', '{first_name}', '{last_name}')"
        )
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end("Person added", object={'person_id': person_id})
        return person_id

    @staticmethod
    def update_birthday_day(person_id: int, day: int) -> None:
        "update birthday day"
        logger.start(f"Update birthday day by person id person_id={person_id}",
                     object={"person_id": person_id, "day": day})
        query = (
            f"UPDATE person_table SET day = {day}, "
            f"birthday_date = CONCAT(YEAR(birthday_date), '-', MONTH(birthday_date), '-', {day}) "
            f"WHERE person_id = {person_id}"
        )
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end()

    @staticmethod
    def update_birthday_month(person_id: int, month: int) -> None:
        "update birthday month"
        logger.start(f"Update birthday month by person id person_id={person_id}",
                     object={"person_id": person_id, "month": month})
        # Connector.start_tranaction(None)
        query = f"UPDATE person_table SET `month` = {month}, " \
            f"birthday_date = CONCAT(YEAR(birthday_date), '-', {month}, '-', DAY(birthday_date)) " \
            f"WHERE person_id = {person_id}"
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end()

    @staticmethod
    def update_birthday_year(person_id: int, year: int) -> None:
        "update"
        logger.start(f"Update birthday year by person id person_id={person_id}",
                     object={"person_id": person_id, "year": year})
        query = f"UPDATE person_table SET year = {year}, " \
            f"birthday_date = CONCAT({year}, '-', MONTH(birthday_date), '-', DAY(birthday_date)) " \
            f"WHERE person_id = {person_id}"

        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        connection.commit()
        logger.end()

    def update_birthday_date(self, person_id: int, birthday_date: datetime.date) -> None:
        "update birthday date"
        logger.start(f"Update birthday date by person id person_id={person_id}", object={
                     "person_id": person_id, "birthday_date": birthday_date})
        date = str(birthday_date).split('-')
        person_json = {
            "person_id": person_id,
            "year": int(date[0]),
            "month": int(date[1]),
            "day": int(date[2]),
            "birthday_date": birthday_date
        }
        self.update_by_id(id_column_value=person_id, data_json=person_json)
        logger.end()

    def update_first_name_by_profile_id(self, profile_id: int, first_name: str) -> None:
        "update first name"
        logger.start(f"Update first name by profile id profile_id={profile_id}", object={
                     "profile_id": profile_id, "first_name": first_name})
        person_json = {
            "person_id": profile_id,
            "first_name": first_name
        }
        self.update_by_id(id_column_value=profile_id, data_json=person_json)
        logger.end()

    @staticmethod
    def update_person_ml_first_name_by_person_id(person_id: int,
                                                 lang_code: LangCode, first_name: str) -> None:
        "update ml first name"
        logger.start(f"Update first name in ml table by person id person_id={person_id}", object={
                     "person_id": person_id, lang_code: LangCode, "first_name": first_name})
        query = "UPDATE person_ml_table SET first_name = %s, lang_code = %s where person_id = %s"
        data = (first_name, lang_code, person_id)
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, data)
        connection.commit()
        logger.end()

    def update_nickname_by_person_id(self, person_id: int, nickname: str) -> None:
        "update nickname"
        logger.start(f"Update nickname by person id person_id={person_id}", object={
                     "person_id": person_id, "nickname": nickname})
        person_json = {
            "person_id": person_id,
            "nickname": nickname
        }
        self.update_by_id(id_column_value=person_id, data_json=person_json)
        logger.end()

    def update_last_name_by_person_id(self, person_id: int, last_name: str) -> None:
        "update last name"
        logger.start(f"Update last name by person id person_id={person_id}", object={
                     "id": id, "last_name": last_name})
        person_json = {
            "person_id": person_id,
            "last_name": last_name
        }
        self.update_by_id(id_column_value=person_id, data_json=person_json)
        logger.end()

    def update_person_ml_last_name_by_person_id(self, person_id: int,
                                                lang_code: LangCode, last_name: str) -> None:
        "update ml last name"
        logger.start(f"Update last name in ml table by person id person_id={person_id}", object={
                     "person_id": person_id, "last_name": last_name})
        query = "UPDATE person_ml_table SET last_name = %s, lang_code = %s where person_id = %s"
        data = (last_name, lang_code, person_id)
        connection = Connector.connect('person')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, data)
        connection.commit()

    # def get_test_person_id(self) -> int:
    #     # TODO implement it
    #     test_person_id = 50050341
    #     return test_person_number

    def get_test_person_number(self) -> int:
        person_number = NumberGenerator().get_random_number(
            schema='person', table='person_table', number_column_name='number')
        return person_number

    def get_test_person_id(self) -> int:
        fetched_result = self.select_multi_dict_by_id(id_column_name='is_test_data',
                                                      select_clause_value='person_id',
                                                      id_column_value='1')
        if fetched_result:
            test_person_id = fetched_result[0]['person_id']
            return test_person_id
        else:
            person_number = NumberGenerator().get_random_number(
                schema='person', table='person_table', number_column_name='number')
            person = Person(number=person_number, is_test_data=True)
            test_person_id = self.insert(person=person)
            return test_person_id
