import json
import logging
from collections.abc import Iterable
from itertools import chain
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    SupportsFloat,
    SupportsInt,
    Union,
    cast,
)

import arrow

from oomnitza_rule_checker.helpers import DateHelper

__all__ = (
    "Op",
    "GroupOperation",
    "FieldDataType",
    "check_rules",
    "check_rule_by_op",
)


RuleType = Dict[str, Any]
DocumentType = Dict[str, Any]
LeftValueType = Optional[Union[str, int, float]]
RightValueType = Optional[Union[str, int, float, Dict[str, Any]]]
SerializedJsonType = Union[str, bytes]


class GroupOperation:
    OR = "or"
    AND = "and"


class FieldDataType:
    DATE = "DATE"
    DATETIME = "DATETIME"


class Op:
    EQUAL = "eq"
    NOT_EQUAL = "ne"
    LESS_THEN = "lt"
    LESS_OR_EQUAL = "le"
    GREATER_THEN = "gt"
    GREATER_OR_EQUAL = "ge"
    BEGINS_WITH = "bw"
    DOES_NOT_BEGIN_WITH = "nb"
    ENDS_WITH = "ew"
    DOES_NOT_END_WITH = "nw"
    CONTAINS = "cn"
    DOES_NOT_CONTAIN = "nc"
    IS_NULL = "nu"
    NOT_NULL = "nn"
    DAYS_AFTER = "da"
    DAYS_BEFORE = "db"
    DAYS_EQUAL = "do"
    HAS_BEEN_CHANGED = "hc"
    BETWEEN = "between"
    DAY_BEFORE_CURRENT_DATE = "day_before_current_date"
    DAY_AFTER_CURRENT_DATE = "day_after_current_date"
    LAST = "last"
    THIS = "this"
    NEXT = "next"
    BEFORE = "before"
    AFTER = "after"
    INCLUDE = "in"
    NOT_INCLUDE = "ni"
    STRICT_INCLUDE = "sin"
    STRICT_NOT_INCLUDE = "sni"


class DatePeriod:
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

    @classmethod
    def get_available_periods(cls) -> List[str]:
        return [cls.WEEK, cls.MONTH, cls.QUARTER, cls.YEAR]


DATE_ACTIONS = [
    Op.DAYS_AFTER,
    Op.DAYS_BEFORE,
    Op.DAYS_EQUAL,
    Op.IS_NULL,
    Op.NOT_NULL,
    Op.BETWEEN,
]


OBJECTS_WITHOUT_VERSION_FIELD = ["CONNECTOR_RUN_LOGS"]


logger = logging.getLogger(__name__)


_missed = object()

_oomnitza_version_key = "version"
_key_groupop = "groupOp"
_key_field = "field"


def _get_oomnitza_document_version(document: DocumentType) -> int:
    return int(document.get(_oomnitza_version_key, 0))


def _is_initial_document_version(
    document: DocumentType,
    object_type: str,
    changed_values: Optional[DocumentType],
) -> bool:
    if object_type in OBJECTS_WITHOUT_VERSION_FIELD:
        return not bool(changed_values)
    return _get_oomnitza_document_version(document) == 0


def _convert_string_to_timestamp(date_string: str) -> int:
    try:
        return cast(int, arrow.get(date_string).timestamp)
    except Exception as e:
        raise ValueError from e


def _is_numeric(value: Any) -> bool:
    """
    Simple method that check whether value can be converted to float.
    """
    try:
        float(value)
    except Exception:
        return False
    return True


def _is_iterable(value: Any) -> bool:
    """
    Simple method that check whether the data type is iterable.
    """
    return isinstance(value, Iterable)


def _is_json(value: Any) -> bool:
    """
    Simple method that check whether the data type is json.
    """
    try:
        json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return False
    return True


def check_rule_by_op(  # noqa: CCR001
    op: str,
    current_value: LeftValueType,
    target_value: RightValueType,
) -> bool:
    """
    Check current and target values according with the specified
    action type.
    """
    # prepare values
    left_value = (
        current_value.lower() if isinstance(current_value, str) else current_value
    )
    right_value = (
        target_value.lower() if isinstance(target_value, str) else target_value
    )

    if op in (
        Op.EQUAL,
        Op.NOT_EQUAL,
    ):
        if _is_numeric(left_value):
            left_value = float(cast(SupportsFloat, left_value))
        elif not left_value:
            left_value = None

        if _is_numeric(right_value):
            right_value = float(cast(SupportsFloat, right_value))
        elif not right_value:
            right_value = None

        if op == Op.EQUAL:
            return left_value == right_value
        elif op == Op.NOT_EQUAL:
            return left_value != right_value

    if op in (
        Op.INCLUDE,
        Op.STRICT_INCLUDE,
        Op.NOT_INCLUDE,
        Op.STRICT_NOT_INCLUDE,
    ):
        if _is_json(left_value):
            left_value = json.loads(cast(SerializedJsonType, left_value))

        if _is_json(right_value):
            right_value = json.loads(cast(SerializedJsonType, right_value))

        if (
            not _is_iterable(left_value) or not _is_iterable(right_value)
        ) or not left_value:
            return False

        # hints fo mypy
        assert not isinstance(left_value, float)  # noqa: S101
        assert not isinstance(right_value, float)  # noqa: S101
        assert left_value is not None  # noqa: S101
        assert right_value is not None  # noqa: S101

        if op == Op.INCLUDE:
            return any(item in right_value for item in left_value)
        elif op == Op.STRICT_INCLUDE:
            return all(item in right_value for item in left_value)
        elif op == Op.NOT_INCLUDE:
            return all(item not in right_value for item in left_value)
        elif op == Op.STRICT_NOT_INCLUDE:
            return any(item not in right_value for item in left_value)

    if op in (
        Op.LESS_THEN,
        Op.LESS_OR_EQUAL,
        Op.GREATER_THEN,
        Op.GREATER_OR_EQUAL,
    ):
        if _is_numeric(left_value):
            left_value = float(cast(SupportsFloat, left_value))
        else:
            return False

        if _is_numeric(right_value):
            right_value = float(cast(SupportsFloat, right_value))
        else:
            return False

        numeric_operation_mapping: Dict[str, Callable[[Any, Any], bool]] = {
            Op.LESS_THEN: lambda a, b: a < b,  # type: ignore [no-any-return]
            Op.LESS_OR_EQUAL: lambda a, b: a <= b,  # type: ignore [no-any-return]
            Op.GREATER_THEN: lambda a, b: a > b,  # type: ignore [no-any-return]
            Op.GREATER_OR_EQUAL: lambda a, b: a >= b,  # type: ignore [no-any-return]
        }
        return numeric_operation_mapping[op](left_value, right_value)

    elif op in (
        Op.BEGINS_WITH,
        Op.DOES_NOT_BEGIN_WITH,
        Op.ENDS_WITH,
        Op.DOES_NOT_END_WITH,
        Op.CONTAINS,
        Op.DOES_NOT_CONTAIN,
    ):
        # Handling case, when empty / nullable strings
        if not right_value:
            return op in (Op.BEGINS_WITH, Op.ENDS_WITH, Op.CONTAINS)

        if not left_value:
            return op in (Op.BEGINS_WITH, Op.ENDS_WITH, Op.CONTAINS)

        left_value = str(left_value).lower()
        right_value = str(right_value).lower()

        substring_operation_mapping: Dict[str, Callable[[Any, Any], bool]] = {
            Op.CONTAINS: lambda a, b: b in a,
            Op.DOES_NOT_CONTAIN: lambda a, b: b not in a,
            Op.BEGINS_WITH: lambda a, b: a.startswith(b),  # type: ignore [no-any-return]
            Op.DOES_NOT_BEGIN_WITH: lambda a, b: not a.startswith(b),
            Op.ENDS_WITH: lambda a, b: a.endswith(b),  # type: ignore [no-any-return]
            Op.DOES_NOT_END_WITH: lambda a, b: not a.endswith(b),
        }
        return substring_operation_mapping[op](left_value, right_value)

    elif op == Op.IS_NULL:
        return left_value in [None, "", []]

    elif op == Op.NOT_NULL:
        return left_value not in [None, "", []]

    elif op == Op.BETWEEN:
        # it is expected the right value has the form of
        # a json dumped string: '{"from": X, "to": Y}'
        # where X and Y are the border values given for the date field
        left_value = (
            int(cast(SupportsInt, left_value))
            if _is_numeric(left_value)
            else left_value
        )

        if not isinstance(right_value, dict):
            try:
                right_value = (
                    json.loads(cast(SerializedJsonType, right_value))
                    if right_value
                    else right_value
                )
            except (json.JSONDecodeError, TypeError):
                return False

        if (
            left_value is not None
            and right_value is not None
            and isinstance(left_value, int)
            and isinstance(right_value, dict)
        ):
            from_value: Optional[str] = right_value.get("from")
            to_value: Optional[str] = right_value.get("to")

            if from_value is None:
                return _is_numeric(to_value) and left_value <= int(
                    cast(SupportsInt, to_value),
                )

            if to_value is None:
                return _is_numeric(from_value) and int(from_value) <= left_value

            return (
                _is_numeric(from_value)
                and _is_numeric(to_value)
                and int(from_value) <= left_value <= int(to_value)
            )

        return False

    elif op in (
        Op.DAYS_AFTER,
        Op.DAYS_BEFORE,
        Op.DAYS_EQUAL,
    ):
        left_value = (
            int(cast(SupportsInt, left_value))
            if _is_numeric(left_value)
            else left_value
        )
        right_value = (
            int(cast(SupportsInt, right_value))
            if _is_numeric(right_value)
            else right_value
        )
        now = arrow.utcnow()

        if op == Op.DAYS_AFTER:
            return (
                left_value  # type: ignore [return-value]
                and (right_value or right_value == 0)
                and DateHelper.get_day_start(now, offset=-cast(int, right_value))
                <= cast(int, left_value)
                < DateHelper.get_day_start(now, offset=-(cast(int, right_value) - 1))
            )

        if op == Op.DAYS_BEFORE:
            return (
                left_value  # type: ignore [return-value]
                and (right_value or right_value == 0)
                and DateHelper.get_day_start(now, offset=cast(int, right_value))
                <= cast(int, left_value)
                < DateHelper.get_day_start(now, offset=cast(int, right_value) + 1)
            )

        if op == Op.DAYS_EQUAL:
            return (
                left_value  # type: ignore [return-value]
                and DateHelper.get_day_start(
                    now,
                    offset=-0,
                )
                <= cast(int, left_value)
                < DateHelper.get_day_start(now, offset=1)
            )

    elif op == Op.HAS_BEEN_CHANGED:
        # If both values represent a number
        if _is_numeric(left_value) and _is_numeric(right_value):
            left_value = float(cast(SupportsFloat, left_value))
            right_value = float(cast(SupportsFloat, right_value))
            return left_value != right_value

        # Note: testing the passed in values directly, because left_value and
        # right_value may be lowercase strings at this point.
        return target_value is not _missed and current_value != target_value

    elif op in (
        Op.DAY_BEFORE_CURRENT_DATE,
        Op.DAY_AFTER_CURRENT_DATE,
        Op.LAST,
        Op.THIS,
        Op.NEXT,
    ):
        if not _is_numeric(left_value) or (
            op in (Op.LAST, Op.NEXT, Op.THIS)
            and right_value not in DatePeriod.get_available_periods()
        ):
            return False

        interval_offsets = {
            Op.DAY_BEFORE_CURRENT_DATE: (-1, 0),
            Op.DAY_AFTER_CURRENT_DATE: (1, 2),
            Op.THIS: (0, 1),
            Op.NEXT: (1, 2),
            Op.LAST: (-1, 0),
        }

        if op in [
            Op.DAY_BEFORE_CURRENT_DATE,
            Op.DAY_AFTER_CURRENT_DATE,
        ]:
            right_value = DatePeriod.DAY

        now = arrow.utcnow()
        _from, _to = interval_offsets[op]
        return (
            DateHelper.get_start(cast(str, right_value), now, offset=_from)
            <= int(cast(SupportsInt, left_value))
            < DateHelper.get_start(cast(str, right_value), now, offset=_to)
        )

    elif op in (Op.BEFORE, Op.AFTER):
        if not isinstance(right_value, dict):
            try:
                right_value = (
                    json.loads(cast(SerializedJsonType, right_value))
                    if right_value
                    else right_value
                )
            except (json.JSONDecodeError, ValueError):
                return False

        if (
            not _is_numeric(left_value)
            or not isinstance(right_value, dict)
            or right_value.get("condition") not in (Op.BEFORE, Op.AFTER)
            or not _is_numeric(right_value.get("days"))
        ):
            return False

        operation_mapping: Dict[str, Callable[[Any, Any], bool]] = {
            Op.BEFORE: lambda a, b: a < b,  # type: ignore [no-any-return]
            Op.AFTER: lambda a, b: a > b,  # type: ignore [no-any-return]
        }
        days = int(right_value["days"])
        return operation_mapping[op](
            int(cast(SupportsInt, left_value)),
            DateHelper.get_day_start(
                arrow.utcnow(),
                offset=days if right_value["condition"] == Op.AFTER else -days,
            ),
        )

    return False


def _check_rules_for_group(  # noqa: CCR001
    rules: RuleType,
    document: DocumentType,
    changed_values: Optional[DocumentType],
    object_type: str,
) -> bool:
    if rules[_key_groupop] == GroupOperation.AND:
        for rule in chain(rules["groups"], rules["rules"]):
            has_match = check_rules(rule, document, changed_values, object_type)
            if not has_match:
                return False

        return True

    elif rules[_key_groupop] == GroupOperation.OR:
        # NOTE: There exists a corner case scenario with WF Begin Block where
        # Rules Set are empty but the Rules Operator set to the OR. So it
        # recognizing as a false negative scenario. AND operator is fine because
        # we are processing False -> True loop rather than True -> False inside OR
        rules_to_check = list(chain(rules["groups"], rules["rules"]))
        if not rules_to_check:
            return True

        for rule in rules_to_check:
            has_match = check_rules(rule, document, changed_values, object_type)
            if has_match:
                return True

        return False

    return False


def _get_prop_from_field(field_name: str, object_type: str) -> str:
    delim = f"{object_type}."
    if field_name.startswith(delim):
        _unused, prop = field_name.split(delim, 1)
    else:
        return field_name
    return prop


def _check_rules_for_rule(  # noqa: CCR001
    rules: RuleType,
    document: DocumentType,
    changed_values: Optional[DocumentType],
    object_type: str,
) -> bool:
    op = rules.get("op")
    value = rules.get("data", "")
    field_name = rules.get("field")
    item_type = rules.get("type")

    if not field_name or not op:
        return False

    prop = _get_prop_from_field(field_name, object_type)

    if isinstance(document, tuple):  # type: ignore [unreachable]
        # is this achievable?
        flag = False  # type: ignore [unreachable]

        for item in document[object_type]:
            if prop in item and check_rule_by_op(op, item[prop], value):
                flag = True
        return flag

    else:
        if item_type == FieldDataType.DATE and op not in DATE_ACTIONS and value:
            try:
                value = _convert_string_to_timestamp(value)

                if op in [
                    Op.LESS_THEN,
                    Op.LESS_OR_EQUAL,
                ]:
                    day_without_second = 86399
                    value += day_without_second

                value = str(value)
            except ValueError:
                logger.warning(f"{value!r} is not a valid date!")  # noqa: G004
                return False

        if item_type == FieldDataType.DATETIME:
            try:
                if value:
                    value = str(_convert_string_to_timestamp(value))
            except ValueError:
                logger.warning(f"{value!r} is not a valid date!")  # noqa: G004
                return False

        if op == Op.HAS_BEEN_CHANGED:
            value = (
                _missed
                if _is_initial_document_version(document, object_type, changed_values)
                else changed_values and changed_values.get(prop, _missed)
            )

        if prop not in document:
            logger.warning(
                f"There is no field {object_type}.{prop}. "  # noqa: G004
                "Probably it was deleted.",
            )
            return False

        current_value = document.get(prop)

        return check_rule_by_op(op, current_value, value)


def check_rules(
    rules: Optional[RuleType],
    document: DocumentType,
    changed_values: Optional[DocumentType],
    object_type: str,
) -> bool:
    args = [rules, document, changed_values, object_type]
    if rules is None or _key_groupop not in rules and _key_field not in rules:
        return True
    elif _key_groupop in rules:
        return _check_rules_for_group(*args)  # type: ignore
    else:
        return _check_rules_for_rule(*args)  # type: ignore
