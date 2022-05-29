import datetime
import os
import mysql.connector
command = "mysqldump -h 192.168.0.20 -u esclavo -p  ejemplo"
# Objeto HOY
today = datetime.date.today()
# Formatea como YYYYMMDD
fecha = today.strftime("%Y%m%d")
# Fichero de salida
file = "backup_Servidor_"+fecha
command = command+" > "+file+".sql"
os.system(command)

