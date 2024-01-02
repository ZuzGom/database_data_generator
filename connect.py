import pyodbc 
def get_cursor():
    cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=dbmanage.lab.ii.agh.edu.pl;Database=u_magorski;Port=1433;User ID=u_magorski;Password=xxxxxxxx')
    return cnxn.cursor()
   
   
