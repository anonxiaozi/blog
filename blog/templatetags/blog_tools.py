#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from django import template


register = template.Library()


@register.simple_tag(name='url_splice', takes_context=True)
def url_splice(context, blog_id, action):
    url = context + blog_id + '/' + action
    print(url)
    return url


