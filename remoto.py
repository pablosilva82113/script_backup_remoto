#conexion remota esclvo maestro de la conexion
import sys
import os
import pymysql

try:
    conexion = pymysql.connect(host='localhost', user='root', passwd='12345678', db='ejemplo')
except:
    print("No se pudo conectar a la base de datos")
    sys.exit()

cur = conexion.cursor()
cur.execute("SHOW MASTER STATUS;")
data = cur.fetchone()
binlog=data[0]
pos=int(data[1])
print(pos)
print(binlog)

conexionEscalvo = pymysql.connect(host='192.168.0.16', user='remoto', passwd='12345678', db='ejemplo')
cursor = conexionEscalvo.cursor()
cursor.execute("STOP SLAVE;")
cursor.execute("CHANGE MASTER TO MASTER_HOST='192.168.0.20', MASTER_USER='esclavo', MASTER_PASSWORD='12345678', MASTER_LOG_FILE='"+binlog+"', MASTER_LOG_POS="+str(pos)+";")
cursor.execute("START SLAVE;")
cursor.execute("SHOW SLAVE STATUS;")
conexionEscalvo.close()
conexion.close()
