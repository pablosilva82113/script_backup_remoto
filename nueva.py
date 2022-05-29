import pymysql

import os
from datetime import datetime

username = 'root'
password = '12345678'
hostname = '192.168.0.20'
hostname2 = 'localhost'
database = 'ejemplo'

#-----verificacmos el mes pertinente
date=datetime.now()
mes=date.strftime('%m')
year=date.strftime('%Y')
filestamp = date.strftime('%Y-%m-%d')

#-----creamos la carpeta si es que no existe
if not os.path.isdir(year):
 os.mkdir(year)

#------creamos la carpeta del mes, si es que no existe
nombre_carpeta = os.path.join(year, mes)
if not os.path.isdir(nombre_carpeta):
   os.mkdir(nombre_carpeta)

#---creamos la ruta con el mes pertinente
ruta=os.path.join(year,mes)

#---se copia el archivo a dicha carpeta
name_file = "{0}-{1}".format(filestamp,database)
os.popen("mysqldump.exe -h "+hostname+" -u "+username+" -p"+password+" ejemplo >"+ ruta + "/"+ name_file +".sql")
os.popen("mysql.exe -u "+username+" -p"+password+" ejemplo <"+ ruta + "/"+ name_file +".sql")


conexionMaster = pymysql.connect( host='127.0.0.1', user= 'root', passwd='12345678', db='ejemplo' )
cur = conexionMaster.cursor()
cur.execute( "SHOW MASTER STATUS;")
data = cur.fetchone()
binlog=data[0]
pos=int(data[1])
print(pos)
print(binlog)

conexionEsclavo = pymysql.connect( host='192.168.0.20', user= 'remoto', passwd='12345678', db='ejemplo' )
cursor = conexionEsclavo.cursor()
cursor.execute("STOP SLAVE;")
cursor.execute("CHANGE MASTER TO MASTER_HOST='192.168.0.16', MASTER_USER='esclavo', MASTER_PASSWORD='12345678', MASTER_LOG_FILE='"+binlog+"', MASTER_LOG_POS="+str(pos)+";")
cursor.execute("START SLAVE;")
cursor.execute("SHOW SLAVE STATUS;")