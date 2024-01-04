from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_proper_default_datetime(
    day_offset: int, update_hour: int = 0, update_minute: int = 0
) -> datetime:
    """현재 시간 기준으로 어제 날짜를 반환합니다.

    @param day_offset: 갱신시간에 갱신되는 데이터가 오늘인지 어제인지에 따라 숫자를 지정합니다 (0: 오늘, 1: 어제)
    @param hour: 갱신 시간의 시간을 지정합니다
    @param minute: 갱신 시간의 분을 지정합니다
    """
    now = datetime.now(tz=ZoneInfo("Asia/Seoul"))
    update_time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=update_hour,
        minute=update_minute,
        tzinfo=ZoneInfo("Asia/Seoul"),
    )

    adjusted_time: datetime

    return (
        update_time - timedelta(days=day_offset)
        if now > update_time
        else update_time - timedelta(days=day_offset + 1)
    )


def to_date_string(min: datetime, date: datetime) -> str:
    min_date = get_kst_datetime(min)
    target_date = get_kst_datetime(date)
    if target_date < min_date:
        raise ValueError(
            f'You can only retrieve data after {min_date.strftime("%Y-%m-%d")}'
        )
    return target_date.strftime("%Y-%m-%d")


def get_kst_datetime(date: datetime) -> datetime:
    """datetime 객체를 KST datetime 객체로 변환합니다.

    datetime.astimezone()을 사용하면 지역에 따라 다른 결과가 나오고 date.replace()에도 버그가 존재하므로 datetime으로 재설정합니다.
    """
    return datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        tzinfo=ZoneInfo("Asia/Seoul"),
    )
