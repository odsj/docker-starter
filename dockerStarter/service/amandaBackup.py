import commands
import sqlite3

"""
Column Index
"""
DATE = 0
TIME = 1
OBJECT =2
DIRECTORY = 3
RESULT = 4
SPENT_TIME = 6
BACKUP_SIZE = 8
ORIGINAL_SIZE= 12

AMANDA_BACKUP_DB = "dockerStarter/service/amanda_result.db"

def showBackupResult():
    # Connection DB
    allBackupResult = []
    try:
        conn = sqlite3.connect(AMANDA_BACKUP_DB)
        cursor = conn.cursor()

        result = cursor.execute("select * from backupresult")
        while True:
            row = result.fetchone()
            if row == None:
                break
            allBackupResult.append(row)
        return allBackupResult
    finally:
        #Close DB connection
        if conn:
            conn.close()

def saveBackupResult(backupResult):
    try:
        #Connection DB
        conn = sqlite3.connect(AMANDA_BACKUP_DB)
        cursor = conn.cursor()

        #Create DB Table
        cursor.execute("create table backupresult(Date text, Time text, Object text, Dir text, Result text, SpentTime float, BackupSize float, OriginalSize float)")

        #Open amanda_result file
        f = open(backupResult, 'r')

        while True:
            #Read amanda_result Line
            line = f.readline()
            if len(line) == 0:
                break
            #print line
            split_colume = line.split()

            if split_colume[RESULT] == 'FAIL':
                Insert_data = """insert into backupresult('Date','Time',Object,Dir,Result)\
                            values('{}','{}','{}','{}','{}')""" \
                    .format(split_colume[DATE], split_colume[TIME], split_colume[OBJECT], split_colume[DIRECTORY],
                            split_colume[RESULT])
            else :
                Insert_data = """insert into backupresult('Date','Time',Object,Dir,Result,SpentTime,BackupSize,OriginalSize)\
                values('{}','{}','{}','{}','{}','{}','{}','{}')"""\
                .format(split_colume[DATE], split_colume[TIME], split_colume[OBJECT], split_colume[DIRECTORY], split_colume[RESULT], split_colume[SPENT_TIME], split_colume[BACKUP_SIZE], split_colume[ORIGINAL_SIZE])

            #Insert Data
            cursor.execute(Insert_data)
            conn.commit()
    except IndexError:
        print("except : "+line)

    except sqlite3.Error, e:
        print("ERR : " + e.message)
        if conn:
            conn.rollback
    except sqlite3.OperationalError:
        print("")

    finally:
        #Close DB connection
        if conn:
            conn.close()
        #Close amanda_result file
        f.close()