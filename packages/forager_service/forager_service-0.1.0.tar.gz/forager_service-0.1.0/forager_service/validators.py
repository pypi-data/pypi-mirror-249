"""Validators for arguments."""
import re

from forager_service.exceptions import ArgumentValidationError


class Validators:
    """Class with method for kwargs validations."""

    @staticmethod
    def validate_str(key: str, value: str) -> None:
        """Validate value is str type."""
        if not isinstance(value, str):
            raise ArgumentValidationError(f"{key} has wrong type.")

    @staticmethod
    def validate_int(key: str, value: int) -> None:
        """Validate value is int type."""
        if not isinstance(value, int):
            raise ArgumentValidationError(f"{key} has wrong type.")

    @staticmethod
    def validate_email_type(key: str, value: str) -> None:
        """Validate email type."""
        if value not in {"personal", "generic"}:
            raise ArgumentValidationError(f"{key} has wrong value.")

    @staticmethod
    def validate_seniority(key: str, value: str) -> None:
        """Validate seniority kwarg."""
        value_list: list = value.split(", ")
        for elem in value_list:
            if elem not in {"junior", "senior", "executive"}:
                raise ArgumentValidationError(f"{key} has wrong value.")

    @staticmethod
    def validate_department(key: str, value: str) -> None:
        """Validate department value."""
        value_list: list = value.split(", ")
        for elem in value_list:
            if elem not in {
                "executive",
                "it",
                "finance",
                "management",
                "sales",
                "legal",
                "support",
                "hr",
                "marketing",
                "communication",
            }:
                raise ArgumentValidationError(f"{key} has wrong value.")

    @staticmethod
    def validate_required_field(key: str, value: str) -> None:
        """Validate required field argument."""
        value_list: list = value.split(", ")
        for elem in value_list:
            if elem not in {"full_name", "position", "phone_number"}:
                raise ArgumentValidationError(f"{key} has wrong value.")

    @staticmethod
    def validate_max_duration(key: str, value: int) -> None:
        """Validate max duration value."""
        if value < 3 or value > 20:
            raise ArgumentValidationError(f"{key} should be in range from 3 to 20.")

    @staticmethod
    def validate_email(key: str, value: str) -> None:
        """Validate email."""
        specials = "!#$%&'*+-/=?^_`{|?."
        specials = re.escape(specials)
        regex = re.compile(
            "^(?!["
            + specials
            + "])(?!.*["
            + specials
            + "]{2})(?!.*["
            + specials
            + "]$)[A-Za-z0-9"
            + specials
            + "]+(?<!["
            + specials
            + "])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"
        )
        if not re.fullmatch(regex, value):
            raise ArgumentValidationError(f"{key} has invalid value.")

    @staticmethod
    def validate_required_arguments(key: str, params: dict) -> None:
        """Validate presence required argument in the list."""
        if key in {"domain-search", "email-finder", "email-count"}:
            if "domain" not in params and "company" not in params:
                raise ArgumentValidationError(
                    f"For {key} operation should be defined domain or company"
                )
        if key == "email-finder":
            if "full_name" not in params and (
                "first_name" not in params or "last_name" not in params
            ):
                raise ArgumentValidationError(
                    "At least first_name and last_name or full_name should"
                    " be in params."
                )


VALIDATORS = {
    "required_arguments": (Validators.validate_required_arguments,),
    "domain": (Validators.validate_str,),
    "company": (Validators.validate_str,),
    "limit": (Validators.validate_int,),
    "offset": (Validators.validate_int,),
    "type": (Validators.validate_str, Validators.validate_str),
    "seniority": (Validators.validate_str, Validators.validate_seniority),
    "department": (Validators.validate_str, Validators.validate_department),
    "required_field": (Validators.validate_str, Validators.validate_required_field),
    "first_name": (Validators.validate_str,),
    "last_name": (Validators.validate_str,),
    "full_name": (Validators.validate_str,),
    "max_duration": (Validators.validate_int, Validators.validate_max_duration),
    "email": (Validators.validate_str, Validators.validate_email),
    "argument": (Validators.validate_str,),
}
