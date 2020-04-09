#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from logging import Filter
import re


class RecordOP(Filter):
    """
    记录update、delete以及操作时间大于1s的数据库操作
    """

    def filter(self, record):
        msg = record.getMessage().lower()
        if 'update' in msg or 'delete' in msg:
            return True
        elif hasattr(record, 'duration'):
            if record.duration > 1:
                return True
        return False


class ExcludeTemplateKeyError(Filter):
    """
    排除模板中的KeyError报错
    """

    def filter(self, record):
        msg = record.getMessage()
        if re.findall(r'Exception while resolving.+?in template', msg):
            return False
        else:
            return True
