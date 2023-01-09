# from flask import Flask, render_template, request
#
# #
# # @app.route('/', methods=["POST"])
# # def __main__():
# #     if request.method == "POST":
# #         movie_name = request.form.get("movie_name")
# #         movie_year = request.form.get("movie_year")
# #         print(f"Movie: {movie_name} {movie_year}")
# #         return f"Movie: {movie_name} {movie_year}"
# #     return render_template("search_movie.jinja2")
#
#
# class DownloaderGUI:
#     app = None
#
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.app.run(debug=True, host="0.0.0.0", port=80)
#         self.app.add_url_rule('/', '', self.my_form)
#         self.film_name = None
#         self.film_year = None
#
#     #@app.route('/')
#     def my_form(self):
#         return render_template('search_movie.jinja2')
#
#     def index(self):
#         pass
#
#     #@app.route('/', methods=['POST'])
#     def my_form_post(self):
#         if request.method == "POST":
#             self.film_name = request.form.get("movie_name")
#             self.film_year = request.form.get("movie_year")
#             #GO TO RESULTS PAGE
#
#     @property
#     def get_film_name(self):
#         return self.film_name
#
#     @property
#     def get_film_year(self):
#         return self.film_year
#
#
# # if __name__ == "__main__":
# #     app.run(debug=True, host="0.0.0.0", port=80)
# #
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


#This will be torrent list
current_search = {
    'film_name': 'Titanic',
    'film_year': '1997'
}


@app.route("/")
def home():
    return render_template('home.jinja2', current_search=current_search)


@app.route('/post/<int:post_id>')
def torrent(post_id):
    print(post_id)
    return render_template('torrent.jinja2', current_search=current_search)


# args: 127.0.0.1:5000/post/create?title=blalala&content=something_else
# form: 127.0.0.1:5000/post/create?title=blalala&content=something_else
@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        film_name = request.form.get('film_name')
        film_year = request.form.get('film_year')
        current_search['film_name'] = film_name
        current_search['film_year'] = film_year
        return redirect(url_for('torrent', post_id=0))
    return render_template('search_movie.jinja2')


@property
def get_film_name():
    return current_search.get('film_name')


@property
def get_film_year():
    return current_search.get('film_year')


def run():
    app.run(debug=True)


if __name__ == '__main__':
    run()
