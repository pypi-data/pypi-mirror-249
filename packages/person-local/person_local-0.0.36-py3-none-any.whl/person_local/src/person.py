from shapely.geometry import Point

# TOOO Person -> PersonLocal
class Person:
    "person details class"

    def __init__(self, number: int, last_coordinate: Point,
                 birthday_date: str = None, day: int = None,
                 month: int = None, year: int = None, first_name: str = None,
                 last_name: str = None, location_id: int = None,
                 nickname: str = None, gender_id: int = None, is_test_data: bool = False) -> None:
        self.number = number
        self.gender_id = gender_id
        self.last_coordinate = last_coordinate
        self.location_id = location_id
        self.birthday_date = birthday_date
        self.day = day
        self.month = month
        self.year = year
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.is_test_data = is_test_data
