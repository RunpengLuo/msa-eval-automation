import os
import sys


def parse_quote(s: str):
    if s[0] in ['\'', '\"'] and s[-1] in ['\'', '\"']:
        return s[1:-1]
    return s

def get_dir(s: str):
    return s if s[-1] != '/' else s[:-1]