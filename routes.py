from flask import Blueprint, current_app, render_template, url_for, redirect, request
import datetime
import uuid

pages = Blueprint(
    "habits", __name__, template_folder="templates", static_folder="static"
)


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]

        return dates

    return {"date_range": date_range}


def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route("/")
def index():

    date_str = request.args.get("date")

    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    completions = [
        item["habit"]
        for item in current_app.db.completions.find({"date": selected_date})
    ]

    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})

    return render_template(
        "index.html",
        title="Habit Tracker - Home",
        habits=habits_on_date,
        completions=completions,
        selected_date=selected_date,
    )


@pages.route("/add", methods=["GET", "POST"])
def add_habit():

    today = today_at_midnight()
    if request.method == "POST":

        new_habit = request.form.get("habit")

        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": new_habit}
        )

        return redirect(url_for(".index"))

    return render_template(
        "add_habit.html",
        title="Habit Trakcer - Add Habit",
        selected_date=today,
    )


@pages.post("/complete")
def complete():

    date_str = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_str)
    entry = {"date": date, "habit": habit}
    current_app.db.completions.insert_one(entry)

    return redirect(url_for(".index", date=date_str))
