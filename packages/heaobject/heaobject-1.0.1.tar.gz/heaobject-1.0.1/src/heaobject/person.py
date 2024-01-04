from .root import AbstractDesktopObject
from typing import Optional
from email_validator import validate_email, EmailNotValidError  # Leave this here for other modules to use
from base64 import urlsafe_b64encode, urlsafe_b64decode
from functools import partial


class Person(AbstractDesktopObject):
    """
    Represents a Person
    """

    def __init__(self) -> None:
        super().__init__()
        # id is a super field
        # name is inherited in super
        self.__preferred_name: Optional[str] = None
        self.__first_name: Optional[str] = None
        self.__last_name: Optional[str] = None
        self.__title: Optional[str] = None
        self.__email: Optional[str] = None
        self.__phone_number: Optional[str] = None

    @property
    def preferred_name(self) -> Optional[str]:
        """
        The Person's preferred name (Optional).
        """
        return self.__preferred_name

    @preferred_name.setter
    def preferred_name(self, preferred_name: Optional[str]) -> None:
        self.__preferred_name = str(preferred_name) if preferred_name is not None else None

    @property
    def first_name(self) -> Optional[str]:
        """
        The Person's first name or given name (Optional).
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: Optional[str]) -> None:
        self.__first_name = str(first_name) if first_name is not None else None
        self.__update_display_name()

    @property
    def last_name(self) -> Optional[str]:
        """
          The Person's last name (Optional).
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: Optional[str]) -> None:
        self.__last_name = str(last_name) if last_name is not None else None
        self.__update_display_name()

    @property
    def title(self) -> Optional[str]:
        """
          The Person's title (Optional).
        """
        return self.__title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        self.__title = str(title) if title is not None else None

    @property
    def email(self) -> Optional[str]:
        """
        The person's email (Optional). Must be a valid e-mail address or None.
        """
        return self.__email

    @email.setter
    def email(self, email: Optional[str]) -> None:
        self.__email = _validate_email(str(email)).email if email is not None else None

    @property
    def phone_number(self) -> Optional[str]:
        """
          The Person's phone number (Optional).
        """
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number: Optional[str]) -> None:
        self.__phone_number = str(phone_number) if phone_number is not None else None

    def __update_display_name(self):
        fname = self.first_name if self.first_name else ""
        lname = self.last_name if self.last_name else ""
        if fname or lname:
            self.display_name = f"{fname}{' ' if fname and lname else ''}{lname}"
        else:
            self.display_name = None


ROLE_ENCODING = 'utf-8'


class Role(AbstractDesktopObject):
    """
    A user role, for authorization purposes. While HEA exposes user authorization information via access control lists,
    this class supports compatibility with file systems with role-based authorization like Amazon Web Services S3
    buckets. The id and name attributes are synchronized with the role attribute such that setting one automatically
    populates the others.
    """
    def __init__(self):
        self.__role: str | None = None

    @property
    def id(self) -> str | None:
        """
        The role, base64-encoded using this module's encode_role() function. Setting this attribute automatically
        generates values for the name and role attributes.
        """
        return self.name

    @id.setter
    def id(self, id_: str | None):
        self.name = id_

    @property
    def name(self) -> str | None:
        """
        The role, base64-encoded using this module's encode_role() function. Setting this attribute automatically
        generates values for the id and role attributes.
        """
        role_ = self.role
        return encode_role(role_) if role_ is not None else None

    @name.setter
    def name(self, name: str | None):
        self.role = decode_role(name) if name is not None else None

    @property
    def role(self) -> str | None:
        """
        The role. Setting this attribute automatically generates values for the id and name attributes.
        """
        return self.__role

    @role.setter
    def role(self, role: str | None):
        self.__role = str(role) if role is not None else role


def encode_role(role: str) -> str:
    """
    Encodes a role string using the Base 64 URL- and filesystem-safe alphabet, which replaces '+' with '-' and '/' with
    '_' in the base 64 alphabet as described in the IETF RFC 4648 specification section 5.

    :param role: the role string (required).
    :returns: returns the encoded data as a utf-8 string.
    """
    return urlsafe_b64encode(role.encode(ROLE_ENCODING)).decode(ROLE_ENCODING)

def decode_role(role_encoded: str) -> str:
    """
    Decodes a string encoded using this module's encode_role() function.

    :param role_encoded: the encoded role string (required).
    :returns: the decoded data as a utf-8 string.
    """
    return urlsafe_b64decode(role_encoded).decode(ROLE_ENCODING)


_validate_email = partial(validate_email, check_deliverability=False)
