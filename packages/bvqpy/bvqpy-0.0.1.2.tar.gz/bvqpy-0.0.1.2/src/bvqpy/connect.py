"""
Authenticate in Google and formr
"""

import requests
import csv
import gspread
import gspread
import requests

def connect(email, password):
    """
    This function tries to log in to the formr API with the user-provided password (argument password).
    """

    r = requests.get('https://formr.org', auth=(email, password))
    if (r.status_code == 200):
        print("Connected to formr!")
    else:
        print("Failed to connect: Error " + r.status_code)

    return gspread.oauth()
    