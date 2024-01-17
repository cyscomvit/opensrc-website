from functools import lru_cache
from os import environ, getenv
from os.path import dirname, join

from dotenv import load_dotenv
from firebase_admin import credentials, db, initialize_app, storage
from flask import Flask, json, redirect, render_template

# Initialize Flask app
app = Flask(__name__)

# Read environment variables set at ./.env
if not load_dotenv(f"{dirname(__file__)}/.env"):
    raise RuntimeError(
        f"Could not load env file. Make sure it is located at {dirname(__file__)}/.env"
    )


def check_if_required_env_variables_are_present():
    required_env_variables = {
        "START_ACT",
        "END_ACT",
        "CURRENT_ACT_YEAR",
        "FIREBASE_STORAGE",
    }

    if not all(env in environ for env in required_env_variables):
        raise RuntimeError(
            f"The following required environmental variables have not been set - {(x for x in required_env_variables if x not in environ)}"
        )


check_if_required_env_variables_are_present()


# Initialize Firebase app
creds = credentials.Certificate("firebase.json")
initialize_app(
    creds,
    {
        "databaseURL": getenv("FIREBASE_DB"),
        "storageBucket": getenv("FIREBASE_STORAGE"),
    },
)


all_leaderboards_ref = db.reference("vitcc").child("owasp")


def fetch_data(act: int | str) -> list[dict]:
    """Return a list of all members in the act. Sorted by points"""
    data_of_act: dict = all_leaderboards_ref.child(f"leaderboard-act{act}").get()
    users_of_act = list(data_of_act.values())
    users_of_act.sort(key=lambda x: x["Rating"], reverse=True)
    return users_of_act


class Act:
    def __init__(self, num: int, name: str):
        self.num: int = num
        self.name: str = name
        self.data: list = fetch_data(num)
        self.cabinet = list(filter(lambda member: member["Rating"] >= 5000, self.data))
        self.members = list(filter(lambda member: member["Rating"] < 5000, self.data))
        self.rank_members()

    def rank_members(self):
        for i, member in enumerate(self.members):
            if i < 1:
                member["Image"] = "platinum-3"
            elif i < 3:
                member["Image"] = "platinum-2"
            elif i < 8:
                member["Image"] = "gold-3"
            elif i < 12:
                member["Image"] = "gold-2"
            elif i <= 25:
                member["Image"] = "silver-3"
            elif i <= 40:
                member["Image"] = "silver-2"
            else:
                member["Image"] = "bronze-1"

            if member["Rating"] == 0:
                member["Image"] = "unranked"


CURRENT_ACT_YEAR: int = int(getenv("CURRENT_ACT_YEAR"))
END_ACT: int = int(getenv("END_ACT"))
START_ACT: int = int(getenv("START_ACT"))

all_acts = [
    Act(i, f"ACT {i} - {CURRENT_ACT_YEAR - END_ACT + i}")
    for i in range(END_ACT, START_ACT, -1)
]


@app.route("/", methods=["GET"])
def index():
    return redirect("/leaderboard")


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return render_template("leaderboard.html", all_acts=all_acts, enumerate=enumerate)


@app.route("/hall_of_cyscom")
def hall_of_cyscom():
    # static/data/test_data.json
    filename = join(app.static_folder, "data", "test.json")
    # print(filename)

    with open(filename) as test_file:
        data = json.load(test_file)

    return render_template("hall_of_cyscom.html", data=data)


jsonfile = open("hoomans.json", "r")
jsondata = jsonfile.read()

# Parse JSON
obj = json.loads(jsondata)
members = obj["members"]


@app.route("/legacy")
def home():
    return render_template("legacy.html", context=members)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
