"""
Path: backend/src/application/ayudante_fechas.py
"""

from datetime import datetime
import calendar

def agregar_meses(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day)
