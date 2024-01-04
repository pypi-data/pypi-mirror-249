from typing import cast

from arrow import Arrow


class DateHelper:
    @classmethod
    def get_day_start(cls, date: Arrow, offset: int = 0) -> int:
        return cast(int, date.floor("day").replace(days=offset).timestamp)

    @classmethod
    def get_week_start(cls, date: Arrow, offset: int = 0) -> int:
        # using american week format ==> Sun->Sat
        return cast(  # noqa: ECE001
            int,
            (
                date.replace(days=1)
                .floor("week")
                .replace(weeks=offset)
                .replace(days=-1)
                .timestamp
            ),
        )

    @classmethod
    def get_month_start(cls, date: Arrow, offset: int = 0) -> int:
        return cast(int, date.floor("month").replace(months=offset).timestamp)

    @classmethod
    def get_quarter_start(cls, date: Arrow, offset: int = 0) -> int:
        return cast(int, date.floor("quarter").replace(quarters=offset).timestamp)

    @classmethod
    def get_year_start(cls, date: Arrow, offset: int = 0) -> int:
        return cast(int, date.floor("year").replace(years=offset).timestamp)

    @classmethod
    def get_start(cls, period: str, date: Arrow, offset: int = 0) -> int:
        return cast(int, getattr(cls, f"get_{period}_start")(date, offset))
