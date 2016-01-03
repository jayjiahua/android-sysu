#coding=utf-8

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import uuid
import json

from sqlalchemy.orm import scoped_session, sessionmaker
from utils.db import engine
from utils.login import login, LoginStatus
from utils.score import get_score
from utils.syllabus import get_syllabus
from utils.session import Session, SESSION_DICT
from utils.student_info import get_student_info
from models.student import Student
from models.moment import Moment, MomentLike, MomentUnlike
from functools import wraps


session_manager = Session()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/login", LoginHandler),
                    (r"/score", ScoreHandler),
                    (r"/syllabus", SyllabusHandler),
                    (r"/info", StudentInfoHandler),
                    (r"/moment", MomentHandler),
                    (r"/moment/like", MomentLikeHandler),
                    (r"/moment/unlike", MomentUnlikeHandler)]
        self.db = scoped_session(sessionmaker(bind=engine,
                                            autocommit=False,
                                            autoflush=True,
                                            expire_on_commit=False))
        tornado.web.Application.__init__(self, handlers, debug=True)

def token_required(func):
    '''check token required decorator'''
    @wraps(func)
    def _wrapped(self, *args, **kwargs):
        token = self.get_argument("token")
        if SESSION_DICT.get(token):
            return func(self, *args, **kwargs)
        else:
            self.set_status(401)
    return _wrapped

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db_session = self.application.db

    def on_finish(self):
        self.db_session.close()

    def get_student_id(self):
        token = self.get_argument("token")
        return SESSION_DICT[token]["username"]

class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        MAX_RETRY_TIME = 3
        session = session_manager.new_session()
        time = 0
        status = login(username, password, session)
        while status in [LoginStatus.CAPTCHA_ERROR, LoginStatus.UNKNOW] and time < MAX_RETRY_TIME:
            status = login(username, password, session)
            time += 1
        if status == LoginStatus.SUCCESS:
            token = uuid.uuid4().hex
            session_manager.save_session(token, username, password)
            self.write({"stat": True, "data": token})
        elif status == LoginStatus.PASSWORD_ERROR:
            self.write({"stat": False, "data": "Password error"})
        else:
            self.write({"stat": False, "data": "Unknow error"})

class StudentInfoHandler(BaseHandler):
    @token_required
    def get(self):
        token = self.get_argument("token")
        session = session_manager.get_session(token)
        student = self.db_session.query(Student).get(SESSION_DICT[token]["username"])
        if student:
            self.write(student.to_dict())
        else:
            student_info = get_student_info(session)
            student = Student(**student_info)
            try:
                self.db_session.add(student)
                self.db_session.commit()
            except:
                self.db_session.rollback()
            finally:
                self.write(student.to_dict())

class ScoreHandler(BaseHandler):
    @token_required
    def get(self):
        year = int(self.get_argument("year", 2015))
        term = int(self.get_argument("term", 1))
        token = self.get_argument("token")
        session = session_manager.get_session(token)
        score_list = get_score(year, term, session)
        self.write(json.dumps(score_list))

class SyllabusHandler(BaseHandler):
    @token_required
    def get(self):
        year = int(self.get_argument("year", 2015))
        term = int(self.get_argument("term", 1))
        type = self.get_argument("type", "json")
        token = self.get_argument("token")
        session = session_manager.get_session(token)
        syllabus = get_syllabus(year, term, session, type)
        if type == "html":
            self.write(syllabus)
        else:
            self.write(json.dumps(syllabus))

class MomentHandler(BaseHandler):
    @token_required
    def get(self):
        student_id = self.get_student_id()
        moments = self.db_session.query(Moment).order_by(Moment.create_time.desc()).all()
        ret = []
        for moment in moments:
            moment_dict = moment.to_dict()
            moment_dict["isLike"] = (moment.likers.filter_by(student_id=student_id).count() != 0)
            moment_dict["isUnlike"] = (moment.unlikers.filter_by(student_id=student_id).count() != 0)
            ret.append(moment_dict)
        self.write(json.dumps(ret))

    @token_required
    def post(self):
        student_id = self.get_student_id()
        content = self.get_argument("content")
        moment = Moment(student_id, content)
        try:
            self.db_session.add(moment)
            self.db_session.commit()
        except:
            self.db_session.rollback()
        finally:
            self.write(moment.to_dict())

class MomentLikeHandler(BaseHandler):
    @token_required
    def post(self):
        student_id = self.get_student_id()
        moment_id = self.get_argument("moment_id")
        like = MomentLike(student_id, moment_id)
        try:
            self.db_session.add(like)
            self.db_session.commit()
            self.write({"stat": True, "data": "Success!"})
        except:
            self.db_session.rollback()
            self.write({"stat": False, "data": "Failed!"})

class MomentUnlikeHandler(BaseHandler):
    @token_required
    def post(self):
        student_id = self.get_student_id()
        moment_id = self.get_argument("moment_id")
        unlike = MomentUnlike(student_id, moment_id)
        try:
            self.db_session.add(unlike)
            self.db_session.commit()
            self.write({"stat": True, "data": "Success!"})
        except:
            self.db_session.rollback()
            self.write({"stat": False, "data": "Failed!"})


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()