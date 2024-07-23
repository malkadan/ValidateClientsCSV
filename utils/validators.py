
import re
from utils.transformers import Transformers
from utils.department import DepartmentEnum
from typing import Tuple, Dict


class Validator():

    def __init__(self, entry):
        self.entry = entry

    def NoneOrEmpty(func):
        def wrapper(self, text):
            try:
                if not text:
                    return False, None
                else:
                    return func(self, text)
            except Exception as e:
                print(f"Exception occurred in {func.__name__}: {str(e)}")
                return False, None

        return wrapper

    def _validate_string_non_email(self, text) -> Tuple[bool, str]:
        """

        :param key:
        :return:
        """
        obj = text
        obj = Transformers.basic_strip_transform(obj)
        return obj and bool(re.search('^[a-zA-Z0-9_]+$', obj)), obj

    @NoneOrEmpty
    def validate_username(self, text) -> Tuple[bool, str]:
        return self._validate_string_non_email(text)

    @NoneOrEmpty
    def validate_name(self, text) -> Tuple[bool, str]:
        """

        :return:
        """
        return self._validate_string_non_email(text)

    @NoneOrEmpty
    def validate_email(self, text) -> Tuple[bool, str]:
        """

        :return:
        """
        obj = Transformers.lowercase_email_transformer(text)
        return bool(re.search('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', obj)), obj

    @NoneOrEmpty
    def validate_department(self, text) -> Tuple[bool, str]:
        """

        :return:
        """
        obj = Transformers.basic_strip_transform(text)
        return obj and any(obj == item.value for item in DepartmentEnum), obj

    @NoneOrEmpty
    def validate_phone(self, text) -> Tuple[bool, str]:
        """

        :return:
        """
        if not text:
            return True, text
        pattern = '^\d{3}(?:-?\d)*$'
        obj = Transformers.basic_strip_transform(text)
        return bool(re.search(pattern, obj)), \
            Transformers.phone_regex_transformer(obj)

    def run(self) -> Tuple[bool, Dict]:
        username, name, email, department, phone = self.validate_username(self.entry['username']), \
                                                    self.validate_name(self.entry['name']), \
                                                    self.validate_email(self.entry['email']), \
                                                    self.validate_department(self.entry['department']), \
                                                    self.validate_phone(self.entry['phone'])

        return username[0] and name[0] and email[0] and department[0] and phone[0], \
            {'username': username[1],
             'name': name[1],
             'email': email[1],
             'department': department[1],
             'phone': phone[1]}

