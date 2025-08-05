from urllib.parse import unquote
import httpx
import re
import asyncio
from datetime import datetime
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
        date_to = "2025-07-31"
        output = []
        teachers = await get_teachers(client)
        links = await get_all_student_unit_links(client, date_from, date_to, 0)
        students = await get_all_students(client, 0)
        for teacher in teachers:
          print(teacher)
          teacher["units"] = await get_units(client, teacher["id"], date_from, date_to)
          #print(teacher["id"], len(teacher["units"]))
          teacher["students"] = 0
          teacher["left"] = 0
          teacher["links"] = []
          for unit in teacher["units"]:
            teacher["links"] += list(filter(lambda link: link["EdUnitId"] == unit, links))
            #left_count = list(filter(lambda link: False if "EndDate" not in link else check_dates([link["EndDate"], date_from]) and check_dates([date_to, link["EndDate"]]), students_count))
          teacher["students"] = unique_students_count(teacher["links"])
          teacher["left"] = unique_left_count(teacher["links"], date_from, date_to)
          #print(teacher["name"], teacher["students"]) 
          output.append([teacher["name"], teacher["students"], teacher["left"] ])
        #coros = [count_students(client, teacher) for teacher in teachers]
        #asyncio.gather(*coros)
        print(output)
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
      #print(teacher)
      ...
    print('finished.')
    return teachers
    #connector = response["result"]["entity_id"].split("|")[0]
    #return {"chat": str(response["result"]["id"]), "user": str(response["result"]["owner"]), "connector": connector}

async def get_units(client, teacher, date_from, date_to):
  def check_unit(unit):
    schedule_items = list(filter(lambda item: item["TeacherId"] == teacher, unit["ScheduleItems"]))
    for item in schedule_items:
        #print(item["BeginDate"])
        if "EndDate" in item:
          if item["BeginDate"] != item["EndDate"]:
            #print(item["BeginDate"])
            return True
        else:
            return True
    return False
  path = api + "GetEdUnits"
  params["teacherId"] = teacher
  params["dateFrom"] = date_from
  params["dateTo"] = date_to
  response = await client.get(path, params=params)
  response = response.json()
  units = response["EdUnits"]
  #units = list(set(units))
  units = list({unit['Id']:unit for unit in units}.values())
  print("units: ", len(units))
  units = list(filter(check_unit, units))
  print("checked units: ", len(units))
  units = list(map(lambda unit: unit["Id"],  units))
  
  #print(len(units))
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
    if len(links) % 1000 == 0 and len(links) > 0:
        output = await get_all_student_unit_links(client, date_from, date_to, skip + 1000)
        links += output
    return links

def check_dates(dates: list):
    format = "%Y-%m-%d"
    dates = list(map(lambda date: datetime.strptime(date, format), dates))
    return dates[0] >= dates[1]

def extract_students(teacher, links):
    ...

def unique_students_count(links):
    students = list(map(lambda link: link["StudentClientId"], links))
    return len(set(students))

def unique_left_count(links, date_from, date_to):
    count = 0
    left = []
    students = set(list(map(lambda link: link["StudentClientId"], links)))
    print(len(students))
    for student in students:
        units = list(filter(lambda link: link["StudentClientId"] == student, links))
        units = list(map(lambda link: False if "EndDate" not in link else check_dates([link["EndDate"], date_from]) and check_dates([date_to, link["EndDate"]]), units))
        #print(student, units)
        if False not in units:
            count += 1;
            left.append(student)
    print(left)
    return count


