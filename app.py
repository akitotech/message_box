from flask import Flask, render_template, request, redirect
from flask import Flask, flash, redirect, render_template, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import IntegrityError
from config import User

# 初期設定的なやつ
app = Flask(__name__)
app.secret_key = "secret"  # 秘密鍵を設定
login_manager = LoginManager()
login_manager.init_app(app)


# ログインユーザーの情報を取得できるようにする
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 入力データの検証:未入力
        if not request.form["name"] or not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)
        if User.select().where(User.name == request.form["name"]):
            flash("その名前はすでに使われています。")
            return redirect(request.url)
        if User.select().where(User.email == request.form["email"]):
            flash("そのメールアドレスはすでに使われています。")
            return redirect(request.url)

        try:
            # ユーザー登録処理
            User.create(
                name=request.form["name"],
                email=request.form["email"],
                password=generate_password_hash(request.form["password"]),
            )
            return render_template("index.html")
        except IntegrityError as e:
            flash(f"{e}")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form["email"] or not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return render_template(request.url)

        # 認証してOKならログイン
        user = User.select().where(User.email == request.form["email"]).first()
        if user is not None and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash(f"ようこそ！{user.name}さん")
            return redirect(url_for("index"))

        # だめだったらフラッシュメッセージ
        flash("認証に失敗しました")

    return render_template("login.html")


# ログアウト処理
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました！")
    return redirect("/")

    if not current_user.is_authenticated:
        return "ログインしていません"


# ユーザ削除
@app.route("/unregister")
@login_required
def unregister():
    current_user.delete_instance()
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
