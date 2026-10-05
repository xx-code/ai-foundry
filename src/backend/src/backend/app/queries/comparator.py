from enum import StrEnum

class Comparator(StrEnum):
    EQUAL = "eq"
    NOT_EQUAL = "neq"
    IN = "in"
    NOT_IN = "not_in"

    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"

    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"

    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"

    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"