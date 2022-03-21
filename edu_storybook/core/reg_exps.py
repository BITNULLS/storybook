"""
reg_exps.py
    Contains all the regular expressions used in the app.
"""
import re

re_alphanumeric = re.compile(r"[a-zA-Z0-9]")
re_alphanumeric2 = re.compile(r"[a-zA-Z0-9]{2,}")
re_alphanumeric8 = re.compile(r"[a-zA-Z0-9!@#$%^&*_=+-]{8,}") # modified for passwords only
re_hex36dash = re.compile(r"[a-fA-F0-9]{36,38}")
re_hex36 = re.compile(r"[a-f0-9-]{36,}")  # for uuid.uuid4
re_hex32 = re.compile(r"[A-F0-9]{32,}")   # for Oracle guid()
re_email = re.compile(r"[^@]+@[^@]+\.[^@]+")
re_timestamp = re.compile(
    r"(\d{4})-(\d{1,2})-(\d{1,2}) (\d{2}):(\d{2}):(\d{2})")
re_redirect_link = re.compile(r"^/([\w.]*/?)*")
