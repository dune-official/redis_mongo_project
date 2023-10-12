from flask import Flask, request, render_template
import db  # author: Linu(s|x)

app = Flask(__name__, template_folder="./templates")

username = "bilbo_swaggins69"


@app.route('/')
def index():
    recommended = db.get_recents(username)
    movie_meta = []
    for movie in recommended:
        movie_meta.append({"title": movie["title"], "id": movie["id"]})

    print("asked for index")
    return render_template("index.html", variables=recommended)


@app.route('/query', methods=['GET'])
def movies():
    genre = request.args.get("genre")
    string = request.args.get("string")
    print("querying")

    entries = db.find_movie(string)
    recents = db.get_recents()

    to_return = []

    if genre == '':
        for entry in entries:
            if genre in entry["genre"]:
                to_return.append(entry)
    else:
        to_return = entries

    content = {"found": to_return, "recents": recents}

    return "Under construction, please wear a hard hat..."


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=80)
