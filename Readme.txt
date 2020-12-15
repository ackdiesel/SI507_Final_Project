Required libraries:

import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd 
import plotly.express as go

Instructions:

Users are prompted via command line to insert a country name, given the option to view proper formatting for spelling by typing 'countries'. Upon entry of a country name, the program fetches data from one source about the Travel Advisory Risk Level (1-4) as determined by the CDC for that country and that is communicated to the user via command line. The program also fetches data specific to the date of use on the selected country's new cases, new deaths, global rank by total cases, the number of people per new case, and the number of people per new death. These metrics are also communicated to the user via command line. Finally, using Plotly, a bar graph is generated in order to give the user a visual representation of the new case rate and new death rates.