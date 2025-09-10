import os
import pymysql
from flask import current_app, g

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_NAME = os.getenv("DB_NAME", "MINI_ATS")


def get_db():
    if "db" not in g:
        g.db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME, autocommit=False)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS MINI_ATS;")
    cur.execute("USE MINI_ATS;")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data (
            ID INT NOT NULL AUTO_INCREMENT,
            sec_token varchar(512) NOT NULL,
            ip_add varchar(50) NULL,
            host_name varchar(50) NULL,
            dev_user varchar(50) NULL,
            os_name_ver varchar(50) NULL,
            latlong varchar(50) NULL,
            city varchar(50) NULL,
            state varchar(50) NULL,
            country varchar(50) NULL,
            act_name varchar(50) NOT NULL,
            act_mail varchar(50) NOT NULL,
            act_mob varchar(20) NOT NULL,
            Name varchar(500) NOT NULL,
            Email_ID VARCHAR(500) NOT NULL,
            resume_score VARCHAR(8) NOT NULL,
            Timestamp VARCHAR(50) NOT NULL,
            Page_no VARCHAR(5) NOT NULL,
            Predicted_Field BLOB NOT NULL,
            User_level BLOB NOT NULL,
            Actual_skills BLOB NOT NULL,
            Recommended_skills BLOB NOT NULL,
            Recommended_courses BLOB NOT NULL,
            pdf_name varchar(50) NOT NULL,
            PRIMARY KEY (ID)
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_feedback (
            ID INT NOT NULL AUTO_INCREMENT,
            feed_name varchar(50) NOT NULL,
            feed_email VARCHAR(50) NOT NULL,
            feed_score VARCHAR(5) NOT NULL,
            comments VARCHAR(100) NULL,
            Timestamp VARCHAR(50) NOT NULL,
            PRIMARY KEY (ID)
        );
        """
    )
    db.commit()
