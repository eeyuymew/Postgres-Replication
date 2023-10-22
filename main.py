import psycopg2
import sys
import time
import os, platform
from psycopg2 import Error

def check_connection(check_ip):
    try:
        connection = psycopg2.connect(user="postgres", password="qwerty", host=check_ip, port="5432",
                                        database="dbtest")
        cursor = connection.cursor()
        sql_query = 'select 1;'
        cursor.execute(sql_query)
        connection.commit()
        print("БД доступна.")
    except (Exception, Error) as error:
         print("БД недоступна.")

def check_ping(hostname):
    response = os.system("ping -c 1 " + hostname + "  >null")
    return response == 0

def Replication_process(Primary_ip, Standby_ip):
    id = 1
    flag_promote = False
    flag_master_drop = False
    while ( True ):
        if ( check_ping(Primary_ip) and flag_master_drop == False ):
            print(f"[{id}] Связь с Master есть.")
            check_connection(Primary_ip)

        if ( not check_ping(Primary_ip) and check_ping(Standby_ip) ):
            print(f"[{id}] [Master недоступен, переключение на StandBy].")
            check_connection(Standby_ip)
            flag_master_drop = True
            if (flag_promote == False):
                os.system(f"ssh -i C:/Users/andre/.ssh/id_rsa replicator@{Standby_ip} '/usr/lib/postgresql/13/bin/pg_ctl promote -D /var/lib/postgresql/13/main'")
                flag_promote = True
                print("[StandBy переведен в основной режим].")

        if ( check_ping(Primary_ip) and flag_master_drop ):
            print((f"[{id}] Связь с Master восстановлена."))
            check_connection(Primary_ip)
            try:
                os.system(f"ssh -i C:/Users/andre/.ssh/id_rsa admin@{Primary_ip} 'rm -rf /var/lib/postgresql/13/main; mkdir /var/lib/postgresql/13/main; chmod go-rwx /var/lib/postgresql/13/main | pg_basebackup -P -R -X stream -c fast -h {Standby_ip} -U postgres -D /var/lib/postgresql/13/main | sudo systemctl restart postgresql'")
                os.system(f"ssh -i C:/Users/andre/.ssh/id_rsa admin@{Primary_ip} 'sudo systemctl restart postgresql'")
                flag_master_drop = False
                flag_promote = False
                print("Репликация успешно выполнена.") 
            except (Exception, Error) as error:
                print(f"Ошибка репликации")
        id+=1
        time.sleep(2)

def main():

    Primary_ip = '158.160.122.56'
    Standby_ip = '51.250.14.54'
    
    Replication_process(Primary_ip, Standby_ip)
    

main()
