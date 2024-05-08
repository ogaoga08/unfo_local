"""
記事モデル
"""
from app.models.abstract import AbstractModel
# from datetime import datetime, timedelta
# import psycopg2

class ArticleModel(AbstractModel):
    def __init__(self, config):
        super(ArticleModel, self).__init__(config)

    # def fetch_recent_articles(self):
    #     """
    #     最新の記事を取得する デフォルトでは最新5件まで
    #     :param limit: 取得する記事の数
    #     :return:
    #     """
    #     sql = "SELECT * FROM articles ORDER BY created_at DESC LIMIT %s"
    #     return self.fetch_all(sql)

# #カード編集
#     def edit_article(self, article_id):
#         sql = "SELECT * FROM articles WHERE id = %s;"
#         return self.fetch_one(sql, article_id)
    
#     def edit_quiz(self, quiz_id):
#         sql = "SELECT * FROM quizzes INNER JOIN users u on quizzes.user_id = u.id WHERE quizzes.id=%s"
#         return self.fetch_one(sql, quiz_id)



#登録
    def create_article(self, user_id, title, body, hash, study_date):
        """
        新しく記事を作成する
        :param user_id: 投稿したユーザのOD
        :param title: 記事のタイトル
        :param body: 記事の本文
        :return: None
        """
        sql = "INSERT INTO articles(user_id, title, body, hash, study_date) VALUE (%s, %s, %s, %s, %s);"
        self.execute(sql, user_id, title, body, hash, study_date)

    def create_quiz(self, user_id, question, choice0, choice1, choice2, choice3, correct, hash, study_date):
        sql = "INSERT INTO quizzes(user_id, question, choice0, choice1, choice2, choice3, correct, hash, study_date) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.execute(sql, user_id, question, choice0, choice1, choice2, choice3, correct, hash, study_date)




#OK・NG処理
    def state_cards(self, id):
        sql = "UPDATE articles SET articles.num_times = num_times + 1 WHERE id=%s"
        self.execute(sql,id)

    def state_date_cards(self, id):
        sql = "UPDATE articles SET study_date = CASE WHEN study_date < CURDATE() THEN CURDATE() ELSE study_date END, study_date = CASE WHEN num_times = 1 THEN DATE_ADD(CURDATE(), INTERVAL 1 DAY) WHEN num_times = 2 THEN DATE_ADD(CURDATE(), INTERVAL 4 DAY) WHEN num_times = 3 THEN DATE_ADD(CURDATE(), INTERVAL 7 DAY) WHEN num_times = 4 THEN DATE_ADD(CURDATE(), INTERVAL 11 DAY) WHEN num_times = 5 THEN DATE_ADD(CURDATE(), INTERVAL 15 DAY) WHEN num_times = 6 THEN DATE_ADD(CURDATE(), INTERVAL 20 DAY) ELSE study_date END WHERE id = %s;"
        self.execute(sql, id)

    def back_state_date_cards(self, id):
        sql = "UPDATE articles SET study_date = CASE WHEN study_date < CURDATE() THEN CURDATE() ELSE study_date END, study_date = CASE WHEN num_times >= 1 AND num_times <= 7 THEN DATE_ADD(study_date, INTERVAL 1 DAY)WHEN num_times >= 8 THEN CURDATE() ELSE study_date END, num_times = CASE WHEN num_times >= 2 AND num_times <= 7 THEN num_times - 1 WHEN num_times >= 8 THEN 1 ELSE num_times END WHERE id = %s"
        self.execute(sql, id)


    def state_quizzes(self, id):
        sql = "UPDATE quizzes SET quizzes.num_times = num_times + 1 WHERE id=%s"
        self.execute(sql,id)

    def state_date_quizzes(self, id):
        sql = "UPDATE quizzes SET study_date = CASE WHEN study_date < CURDATE() THEN CURDATE() ELSE study_date END, study_date = CASE WHEN num_times = 1 THEN DATE_ADD(study_date, INTERVAL 1 DAY) WHEN num_times = 2 THEN DATE_ADD(study_date, INTERVAL 4 DAY) WHEN num_times = 3 THEN DATE_ADD(study_date, INTERVAL 7 DAY) WHEN num_times = 4 THEN DATE_ADD(study_date, INTERVAL 11 DAY) WHEN num_times = 5 THEN DATE_ADD(study_date, INTERVAL 15 DAY) WHEN num_times = 6 THEN DATE_ADD(study_date, INTERVAL 20 DAY) ELSE study_date END WHERE id = %s"
        self.execute(sql, id)

    def back_state_date_quizzes(self, id):
        sql = "UPDATE quizzes SET study_date = CASE WHEN study_date < CURDATE() THEN CURDATE() ELSE study_date END, study_date = CASE WHEN num_times >= 1 AND num_times <= 7 THEN DATE_ADD(study_date, INTERVAL 1 DAY)WHEN num_times >= 8 THEN CURDATE() ELSE study_date END, num_times = CASE WHEN num_times >= 8 THEN 1 ELSE num_times END WHERE id = %s"
        self.execute(sql, id)



#ホーム(今日・進行中・済)
    def fetch_articles_by_userid(self, user_id):
        #ユーザー自身の投稿のみ表示(今日)
        sql = "SELECT * FROM articles WHERE user_id=%s AND DATE(study_date) <= CURDATE() AND num_times <= 7 ORDER BY study_date DESC;"
        return self.fetch_all(sql, user_id)
    
    def fetch_articles_ongoing_by_userid(self, user_id):
        #ユーザー自身の投稿のみ表示(進行中)
        sql = "SELECT * FROM articles WHERE user_id=%s AND num_times <= 7 ORDER BY study_date ASC;"
        return self.fetch_all(sql, user_id)
    
    def fetch_articles_done_by_userid(self, user_id):
        #ユーザー自身の投稿のみ表示(済)
        sql = "SELECT * FROM articles WHERE user_id=%s AND num_times >= 8 ORDER BY study_date ASC;"
        return self.fetch_all(sql, user_id)
    

    def fetch_quizzes_by_userid(self, user_id):
        #ユーザー自身の投稿のみ表示(今日)
        sql = "SELECT * FROM quizzes WHERE user_id=%s AND DATE(study_date) <= CURDATE() AND num_times <= 7 ORDER BY study_date DESC;"
        return self.fetch_all(sql, user_id)
    
    def fetch_quizzes_ongoing_by_userid(self, user_id):
        #ユーザー自身の投稿のみ表示(進行中)
        sql = "SELECT * FROM quizzes WHERE user_id=%s AND num_times >= 1 AND num_times <= 7 ORDER BY study_date ASC;"
        return self.fetch_all(sql, user_id)
    
    def fetch_quizzes_done_by_userid(self, user_id):
        #ユーザー自身の投稿のみ表示(済)
        sql = "SELECT * FROM quizzes WHERE user_id=%s AND num_times >= 8 ORDER BY study_date ASC;"
        return self.fetch_all(sql, user_id)




#編集
    def edit_article_page(self, id):
        sql = "SELECT * FROM articles WHERE id = %s;"
        return self.fetch_one(sql, id)
    
    def edit_article(self, title, body, hash, id):
        sql = "UPDATE articles SET title = %s, body = %s, hash = %s WHERE id = %s"
        self.execute(sql, title, body, hash, id)




#検索
    def search_hash_cards(self, search, user_id):
        sql = "SELECT * FROM articles WHERE hash = %s AND user_id = %s AND DATE(study_date) <= CURDATE() AND num_times <= 7 ORDER BY study_date DESC;"
        return self.fetch_all(sql, search, user_id)
    
    def search_hash_quizzes(self, search, user_id):
        sql = "SELECT * FROM quizzes WHERE hash = %s AND user_id = %s AND DATE(study_date) <= CURDATE() AND num_times <= 7 ORDER BY study_date DESC;"
        return self.fetch_all(sql, search, user_id)

    def search_hash_cards_on(self, search, user_id):
        sql = "SELECT * FROM articles WHERE hash = %s AND user_id = %s AND num_times >= 1 AND num_times <= 7 ORDER BY study_date ASC;"
        return self.fetch_all(sql, search, user_id)
    
    def search_hash_quizzes_on(self, search, user_id):
        sql = "SELECT * FROM quizzes WHERE hash = %s AND user_id = %s AND num_times >= 1 AND num_times <= 7 ORDER BY study_date ASC;"
        return self.fetch_all(sql, search, user_id)

    def search_hash_cards_done(self, search, user_id):
        sql = "SELECT * FROM articles WHERE hash = %s AND user_id = %s AND num_times >= 8 ORDER BY study_date ASC;"
        return self.fetch_all(sql, search, user_id)
    
    def search_hash_quizzes_done(self, search, user_id):
        sql = "SELECT * FROM quizzes WHERE hash = %s AND user_id = %s AND num_times >= 8 ORDER BY study_date ASC;"
        return self.fetch_all(sql, search, user_id) 




#バッジ
    def badge_articles_num(self, user_id):
        sql = "SELECT COUNT(*) as badge_count FROM articles WHERE user_id = %s AND DATE(study_date) <= CURDATE() AND num_times <= 7;"
        return self.fetch_all(sql, user_id)
    
    def badge_quizzes_num(self, user_id):
        sql = "SELECT COUNT(*) as badge_count FROM quizzes WHERE user_id = %s AND DATE(study_date) <= CURDATE() AND num_times <= 7;"
        return self.fetch_all(sql, user_id)

#記録
    def fetch_articles_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM articles WHERE user_id = %s;"
        return self.fetch_all(sql, user_id)
    
    def fetch_quizzes_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM quizzes WHERE user_id = %s;"
        return self.fetch_all(sql, user_id)
    

    def fetch_articles_today_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM articles WHERE user_id=%s AND DATE(study_date) <= CURDATE() AND num_times <= 7;"
        return self.fetch_all(sql, user_id)
    
    def fetch_quizzes_today_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM quizzes WHERE user_id=%s AND DATE(study_date) <= CURDATE() AND num_times <= 7;;"
        return self.fetch_all(sql, user_id)


    def fetch_articles_ongoing_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM articles WHERE user_id = %s AND num_times <= 7;"
        return self.fetch_all(sql, user_id)
    
    def fetch_quizzes_ongoing_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM quizzes WHERE user_id = %s AND num_times <= 7;"
        return self.fetch_all(sql, user_id)
    

    def fetch_articles_done_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM articles WHERE user_id = %s AND num_times >= 8;"
        return self.fetch_all(sql, user_id)

    def fetch_quizzes_done_num_by_userid(self, user_id):
        sql = "SELECT COUNT(*) AS record_count FROM quizzes WHERE user_id = %s AND num_times >= 8;"
        return self.fetch_all(sql, user_id)