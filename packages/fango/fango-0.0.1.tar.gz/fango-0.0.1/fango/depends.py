
from fastapi import Request
from paginator.cursor import CursorPagination


def get_paginator(request: Request):
    return CursorPagination(request)
