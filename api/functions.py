from datetime import datetime
import calendar

# =======================
# Основная функция
# =======================
async def get_month_data(month: int, year: int):
    # Здесь должна быть твоя логика с API HollyHop.
    # Для проверки пока возвращаем тестовые данные.
    dates = get_dates(month, year)
    print(f"📅 Получаем данные за {dates['title']} ({dates['from']} → {dates['to']})")

    output = [["Преподаватель", "Ученики", "Откол", "% откола"]]
    output.append(["Иванова", 10, 2, "20%"])
    output.append(["Петров", 8, 1, "12.5%"])
    output.append(["СяоДин", 15, 0, "0%"])

    return output


# =======================
# Служебная функция дат
# =======================
def get_dates(month: int, year: int):
    month = int(month)
    year = int(year)
    date_from = datetime(year, month, 1).strftime("%Y-%m-%d")
    _, day = calendar.monthrange(year, month)
    date_to = datetime(year, month, day).strftime("%Y-%m-%d")
    title = datetime(year, month, 1).strftime("%B %Y")
    return {"from": date_from, "to": date_to, "title": title, "year": year}
