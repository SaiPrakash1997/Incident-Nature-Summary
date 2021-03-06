import io
import sqlite3
from project0.extractIncidents import extractDataFromFile
from project0.fetchIncidents import dataFetchedFromURL
from project0.incidentsDB import incidentDataBase


def test_fetchincidents():

    urlParse = "https://www.normanok.gov/sites/default/files/documents/2022-03/2022-03-06_daily_incident_summary.pdf"
    print(urlParse)
    fetchIncidentObj = dataFetchedFromURL()
    dataFromFunc = fetchIncidentObj.fetchincidents(urlParse)
    extractData = extractDataFromFile()
    dataList = extractData.extractincidents(dataFromFunc)
    assert dataFromFunc is not None
    assert io.BytesIO(dataFromFunc)
    assert len(dataList) != 0
    assert len(dataList) == 267


def test_extractsIncidents():
    localFileData = open('2022-01-01_daily_incident_summary.pdf', 'rb')
    print(localFileData)
    extractData = extractDataFromFile()
    dataList = extractData.extractincidents(localFileData.read())
    assert len(dataList) != 0
    assert len(dataList) == 262
    assert type(dataList) == list


def test_populatedb():
    fetch_sql = "select count(*) from incidents; "
    localFileData = open('2022-01-01_daily_incident_summary.pdf', 'rb')
    extractData = extractDataFromFile()
    dataList = extractData.extractincidents(localFileData.read())
    incidentObj = incidentDataBase()
    incidentObj.populatedb(dataList)
    dbName = "normanpd.db"
    con = sqlite3.connect(dbName)
    sql_cursor = con.cursor()
    sql_cursor.execute(fetch_sql)
    result = sql_cursor.fetchall()
    print(result)
    assert result[0][0] == 261
    assert type(result[0]) == tuple


def test_status():
    incidentObj = incidentDataBase()
    result = incidentObj.status()
    assert result != 0
    for data in result:
        len(data) > 0
    assert result is not None
    assert type(result) == list


def test_createdb():
    incidentObj = incidentDataBase()
    con = incidentObj.createdb()
    assert con is not None
