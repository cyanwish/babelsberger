import datetime
import requests
from bs4 import BeautifulSoup
import config


def main():
    meal_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
    today = get_today()
    if today in meal_days:
        babelsberger = get_babelsberger_menu()
        daily_meals = get_daily_meals(babelsberger[today])
        output_string = "Daily meals:\n"
        for meal in daily_meals:
            output_string += "### " + meal + " ###\n"
        data = {'text': output_string}
        response = requests.post(config.get_slack_web_hook_url(),
                                 json=data, allow_redirects=True)

def get_today():
    return datetime.datetime.now().strftime("%A")


def get_babelsberger_menu(url=config.get_babelsberger_url()):
    table_data_cells = BeautifulSoup(requests.get(url).content, 'html.parser').body.contents[3].contents[5].find_all("td")
    try:
        table_data_cells.remove(table_data_cells[0])
        table_data_cells.remove(table_data_cells[5])
    except ValueError:
        pass
    divs = {'monday': table_data_cells[0].div,
            'tuesday': table_data_cells[1].div,
            'wednesday': table_data_cells[2].div,
            'thursday': table_data_cells[3].div,
            'friday': table_data_cells[4].div}
    return divs


def get_daily_meals(div):
    daily_meals = []
    for paragraph in div.find_all('p'):
        meal = ""
        for line in paragraph.stripped_strings:
            meal += " " + line.replace("\n", "").replace(".", "")
        daily_meals.append(" ".join(meal.split()))
    return daily_meals


main()
