from urllib.parse import unquote
import httpx
import re
import asyncio
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
        teachers = await get_teachers(client)
        for teacher in teachers:
           ...   
        students = await get_all_students(client, 0)
        units = await get_units(client, 1418, "2025-01-01","2025-08-01")
        #units = list(filter(lambda unit: unit

async def get_teachers(client):
    path = api + "getteachers"
    response = await client.get(path, params=params)
    response = response.json()
    teachers = list(filter(lambda teacher: not teacher["Fired"], response["Teachers"]))
    teachers = map(lambda teacher: {"id": teacher["Id"], "name": teacher["LastName"]} , teachers)
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
  return response["EdUnits"]

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
