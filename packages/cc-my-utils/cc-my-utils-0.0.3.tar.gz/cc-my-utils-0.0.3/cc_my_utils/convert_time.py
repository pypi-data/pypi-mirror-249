#!/usr/bin/env python3

import pytz
import datetime


class ConvertTime:

    @staticmethod
    def str_to_obj(time_str, to_str: str):
        return datetime.datetime.fromisoformat(time_str)
    
    @staticmethod
    def str_to_app(time_str, app: str):
        time_obj = datetime.datetime.fromisoformat(time_str)
        if app == 'notion':
            format_time = time_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
            return format_time
        elif app == 'str':
            return time_obj.strftime('%Y-%m-%d %H:%M:%S')

