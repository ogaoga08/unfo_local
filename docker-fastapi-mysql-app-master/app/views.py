# これがコントローラー(htmlページ,python処理とデータベースの橋渡し)
from fastapi import FastAPI, Request, Form, Cookie, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from fastapi.staticfiles import StaticFiles
from app.configs import Config
from app.utilities.session import Session
from app.models.auth import AuthModel
from app.models.articles import ArticleModel
from app.utilities.check_login import check_login
from app.utilities.save_image import save_image
from datetime import datetime

app = FastAPI()
app.mount("/app/statics", StaticFiles(directory="app/statics"), name="static")
templates = Jinja2Templates(directory="/app/templates")
config = Config()
session = Session(config)


@app.get("/")
def index(request: Request):
    print(request.body)
    """
    トップページを返す
    :param request: Request object
    :return:
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register")
def register(request: Request):
    """
    新規登録ページ
    :param request:
    :return:
    """
    print(request.body)
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/login")  # (index.htmlから)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    ログイン処理
    :param request:
    :param username:
    :param password:
    :return:
    """
    # usernameとpwの値をデータベースに問い合わせ・照らし合わせている
    # 実際に内部での処理はauth.py/def loginが行なっている
    auth_model = AuthModel(config)  # データベースにアクセスするために名前を設定
    [result, user] = auth_model.login(username, password)  # モデルに対してusernameとpwの値を投げかける
    # ↑2つの値(result,user)を返している
    if not result:  # =resultに値が入っていなければ
        # ユーザが存在しなければトップページへ戻す
        return templates.TemplateResponse(
            "index.html", {"request": request, "error": "ユーザ名またはパスワードが間違っています"}
        )
    response = RedirectResponse(
        "/cards", status_code=HTTP_302_FOUND
    )  # したのreturnを経てnextpageでもセッションの情報が保持される
    session_id = session.set("user", user)  # =ユーザー情報をセッションの情報(ID)として登録
    response.set_cookie("session_id", session_id)  # IDを利用してクッキーに設定
    return response  # 上のresponseにもどる

@app.post("/register")
def create_user(username: str = Form(...), password: str = Form(...)):
    """
    ユーザ登録をおこなう
    フォームから入力を受け取る時は，`username=Form(...)`のように書くことで受け取れる
    :param username: 登録するユーザ名
    :param password: 登録するパスワード
    :return: 登録が完了したら/blogへリダイレクト
    """
    auth_model = AuthModel(config)
    auth_model.create_user(username, password)
    user = auth_model.find_user_by_name_and_password(username, password)
    response = RedirectResponse(url="/cards", status_code=HTTP_302_FOUND)
    session_id = session.set("user", user)
    response.set_cookie("session_id", session_id)
    return response




#今日のカードページの処理
@app.get("/cards")
@check_login
def articles_index(
    request: Request, session_id=Cookie(default=None)
): 
    user = session.get(session_id).get("user")  
    article_model = ArticleModel(config)
    articles = article_model.fetch_articles_by_userid(user["id"])
    quizzes = article_model.fetch_quizzes_by_userid(user["id"])
    articles_today = article_model.fetch_articles_today_num_by_userid(user["id"])
    quizzes_today = article_model.fetch_quizzes_today_num_by_userid(user["id"])
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "cards-index.html", {"request": request, "articles": articles, "quizzes": quizzes, "articles_today": articles_today[0]["record_count"], "quizzes_today": quizzes_today[0]["record_count"],
        "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
    )

@app.post("/cards/{article_id}")
@check_login
def post_cards_info1(article_id: int, article_state_change: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    if article_state_change == "OK":
        article_model.state_date_cards(article_id)
        article_model.state_cards(article_id)
        return RedirectResponse("/cards", status_code=HTTP_302_FOUND)
    elif article_state_change == "NG":
        article_model.back_state_date_cards(article_id)
        return RedirectResponse("/cards", status_code=HTTP_302_FOUND)
    else:
        pass

@app.post("/quizzes/{quiz_id}")
@check_login
def post_quizzes_info1(quiz_id: int, article_state_change: str = Form(default=None), quiz_state_change: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    if article_state_change:
        pass
    elif quiz_state_change == "OK":
        article_model.state_date_quizzes(quiz_id)
        article_model.state_quizzes(quiz_id)
        return RedirectResponse("/cards", status_code=HTTP_302_FOUND)
    elif quiz_state_change == "NG":
        article_model.back_state_date_quizzes(quiz_id)
        return RedirectResponse("/cards", status_code=HTTP_302_FOUND)



#学習中のカードページの処理
@app.get("/cards_ongoing")
@check_login
def articles_ongoing_index(
    request: Request, session_id=Cookie(default=None)
):  
    user = session.get(session_id).get("user") 
    article_model = ArticleModel(config)
    articles = article_model.fetch_articles_ongoing_by_userid(user["id"])
    quizzes = article_model.fetch_quizzes_ongoing_by_userid(user["id"])
    articles_below_7 = article_model.fetch_articles_ongoing_num_by_userid(user["id"])
    quizzes_below_7 = article_model.fetch_quizzes_ongoing_num_by_userid(user["id"])
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "ongoing-index.html",
        {"request": request,
        "articles": articles,
        "quizzes": quizzes,
        "articles_below_7": articles_below_7[0]["record_count"],
        "quizzes_below_7": quizzes_below_7[0]["record_count"],
        "a_badge": a_badge[0]["badge_count"],
        "q_badge": q_badge[0]["badge_count"],
        "user": user
        }
    )

@app.post("/cards_ongoing/{article_id}")
@check_login
def post_cards_info2(article_id: int, article_state_change: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    if article_state_change == "OK":
        article_model.state_date_quizzes(article_id)
        article_model.state_quizzes(article_id)
        return RedirectResponse("/cards_ongoing", status_code=HTTP_302_FOUND)
    elif article_state_change == "NG":
        article_model.back_state_date_quizzes(article_id)
        return RedirectResponse("/cards_ongoing", status_code=HTTP_302_FOUND)

@app.post("/quizzes_ongoing/{quiz_id}")
@check_login
def post_quizzes_info2(quiz_id: int, article_state_change: str = Form(default=None), quiz_state_change: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    if article_state_change:
        pass
    elif quiz_state_change == "OK":
        article_model.state_date_quizzes(quiz_id)
        article_model.state_quizzes(quiz_id)
        return RedirectResponse("/cards_ongoing", status_code=HTTP_302_FOUND)
    elif quiz_state_change == "NG":
        article_model.back_state_date_quizzes(quiz_id)
        return RedirectResponse("/cards_ongoing", status_code=HTTP_302_FOUND)



#学習済のカードページの処理
@app.get("/cards_done")
@check_login
def articles_done_index(
    request: Request, session_id=Cookie(default=None)
):  
    user = session.get(session_id).get("user")  
    article_model = ArticleModel(config)
    articles = article_model.fetch_articles_done_by_userid(user["id"])
    quizzes = article_model.fetch_quizzes_done_by_userid(user["id"])
    articles_above_8 = article_model.fetch_articles_done_num_by_userid(user["id"])
    quizzes_above_8 = article_model.fetch_quizzes_done_num_by_userid(user["id"])
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "done-index.html", {"request": request, "articles": articles, "quizzes": quizzes, "articles_above_8": articles_above_8[0]["record_count"], "quizzes_above_8": quizzes_above_8[0]["record_count"],
        "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
    )

@app.post("/cards_done/{article_id}")
@check_login
def post_cards_info3(article_id: int, article_state_change: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    if article_state_change == "OK":
        article_model.state_date_cards(article_id)
        article_model.state_cards(article_id)
        return RedirectResponse("/cards_done", status_code=HTTP_302_FOUND)
    elif article_state_change == "NG":
        article_model.back_state_date_cards(article_id)
        return RedirectResponse("/cards_done", status_code=HTTP_302_FOUND)

@app.post("/quizzes_done/{quiz_id}")
@check_login
def post_quizzes_info3(quiz_id: int, article_state_change: str = Form(default=None), quiz_state_change: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    if article_state_change:
        pass
    elif quiz_state_change == "OK":
        article_model.state_date_quizzes(quiz_id)
        article_model.state_quizzes(quiz_id)
        return RedirectResponse("/cards_done", status_code=HTTP_302_FOUND)
    elif quiz_state_change == "NG":
        article_model.back_state_date_quizzes(quiz_id)
        return RedirectResponse("/cards_done", status_code=HTTP_302_FOUND)




#カード編集ページ
@app.get("/cards/edit/{article_id}")
@check_login
def edit_cards_page(
    article_id: int,
    request: Request,
    session_id=Cookie(default=None)
):
    user = session.get(session_id).get("user") 
    article_model = ArticleModel(config)
    article = article_model.edit_article_page(article_id)
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "cards_edit.html", {"request": request, "article": article, "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"],
        "user": user}
    )

@app.post("/cards/edit/{article_id}")
@check_login
def edit_cards(
    title: str = Form(...),
    body: str = Form(...),
    hash: str = Form(default=None),
    session_id=Cookie(default=None)
):
    article_model = ArticleModel(config)
    user_id = session.get(session_id).get("user").get("id")
    article_model.create_article(user_id, title, body, hash)
    return RedirectResponse("/cards", status_code=HTTP_302_FOUND)



#カード作成ページ
@app.get("/create-cards")
@check_login
def create_article_page(
    request: Request,
    session_id=Cookie(default=None),
):
    user = session.get(session_id).get("user")
    article_model = ArticleModel(config)
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "create-article.html", {"request": request, "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
    )

@app.post("/create-cards")
@check_login
def post_article(
    title: str = Form(...),
    body: str = Form(...),
    hash: str = Form(default=None),
    study_date: str = Form(...),
    session_id=Cookie(default=None)
):
    article_model = ArticleModel(config)
    user_id = session.get(session_id).get("user").get("id")
    article_model.create_article(user_id, title, body, hash, study_date)
    return RedirectResponse("/create-cards", status_code=HTTP_302_FOUND)



#クイズ作成ページ
@app.get("/create-quiz")
@check_login
def create_quiz_page(
    request: Request,
    session_id=Cookie(default=None),
):
    user = session.get(session_id).get("user")
    article_model = ArticleModel(config)
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "create-quiz.html", {"request": request, "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
    )

@app.post("/create-quiz")
@check_login
def post_quiz(
    question: str = Form(...),
    choice0: str = Form(...),
    choice1: str = Form(...),
    choice2: str = Form(default=None),
    choice3: str = Form(default=None),
    correct: int = Form(...),
    hash: str = Form(default=None),
    study_date: str = Form(...),
    session_id=Cookie(default=None)
):
    article_model = ArticleModel(config)
    user_id = session.get(session_id).get("user").get("id")
    article_model.create_quiz(user_id, question, choice0, choice1, choice2, choice3, correct, hash, study_date)
    return RedirectResponse("/create-quiz", status_code=HTTP_302_FOUND)



#記録ページ
@app.get("/records")
@check_login
def records_page(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    article_model = ArticleModel(config)
    articles = article_model.fetch_articles_num_by_userid(user["id"])
    quizzes = article_model.fetch_quizzes_num_by_userid(user["id"])
    articles_above_8 = article_model.fetch_articles_done_num_by_userid(user["id"])
    quizzes_above_8 = article_model.fetch_quizzes_done_num_by_userid(user["id"])
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
    "records.html",
    {
        "request": request,
        "articles": articles[0]["record_count"],
        "quizzes": quizzes[0]["record_count"],
        "articles_above_8": articles_above_8[0]["record_count"],
        "quizzes_above_8": quizzes_above_8[0]["record_count"],
        "a_badge": a_badge[0]["badge_count"],
        "q_badge": q_badge[0]["badge_count"],
        "user": user,
    },
)



#設定ページ
@app.get("/settings")
@check_login
def settings_page(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    article_model = ArticleModel(config)
    a_badge = article_model.badge_articles_num(user["id"])
    q_badge = article_model.badge_quizzes_num(user["id"])
    return templates.TemplateResponse(
        "settings.html", {"request": request, "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
    )



#ログアウト処理
@app.get("/logout")
@check_login
def logout(session_id=Cookie(default=None)):
    session.destroy(session_id)
    response = RedirectResponse(url="/")
    response.delete_cookie("session_id")
    return response





#カード検索
@app.post("/cards")
@check_login
def search_cards(request: Request, current_page:str = Form(...),  search: str = Form(...), session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    article_model = ArticleModel(config)
    if current_page == "today":
        articles = article_model.search_hash_cards(search, user["id"])
        quizzes = article_model.search_hash_quizzes(search, user["id"])
        articles_today = article_model.fetch_articles_today_num_by_userid(user["id"])
        quizzes_today = article_model.fetch_quizzes_today_num_by_userid(user["id"])
        a_badge = article_model.badge_articles_num(user["id"])
        q_badge = article_model.badge_quizzes_num(user["id"])
        return templates.TemplateResponse(
            "cards-index.html", {"request": request, "articles": articles, "quizzes": quizzes, "articles_today": articles_today[0]["record_count"], "quizzes_today": quizzes_today[0]["record_count"],
            "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
        )
    elif current_page == "ongoing":
        articles = article_model.search_hash_cards_on(search, user["id"])
        quizzes = article_model.search_hash_quizzes_on(search, user["id"])
        articles_below_7 = article_model.fetch_articles_ongoing_num_by_userid(user["id"])
        quizzes_below_7 = article_model.fetch_quizzes_ongoing_num_by_userid(user["id"])
        a_badge = article_model.badge_articles_num(user["id"])
        q_badge = article_model.badge_quizzes_num(user["id"])
        return templates.TemplateResponse(
            "ongoing-index.html", {"request": request, "articles": articles, "quizzes": quizzes, "articles_below_7": articles_below_7[0]["record_count"], "quizzes_below_7": quizzes_below_7[0]["record_count"],
            "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
        )
    elif current_page == "done":
        articles = article_model.search_hash_cards_done(search, user["id"])
        quizzes = article_model.search_hash_quizzes_done(search, user["id"])
        articles_above_8 = article_model.fetch_articles_done_num_by_userid(user["id"])
        quizzes_above_8 = article_model.fetch_quizzes_done_num_by_userid(user["id"])
        a_badge = article_model.badge_articles_num(user["id"])
        q_badge = article_model.badge_quizzes_num(user["id"])
        return templates.TemplateResponse(
            "done-index.html", {"request": request, "articles": articles, "quizzes": quizzes, "articles_above_8": articles_above_8[0]["record_count"], "quizzes_above_8": quizzes_above_8[0]["record_count"],
            "a_badge": a_badge[0]["badge_count"], "q_badge": q_badge[0]["badge_count"], "user": user}
        )