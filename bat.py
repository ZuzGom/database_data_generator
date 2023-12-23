from datetime import datetime, timedelta
from mysql.connector import connect, Error
import requests
from bs4 import BeautifulSoup

'''
def track():
    try:
        page = requests.get('https://github.com/ZuzGom/remote/blob/main/url.txt')
    except requests.exceptions.ConnectionError:
        linia = None
    else:       
        soup = BeautifulSoup(page.content, 'html.parser')
        linia = str(soup.find("td", {"id": "LC1"})).split()[-1][9:-5]                        
    return linia
'''

# funnkcja która zwraca url bazy
def tcp():
    try:
        page = requests.get('https://github.com/ZuzGom/remote/blob/main/tcp.txt')
    except requests.exceptions.ConnectionError:
        linia = None
    else:       
        soup = BeautifulSoup(page.content, 'html.parser')
        linia = str(soup.find("td", {"id": "LC1"})).split()[-1][9:-5]                        
    return linia
u_tcp = tcp().split(':')
host=u_tcp[1][2:]
port=u_tcp[2]
'''Stare polaczenie do starej bazy
def pol_old():
    try:
        connection = connect(
            host="ekonomik.atthost24.pl",
            user="18013_earp",
            password="earp.123",
            database="18013_earp"
        )
        return connection
    except Error as e:
        print(e)
'''
#Function which connect with database
def polaczenie():
    try:
        connection = connect(
        #Tutaj trzeba wpisac HOSTA
            host=host,
            port=port,
            user="ul",
            password="earp123",
            database="Dane"
        )
        return connection
    except Error as e:
        print(e)
        
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error:
        result = None
        return result


#Function which gives data to database
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print("The error " + str(e) + " occurred")


#Important function, which download live information about bees house
def get_inf():
    connection = polaczenie()

    if(connection!=None):
        select_query = "SELECT temperature, AdditionalTemperature, Weight, Humidity, Date, Time FROM Measurements"
        query = execute_read_query(connection, select_query)[-1]

        connection.close()

        #Temperature inside - temp1
        temp1 = str(query[0])

        #Temperature outside - temp2
        temp2 = str(query[1])

        #Zuzia solution
        waga = str(int(float(query[2]))/1000)

        humi = str(query[3])
        kalendarz = str(query[4])
        zegar = str(query[5])

        data = kalendarz + "\n" + zegar
        temp= "zew: "+ temp1 + '°C\nwew: ' + temp2 + '°C'

        return data, temp, waga + 'kg', humi + '%'

    else:
        temp='zew: 0°C\nwew: 0°C'
        waga='0'
        humi='0'
        data = "00-00-0000 \n 00:00:00"

        return data, temp, waga + 'kg', humi + "%"

#print(get_inf())

#Function for Zuzia, check if the time is updatet
def data():
    now = datetime.now()
    return str(now)


#Future function
#return 2D tables with data included from now to some date
def get_all(dni):
    date = datetime.now()-timedelta(minutes=dni)
            #od tej daty

    #data, godzina, temp_wew, temp_zew, wilgotnosc, waga
    tab = [
    ['77112020-01-17',' 18:48:09',' 22','24',' 54',' 0'],
    ['77212020-01-17',' 18:48:14',' 23','22',' 55',' 0'],
    ['77312020-01-17',' 18:48:19',' 23','28',' 59',' 0'],
    ['77412020-01-17',' 18:48:24',' 23','28',' 56',' 0'],
    ['77512020-01-17',' 18:48:29',' 23','29',' 54',' 0'],
    ['77612020-01-17',' 18:48:34',' 23','22',' 54',' 0']
    ]
    return tab


#Function return 'tab[]' to TODAY graph
def get_all_day():
    teraz = datetime.now()
    dzien = str(teraz.day)
    miesiac = str(teraz.month)
    rok = str(teraz.year)

    tab = []
    connection = polaczenie()

    if(connection!=None):
        select_query = "SELECT Day, Month, Year, Hour, Minute, Temperature, AdditionalTemperature, Humidity, Weight FROM Measurements WHERE Day = " + dzien + " AND Month = " + miesiac + " AND Year = " + rok
        query = execute_read_query(connection, select_query)

        connection.close()

        for x in query:
            line = [(x[:3]),(x[3:5])] + list(x[5:])
            line[-1]=int(float(line[-1]))/1000
            tab.append(line)

    return tab


#Function return 'tab[]' to hour back graph
def get_all_hour():
    teraz = datetime.now()
    minuta = str(teraz.minute)
    godzina = str(teraz.hour)
    dzien = str(teraz.day)
    miesiac = str(teraz.month)
    rok = str(teraz.year)

    tab = []
    connection = polaczenie()

    if(connection!=None):
        select_query = "SELECT Day, Month, Year, Hour, Minute, Temperature, AdditionalTemperature, Humidity, Weight FROM Measurements WHERE ((Hour=" + str(int(godzina)-1) + " AND Minute<=" + minuta + " ) AND Day=" + dzien + " AND Month = " + miesiac + " AND Year = " + rok + ") OR (( Hour = " + str(int(godzina)-2) + " AND Minute >= " + minuta + " ) AND Day = " + dzien + " AND Month = " + miesiac + " AND Year = " + rok + ")"
        query = execute_read_query(connection, select_query)

        connection.close()

        for x in query:
            line = [(x[:3]), (x[3:5])] + list(x[5:])
            line[-1] = int(float(line[-1])) / 1000
            tab.append(line)

    return tab


#Function return 'tab[]' to month back graph
def get_all_month():
    teraz = datetime.now()
    dzien = str(teraz.day)
    miesiac = str(teraz.month)
    rok = str(teraz.year)

    tab = []
    connection = polaczenie()

    if(connection!=None):
        select_query = "SELECT Day, Month, Year, Hour, Minute, Temperature, AdditionalTemperature, Humidity, Weight FROM Measurements WHERE (Day <= " + dzien + " AND Month = " + miesiac + " AND Year = " + rok + " ) OR ( Day >= " + dzien + " AND Month = " + str(int(miesiac)-1) + " AND Year = " + rok + ")"
        query = execute_read_query(connection, select_query)

        connection.close()

        for x in query:
            line = [(x[:3]), (x[3:5])] + list(x[5:])
            line[-1] = int(float(line[-1])) / 1000
            tab.append(line)
            
    return tab


#Function return 'tab[]' since begin of the year 
def get_all_year():
    teraz = datetime.now()
    rok = str(teraz.year)

    tab = []
    connection = polaczenie()

    if(connection!=None):
        select_query = "SELECT Day, Month, Year, Hour, Minute, Temperature, AdditionalTemperature, Humidity, Weight FROM Measurements WHERE Year = " + rok
        query = execute_read_query(connection, select_query)

        connection.close()

        for x in query:
            line = [(x[:3]), (x[3:5])] + list(x[5:])
            line[-1] = int(float(line[-1])) / 1000
            tab.append(line)

    return tab


#Function works
def push_alert(id, error, tresc):
    connection = polaczenie()
    
    if(connection!=None):
        inserting_error = "INSERT INTO Alerty ( id, error, tekst ) VALUES ( " + str(id) + ", " + str(error) + ", \"" + tresc + "\" )"
        execute_query(connection, inserting_error)
    
    connection.close()
    

#Function return 'tab[]' with last 5 records from table - Alerty
def get_err():
    connection = polaczenie()
    tab = []
    
    if(connection!=None):
        select_query = "SELECT * FROM Alerty WHERE id>=0 ORDER BY data DESC LIMIT 5"
        query = execute_read_query(connection, select_query)

        connection.close()

        for x in query:
            line = x
            tab.append(line)
    
    return tab


'''
def get_ule(id):
    
    ta przyszłościowa funkcja służy do pobierania informacji z tabli 'user' z indeksu ule
    taki indeks trzeba dopiero stworzyć
    lista ule zawiera indeksy uli przypisane do id użytkownika
    
    ule = [1,2]
    return ule

'''
