# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re


def is_time_format(dt, time_format: str = '%Y-%m-%d %H:%M:%S') -> bool:
    try:
        datetime.strptime(dt, time_format)
    except ValueError:
        return False
    return True


def to_str(dt=None, dt_list=None):
    if dt_list:
        return list(map(lambda x: to_str(x), dt_list))
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else ""


def to_dt(s: str, time_format: str = '%Y-%m-%d %H:%M:%S'):
    if is_time_format(s, time_format):
        return datetime.strptime(s, time_format)
    return None


def start_of_hour(dt):
    return dt.replace(minute=0, second=0)


def end_of_hour(dt):
    return dt.replace(minute=59, second=59)


def start_of_day(dt):
    return dt.replace(hour=0, minute=0, second=0)


def end_of_day(dt):
    return dt.replace(hour=23, minute=59, second=59)


def start_of_week(dt):
    return start_of_day(dt + relativedelta(days=-dt.weekday()))


def end_of_week(dt):
    return start_of_week(dt) + relativedelta(days=7, seconds=-1)


def start_of_month(dt):
    return dt.replace(day=1, hour=0, minute=0, second=0)


def end_of_month(dt):
    return start_of_month(dt) + relativedelta(months=+1, seconds=-1)


def start_of_year(dt):
    return dt.replace(month=1, day=1, hour=0, minute=0, second=0)


def end_of_year(dt):
    return start_of_year(dt) + relativedelta(years=+1, seconds=-1)


def day(dt, offset: int):
    if offset > 0:
        return [start_of_day(dt), dt]
    end = end_of_day(dt) + relativedelta(days=offset) if offset < 0 else dt
    return [start_of_day(dt) + relativedelta(days=offset), end]


def week(dt, offset: int):
    if offset > 0:
        return [start_of_week(dt), dt]
    end = end_of_week(dt) + relativedelta(days=offset * 7) if offset < 0 else dt
    return [start_of_week(dt) + relativedelta(days=offset * 7), end]


def month(dt, offset: int):
    if offset > 0:
        return [start_of_month(dt), dt]
    end = end_of_month(dt) + relativedelta(months=offset) if offset < 0 else dt
    return [start_of_month(dt) + relativedelta(months=offset), end]


def season(dt, offset: int = None, order: int = None):
    start_of_season = dt.replace(month=int((dt.month - 1) / 3) * 3 + 1, day=1, hour=0, minute=0, second=0)
    if offset:
        start_of_season = start_of_season + relativedelta(months=+3 * offset)
    elif order:
        start_of_season = dt.replace(month=order * 3 - 2, day=1, hour=0, minute=0, second=0)
    if start_of_season > dt:
        start_of_season = start_of_season + relativedelta(years=-1)
    end_of_season = start_of_season + relativedelta(months=+3, seconds=-1)
    if end_of_season > dt:
        end_of_season = dt
    return [start_of_season, end_of_season]


def year(dt, offset: int):
    if offset > 0:
        return [start_of_year(dt), dt]
    end = end_of_year(dt) + relativedelta(months=offset) if offset < 0 else dt
    return [start_of_year(dt) + relativedelta(years=offset), end]


def parse_time_slot(s, now=datetime.now()):
    if '本周' in s or '这周' in s or '这个星期' in s or '这个礼拜' in s:
        return week(now, offset=0)
    elif '上周' in s or '上一周' in s or '上星期' in s or '上个星期' in s or '上礼拜' in s or '上个礼拜' in s:
        return week(now, offset=-1)
    elif '本季度' in s or '此季度' in s or '这个季度' in s:
        return season(now, offset=0)
    elif '上季度' in s or '上个季度' in s:
        return season(now, offset=-1)
    elif '1季度' in s:
        return season(now, order=1)
    elif '2季度' in s:
        return season(now, order=2)
    elif '3季度' in s:
        return season(now, order=3)
    elif '4季度' in s:
        return season(now, order=4)
    elif "," in s:
        ms = re.findall(r"\d{4}-\d{2}-\d{2}", s)
        if ms:
            start_datetime = start_of_day(to_dt(ms[0], "%Y-%m-%d"))
            end_datetime = end_of_day(to_dt(ms[-1], "%Y-%m-%d"))
            if end_datetime > now:
                end_datetime = now
            return [start_datetime, end_datetime]
    elif re.match(r"最近(\d+)个月", s):
        m = re.findall(r"\d+", s)
        if m:
            mm = int(m[0])
            return [month(now, -mm)[0], now]
    elif re.match(r"最近(\d+)天", s):
        d = re.findall(r"\d+", s)
        if d:
            dd = int(d[0])
            return [day(now, -dd)[0], now]

    return []


def parse_year_offset(s):
    offset = None
    if '今年' in s or '本年度' in s:
        offset = 0
    elif '去年' in s or '上年度' in s or '上个年度' in s:
        offset = -1
    elif '前年' in s or '前年度' in s:
        offset = -2
    return offset


def parse_month_offset(s):
    offset = None
    if '当月' in s or '本月' in s or '这个月' in s:
        offset = 0
    elif '上月' in s or '上个月' in s:
        offset = -1
    return offset


def parse_day_offset(s):
    offset = None
    if '当天' in s or '今天' in s or '今日' in s or '本日' in s:
        offset = 0
    elif '昨天' in s or '前一天' in s or '昨日' in s or '前一日' in s:
        offset = -1
    elif '前天' in s:
        offset = -2
    return offset


def parse_time_slot_of_day(s):
    if "凌晨" in s:
        return [0, 6]
    elif "早上" in s or "早晨" in s:
        return [6, 10]
    elif "中午" in s:
        return [10, 14]
    elif "下午" in s:
        return [14, 17]
    elif "晚上" in s or "傍晚" in s:
        return [17, 24]
    return []


def parse_time_value(s):
    re1 = re.findall(r"\d{4}年", s)
    re2 = re.findall("([1-9]|1[0-2])月", s)
    re3 = re.findall("([1-2]|[1-3]*[0-9])[日号]", s)
    re4 = re.findall("([1-2]|[1-2]*[0-9])[时点]", s)

    y = int(re1[0].replace('年', '')) if re1 else None
    m = int(re2[0].replace('月', '')) if re2 else None
    d = int(re3[0].replace('日', '').replace('号', '')) if re3 else None
    h = int(re4[0].replace('时', '').replace('点', '')) if re4 else None

    time_slot_of_day = parse_time_slot_of_day(s)
    if time_slot_of_day and h:
        if time_slot_of_day[0] <= h + 12 <= time_slot_of_day[1]:
            h = h + 12

    return y, m, d, h


"""
 now: 解析时间的标准对照日期，处理工单时该时间是工单创建时间；
 default_empty: 在解析字符串未解析成合法时间时，返回空字符串。
"""


def parse_ymd(s, now=datetime.now(), default_empty: bool = False):
    s = s.replace(' ', '')
    num_dict = {'三十一': '31', '三十': '30', "二十九": "29", "二十八": "28", "二十七": "27", "二十六": "26",
                "二十五": "25", '二十四': '24', "二十三": "23", "二十二": "22", "二十一": "21", "二十": "20",
                "十九": "19", '十八': '18', "十七": "17", "十六": "16", "十五": "15", "十四": "14",
                "十三": "13", '十二': '12', "十一": "11", "十": "10", "九": "9", "八": "8",
                "七": "7", '六': '6', "五": "5", "四": "4", "三": "3", "二": "2", "一": "1", "零": "0"}
    # TODO: 中文数字从大到小匹配，从小到大会导致重复匹配
    for num in num_dict:
        s = s.replace(num, num_dict[num])

    if re.search("[到~]", s):  # TODO: 字符串分割解析
        idx = re.search("[到~]", s).start()
        return [parse_ymd(s[:idx], now, default_empty)[0], parse_ymd(s[idx + 1:], now, default_empty)[1]]

    start_end_time = parse_time_slot(s, now)
    start_datetime, end_datetime = "", ""
    if start_end_time:
        start_datetime, end_datetime = start_end_time[0], start_end_time[1]
    else:
        y_value, m_value, d_value, h_value = parse_time_value(s)
        y_offset, m_offset, d_offset = parse_year_offset(s), parse_month_offset(s), parse_day_offset(s)
        time_slot_of_day = parse_time_slot_of_day(s)

        y_range_cond = ((y_value or y_offset is not None) and not m_value and not d_value and not h_value and m_offset
                        is None and d_offset is None)
        m_range_cond = (m_value or m_offset is not None) and not d_value and not h_value and d_offset is None
        d_range_cond = (d_value or d_offset is not None) and not h_value and not time_slot_of_day
        h_range_cond = h_value or time_slot_of_day

        y_offset = y_offset if y_offset else 0
        m_offset = m_offset if m_offset else 0
        d_offset = d_offset if d_offset else 0

        y = y_value if y_value else now.year
        m = m_value if m_value else now.month
        d = d_value if d_value else now.day
        h = h_value if h_value else now.hour

        if y_range_cond:
            start_datetime = start_of_year(datetime(y, 1, 1)) + relativedelta(years=y_offset)
            end_datetime = end_of_year(start_datetime)
        elif m_range_cond:
            start_datetime = start_of_month(datetime(y, m, 1)) + relativedelta(months=m_offset, years=y_offset)
            if start_datetime > now:
                start_datetime += relativedelta(years=-1)
            end_datetime = end_of_month(start_datetime)
        elif d_range_cond:
            start_datetime = start_of_day(datetime(y, m, d)) + relativedelta(days=d_offset, months=m_offset,
                                                                             years=y_offset)
            if start_datetime > now:
                if m_value:
                    start_datetime += relativedelta(years=-1)
                elif d_value:
                    start_datetime += relativedelta(months=-1)
            end_datetime = end_of_day(start_datetime)
        elif h_range_cond:
            if h_value:
                start_datetime = start_of_hour(datetime(y, m, d, h)) + relativedelta(days=d_offset, month=m_offset,
                                                                                     years=y_offset)
                if start_datetime > now:
                    if m_value:
                        start_datetime += relativedelta(years=-1)
                    elif d_value:
                        start_datetime += relativedelta(months=-1)
                end_datetime = end_of_hour(start_datetime)

            elif time_slot_of_day:
                start_datetime = start_of_hour(datetime(y, m, d, time_slot_of_day[0])) + relativedelta(days=d_offset,
                                                                                                       month=m_offset,
                                                                                                       years=y_offset)
                if start_datetime > now:
                    if m_value:
                        start_datetime += relativedelta(years=-1)
                    elif d_value:
                        start_datetime += relativedelta(months=-1)
                end_datetime = end_of_hour(start_datetime.replace(hour=time_slot_of_day[1]))

        if start_datetime and start_datetime > now:
            start_datetime = start_of_day(now)
        if end_datetime and end_datetime > now:
            end_datetime = now

    if not start_datetime and not end_datetime and not default_empty:
        start_datetime = start_of_day(now)
        end_datetime = now

    return to_str(dt_list=[start_datetime, end_datetime])


def parse_duration(s):
    def get_leading_int(s):
        n = re.sub(r"[^0-9]", "", s)
        if len(n) > 0:
            return int(n)
        return 0

    s = s.replace(' ', '')
    duration = 0  # seconds

    # days
    r = re.findall(r"[0-9]*[天日]", s)
    if len(r) > 0:
        duration += 86400 * get_leading_int(r[0])

    # hours
    r = re.findall(r"[0-9]*(?:小时|个小时|个半小时|钟|个钟|个台班|个点)", s)
    if len(r) > 0:
        duration += 3600 * get_leading_int(r[0])

    # half hour
    if "个半小时" in s or "个半钟" in s or "个半点" in s:
        duration += 1800

    # minutes
    r = re.findall(r"[0-9]*(?:分|个分)", s)
    if len(r) > 0:
        duration += 60 * get_leading_int(r[0])

    # seconds
    r = re.findall(r"[0-9]*秒", s)
    if len(r) > 0:
        duration += get_leading_int(r[0])

    return duration
