import pymysql

import os
import datetime

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

command = "mysqldump -h 192.168.0.20 -u esclavo -p  ejemplo"
# Objeto HOY
today = datetime.date.today()
# Formatea como YYYYMMDD
fecha = today.strftime("%Y%m%d")
# Fichero de salida
file = "backup_Servidor_"+fecha
command = command+" > "+file+".sql"
os.system(command)
