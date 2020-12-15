import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd 
import plotly.express as go

conn = sqlite3.connect('travel_table.sqlite')
cur = conn.cursor()

create_table = '''
    CREATE TABLE IF NOT EXISTS "Rate_Table1" (
        "#"                 INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "Country"           TEXT NOT NULL,
        "New Cases"         INTEGER NOT NULL,
        "New Deaths"        INTEGER NOT NULL,
        "1 Case/X Ppl"      INTEGER NOT NULL,
        "1 Death/X Ppl"     INTEGER NOT NULL
    )
'''
cur.execute(create_table)

countries_list = [
    'usa', 'india', 'brazil', 'russia', 'france', 'uk', 'italy', 'turkey', 'spain', 
    'argentina', 'colombia', 'germany', 'mexico', 'poland', 'iran', 'peru', 'ukraine', 
    'south africa', 'indonesia', 'netherlands', 'belgium', 'czechia', 'iraq', 'chile', 
    'romania', 'bangladesh', 'canada', 'philippines', 'pakistan', 'morocco', 'switzerland', 
    'saudi arabia', 'israel', 'portugal', 'austria', 'sweden', 'hungary', 'serbia', 'jordan', 
    'nepal', 'ecuador', 'panama', 'georgia', 'uae', 'bulgaria', 'japan', 'croatia', 'azerbaijan', 
    'belarus', 'dominican republic', 'costa rica', 'armenia', 'bolivia', 'lebanon', 'kuwait', 
    'kazakhstan', 'qatar', 'slovakia', 'guatemala', 'moldova', 'oman', 'greece', 'egypt', 'ethiopia', 
    'honduras', 'tunisia', 'denmark', 'palestine', 'myanmar', 'venezuela', 'bosnia and herzegovina', 
    'slovenia', 'paraguay', 'lithuania', 'algeria', 'kenya', 'libya', 'bahrain', 'malaysia', 'kyrgyzstan', 
    'ireland', 'uzbekistan', 'north macedonia', 'nigeria', 'singapore', 'ghana', 'afghanistan', 'albania', 
    's. korea', 'luxembourg', 'montenegro', 'el salvador', 'norway', 'sri lanka', 'finland', 'australia', 
    'uganda', 'latvia', 'cameroon', 'ivory coast', 'sudan', 'zambia', 'estonia', 'madagascar', 'senegal', 
    'mozambique', 'namibia', 'angola', 'french polynesia', 'cyprus', 'drc', 'guinea', 'maldives', 'tajikistan', 
    'botswana', 'french guiana', 'jamaica', 'cabo verde', 'zimbabwe', 'malta', 'mauritania', 'uruguay', 'haiti', 
    'cuba', 'gabon', 'belize', 'syria', 'guadeloupe', 'réunion', 'bahamas', 'hong kong', 'andorra', 
    'trinidad and tobago', 'eswatini', 'rwanda', 'malawi', 'congo', 'guyana', 'nicaragua', 'mali', 'djibouti', 
    'martinique', 'iceland', 'mayotte', 'suriname', 'equatorial guinea', 'aruba', 'car', 'somalia', 'thailand', 
    'burkina faso', 'gambia', 'curaçao', 'togo', 'south sudan', 'benin', 'guinea-bissau', 'sierra leone', 'niger', 
    'lesotho', 'new zealand', 'yemen', 'channel islands', 'san marino', 'chad', 'liberia', 'liechtenstein', 
    'vietnam', 'sint maarten', 'gibraltar', 'sao tome and principe', 'mongolia', 'saint martin', 'turks and caicos', 
    'taiwan', 'burundi', 'papua new guinea', 'diamond princess', 'eritrea', 'monaco', 'comoros', 'faeroe islands', 
    'mauritius', 'tanzania', 'bhutan', 'bermuda', 'isle of man', 'cambodia', 'cayman islands', 'barbados', 
    'saint lucia', 'seychelles', 'caribbean netherlands', 'st. barth', 'brunei', 'antigua and barbuda', 
    'st. vincent grenadines', 'dominica', 'british virgin islands', 'grenada', 'macao', 'fiji', 'laos', 'new caledonia', 
    'timor-leste', 'vatican city', 'saint kitts and nevis', 'greenland', 'falkland islands', 'solomon islands', 
    'saint pierre miquelon', 'montserrat', 'western sahara', 'anguilla', 'ms zaandam', 'marshall islands', 
    'wallis and futuna', 'samoa', 'vanuatu', 'china']

def rate_webscrape():
    '''
    Below is the code for web scraping country-specific covid rate data,
    which is then parsed, formatted, fit to a table, and extracted to 
    a file named 'covid_rates_table'.
    '''
    rate_url = 'https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?"%20%5CI%20"countries"'
    rate_response = requests.get(rate_url)
    rate_soup = BeautifulSoup(rate_response.text, 'html.parser')

    table = rate_soup.find("table", attrs={"id": "main_table_countries_today"})

    columns = table.find_all("th")
    #for c in rate_soup.find_all('br'):
    #    c.replace_with(' ')

    column_names = []
    for c in columns:
        column_names.append(c.get_text())
    #print(column_names)

    rows = table.find("tbody").find_all("tr")

    l = []
    for tr in rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)

    df = pd.DataFrame(l, columns=column_names)
   
    for i in range(0, len(df)):  
        insert_row = '''
            INSERT INTO Rate_Table1
            VALUES (NULL, ?, ?, ?, ?, ?)
            '''
        values_list = [
            df.iloc[i]['Country,Other'], df.iloc[i]['NewCases'], df.iloc[i]['NewDeaths'], 
            df.iloc[i]['1 Caseevery X ppl'], df.iloc[i]['1 Deathevery X ppl']
            ]
        cur.execute(insert_row, values_list)
    conn.commit()

def db_processing_and_graphs(input_response):
    db_query = """
    SELECT *
    FROM Rate_Table1
    WHERE COUNTRY = '{country}'
    """
    
    if input_response in ['uk', 'usa']:
        country = input_response.upper()
    else:
        country = input_response.capitalize()

    cur.execute(db_query.format(country=country))
    result = cur.fetchall()
    answer = result[0]
 
    print("Worldwide country rank, by total number of cases: " + str(answer[0]))
    print("New cases today: " + str(answer[2]))
    print("New deaths today: " + str(answer[3]))
    print("New case per " + str(answer[4]) + " number of people")
    print("New death per " + str(answer[5]) + " number of people")
    
    
    fig = go.bar(x=["New Cases", "New Deaths"], y=[answer[2], answer[3]], labels=dict(x="Metric", y="Incidence today"))
    fig.show()

def travel_webscrape(input_response):
    '''
    Below is the code for web scraping country-specific travel 
    restrictions (in the form of Levels 1-4) put in place due to COVID spread.
    '''
    base_travel_url = 'https://wwwnc.cdc.gov/travel/notices/covid-4/coronavirus-'
    
    if input_response in ("uk", "UK"):
        input_response = "united-kingdom"
    country_travel_url = input_response
    travel_url = base_travel_url + country_travel_url
    travel_response = requests.get(travel_url)
    travel_soup = BeautifulSoup(travel_response.text, 'html.parser')
    travel_level = travel_soup.find("div", class_="notice-typename-covid-4 p-2").get_text()

    print("For your selected country, the CDC has designated it: " + travel_level + ".")

def interactive_prompt():
    input_response = ''

    while input_response != 'exit':
        print("Welcome to the COVID travel safety check program, where you can compare the CDC recommended travel guideline with currend covid rate information!")
        print("Enter a country! Is it safe for you to travel there?")
        print("Note: For a list of countries in their proper search format, type 'countries'. For help, type in 'help'.")
        input_response = input('Choose a country: ')

        if input_response == 'help':
            print("Type in the name of any country. Note your spelling. Case sensitivity does not apply.")
            continue
        elif input_response == 'countries':
            print("Enter one of the following countries, spelled the same way: ") 
            print(countries_list)
        elif input_response in ('us', 'US', 'usa', 'USA'):
            print("Sorry, we do not currently have data on the United States. Try again with another country.")
        elif input_response.lower() in countries_list:
            rate_webscrape()
            travel_webscrape(input_response)
            db_processing_and_graphs(input_response)
            print("With this new information in mind, we urge you to consider the risk of contracting or spreading COVID-19 should you decide to travel. Stay safe!")
        else:
            print("Invalid input. Please check your spelling and try again.")
    
    else:
        conn.close()
        quit()

if __name__=="__main__":
    interactive_prompt()