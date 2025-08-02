from urllib.parse import unquote
import httpx
import re
import asyncio
import datetime
#import asyncpg
import time
import os
import redis
import emoji
import random 
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
api = os.getenv("api")
key = os.getenv("key")
params = {"authkey":key}
connection_string = os.getenv("postgresql")
#slist = os.getenv("list").split(',')
load_dotenv(dotenv_path=".env.local")
#redis_url = os.getenv("REDIS_URL")

async def main():
    async with httpx.AsyncClient() as client:
        date_from = "2025-07-01"
        date_to = "2025-08-01"
        
        teachers = await get_teachers(client)
        links = await get_all_student_unit_links(client, date_from, date_to, 0)
        students = await get_all_students(client, 0)
        
        async for teacher in teachers:
          teacher["units"] = await get_units(client, teacher["id"], date_from, date_to)
          print(teacher["id"], len(teacher["units"]))
          teacher["students"] = 0
          for unit in teacher["units"]:
            teacher["students"] += len(list.filter(lambda link: link["EdUnitId"] == unit, links))
          print(teacher["name"], teacher["students"])     
        print("main finished.")
        #units = await get_units(client, 1418, "2025-01-01","2025-08-01")
        #units = list(filter(lambda unit: unit

async def get_teachers(client):
    path = api + "getteachers"
    response = await client.get(path, params=params)
    response = response.json()
    teachers = list(filter(lambda teacher: not teacher["Fired"], response["Teachers"]))
    teachers = list(map(lambda teacher: {"id": teacher["Id"], "name": teacher["LastName"]} , teachers))
    for teacher in teachers:
      print(teacher)
    print('finished.')
    return teachers
    #connector = response["result"]["entity_id"].split("|")[0]
    #return {"chat": str(response["result"]["id"]), "user": str(response["result"]["owner"]), "connector": connector}

async def get_units(client, teacher, date_from, date_to):
  path = api + "GetEdUnits"
  params["teacherId"] = teacher
  params["dateFrom"] = date_from
  params["dateTo"] = date_to
  response = await client.get(path, params=params)
  response = response.json()
  units = response["EdUnits"]
  units = map(lambda unit: unit["Id"],  response["EdUnits"])
  return units

async def get_students(units):
  ...
  ...

async def get_all_students(client, skip):
    students = []
    path = api + "GetStudents"
    params["skip"] = skip
    response = await client.get(path, params=params)
    response = response.json()
    students += response["Students"]
    print("students count: ", len(students))
    if len(students) % 1000 == 0:
        output = await get_all_students(client, skip + 1000)
        students += output
    return students

async def get_all_student_unit_links(client, date_from, date_to, skip):
    links = []
    path = api + "GetEdUnitStudents"
    params["skip"] = skip
    params["dateFrom"] = date_from
    params["dateTo"] = date_to
    response = await client.get(path, params=params)
    response = response.json()
    links += response["EdUnitStudents"]
    print("links count: ", len(links))
    if len(links) % 1000 == 0:
        output = await get_all_student_unit_links(client, date_from, date_to, skip + 1000)
        links += output
    return links

def check_dates(dates: list, more: bool):
    format = "%Y-%m-%d"
    dates = map(lambda date: datetime.strptime(date, format), dates)
    if more:
        return dates[0] > dates[1]
    else:
        return dates[0] < dates[1]
