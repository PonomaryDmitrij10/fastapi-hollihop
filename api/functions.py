from urllib.parse import unquote
import httpx
from datetime import datetime
import os
import calendar
from dotenv import load_dotenv

# =======================
# Настройки
# =======================
TEST_MODE = False   # ← переключай здесь (True = тестовые данные, False = боевой режим)

# Загружаем .env
load_dotenv(dotenv_path=".env")
api = os.getenv("api")
key = os.getenv("key")
params = {"authkey": key}
load_dotenv(dotenv_path=".env.local")


# =======================
# Основная функция
# =======================
async def get_month_data(month: int, year: int | None = None):
    if year is None:
        year = datetime.now().year

    dates = get_dates(month, year)
    date_from = dates["from"]
    date_to = dates["to"]

    print(f"📅 Получаем данные за {dates['title']} ({date_from} → {date_to})")

    # ===== ТЕСТОВЫЙ РЕЖИМ =====
    if TEST_MODE:
        output = [["Преподаватель", "Ученики", "Откол", "% откола"]]
        output.append(["Иванова", 10, 2, "20%"])
        output.append(["Петров", 8, 1, "12.5%"])
        output.append(["СяоДин", 15, 0, "0%"])
        return output

    # ===== БОЕВОЙ РЕЖИМ =====
    async with httpx.AsyncClient() as client:
        teachers = await get_teachers(client)
        print(f"👨‍🏫 Найдено преподавателей: {len(teachers)}")

        links = await get_all_student_unit_links(client, date_from, date_to, 0)
        print(f"🔗 Всего связей EdUnit-Student: {len(links)}")

        students = await get_all_students(client, 0)
        print(f"👨‍🎓 Всего студентов: {len(students)}")

        # Заголовки таблицы
        output = [["Преподаватель", "Ученики", "Откол", "% откола"]]

        for teacher in teachers:
            teacher["units"] = await get_units(client, teacher["id"], date_from, date_to)
            print(f"➡️ {teacher['name']} → найдено юнитов: {len(teacher['units'])}")

            teacher["links"] = []
            for unit in teacher["units"]:
                teacher["links"] += list(filter(lambda link: link["EdUnitId"] == unit, links))

            students_count = unique_students_count(teacher["links"])
            left_count = unique_left_count(teacher["links"], date_from, date_to)
            percent = "0.0%" if not students_count else f"{left_count / students_count * 100:.2f}%"

            print(f"   👥 {teacher['name']} → Ученики={students_count}, Откол={left_count}, %={percent}")

            output.append([teacher["name"], students_count, left_count, percent])

        print("✅ get_month_data finished")
        return output


# =======================
# Служебные функции
# =======================
async def get_teachers(client):
    path = api + "getteachers"
    response = await client.get(path, params=params)
    response = response.json()
    teachers = list(filter(lambda teacher: not teacher["Fired"], response["Teachers"]))
    teachers = list(map(lambda teacher: {"id": teacher["Id"], "name": teacher["LastName"]}, teachers))
    return teachers


async def get_units(client, teacher, date_from, date_to):
    def check_unit(unit):
        not_related_items = list(filter(lambda item: item["TeacherId"] != teacher, unit["ScheduleItems"]))
        if len(not_related_items) == 0:
            return True
        schedule_items = list(filter(lambda item: item["TeacherId"] == teacher, unit["ScheduleItems"]))
        for item in schedule_items:
            if "EndDate" in item:
                if item["BeginDate"] != item["EndDate"]:
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
    units = list({unit["Id"]: unit for unit in units}.values())  # уникальные
    units = list(filter(check_unit, units))
    units = list(map(lambda unit: unit["Id"], units))
    return units


async def get_all_students(client, skip):
    students = []
    path = api + "GetStudents"
    params["skip"] = skip
    response = await client.get(path, params=params)
    response = response.json()
    students += response["Students"]
    if len(students) % 1000 == 0 and len(students) > 0:
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
    if len(links) % 1000 == 0 and len(links) > 0:
        output = await get_all_student_unit_links(client, date_from, date_to, skip + 1000)
        links += output
    return links


def check_dates(dates: list):
    format = "%Y-%m-%d"
    dates = list(map(lambda date: datetime.strptime(date, format), dates))
    return dates[0] >= dates[1]


def unique_students_count(links):
    students = list(map(lambda link: link["StudentClientId"], links))
    return len(set(students))


def unique_left_count(links, date_from, date_to):
    count = 0
    students = set(list(map(lambda link: link["StudentClientId"], links)))
    for student in students:
        units = list(filter(lambda link: link["StudentClientId"] == student, links))
        units = list(
            map(
                lambda link: False
                if "EndDate" not in link
                else check_dates([link["EndDate"], date_from])
                and check_dates([date_to, link["EndDate"]]),
                units,
            )
        )
        if False not in units:
            count += 1
    return count


def get_dates(month, year):
    month = int(month)
    year = int(year)
    date_from = datetime(year, month, 1).strftime("%Y-%m-%d")
    _, day = calendar.monthrange(year, month)
    date_to = datetime(year, month, day).strftime("%Y-%m-%d")
    title = datetime(year, month, 1).strftime("%B %Y")
    return {"from": date_from, "to": date_to, "title": title, "year": year}
