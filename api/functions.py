# Основная функция
async def get_month_data(month: int, year: int):
    async with httpx.AsyncClient() as client:
        dates = get_dates(month, year)
        date_from = dates["from"]
        date_to = dates["to"]

        print(f"📅 Получаем данные за {dates['title']} ({date_from} → {date_to})")

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


def get_dates(month: int, year: int):
    month = int(month)
    year = int(year)
    date_from = datetime(year, month, 1).strftime("%Y-%m-%d")
    _, day = calendar.monthrange(year, month)
    date_to = datetime(year, month, day).strftime("%Y-%m-%d")
    title = datetime(year, month, 1).strftime("%B %Y")
    return {"from": date_from, "to": date_t
