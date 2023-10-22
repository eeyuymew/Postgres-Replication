# Postgres-Replication
Работу выполнил: Музыченко Андрей.
## 1) Подготовка:
Для выполнения работы было подготовлено Debian (Master) - 158.160.122.56, Debian (Slave) - 51.250.94.1, и Windows 10

## 2) Настройка потоковой репликации:
- На каждой машине был установлен postgres
```
sudo apt-get install postgresql || apt-get install postgresql-client
```
- Настроены конфигурационные файлы:
  На Master:
  Изменен файл postrgesql.conf:
  ```
  listen_addresses = '*'
  wal_level = replica
  max_wal_senders = 2
  max_replication_slots = 2
  hot_standby = on
  hot_standby_feedback = on
  ```
  Добавлена строка в файл pg_hba.conf:
  ```
  host    replicator    all    51.250.14.54/32    md5
  ```

  На Slave:
  Выполнена команда:
  ```
  pg_basebackup --host=158.160.122.56 --username=replicator --pgdata=/var/lib/postgresql/13/main --wal-method=stream --write-recovery-conf
  ```
  ## 3) Запуск скрипта:
  - Был подготовлен скрипт main.py:
    Метод check_ping проверяет доступность машины командой ping.
    
    Метод check_connection проверяет доступность БД на определенной машине при помощи psycopg командой select 1;
    
    В случае если, check_ping обнаружает недоступность Master данные дублируются на Slave и сервер переходит в основной режим на Slave,
    пока Master не станет доступным.
    
    Когда Master становится доступным происходит репликация данных при помощи pg_basebackup и вся конфигурация возвращается обратно на Master.
  - Скрипт был запущен в фоновом режиме на Windows.

  ## Демонстрация:
  https://www.youtube.com/watch?v=LZLOW2Wv8_o
    
