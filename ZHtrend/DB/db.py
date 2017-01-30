# -*- encoding:utf-8 -*-
import MySQLdb

conn = MySQLdb.connect("127.0.0.1", "root", "Smm", "ZHTrend", use_unicode=True, charset="utf8",
                       connect_timeout=3600)


def AlgoGetQuestionIDs():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT questionid FROM `answer` WHERE DATE_FORMAT(posttime,'%Y-%m-%d')=DATE_FORMAT(now(),'%Y-%m-%d')")
    ret = cursor.fetchall()
    cursor.close()
    return ret


def AlgoGetQuestionID(questionid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM `answer` WHERE DATE_FORMAT(posttime,'%Y-%m-%d')=DATE_FORMAT(now(),'%Y-%m-%d') and questionid = '" +
        questionid[0] + "'")
    ret = cursor.fetchall()
    cursor.close()
    return ret


def AlgoGetFollowers(id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT follower FROM `user` WHERE id = '%s'" % id)
    ret = cursor.fetchall()
    cursor.close()
    return ret


def AlgoDropTable():
    cursor = conn.cursor()
    cursor.execute("drop table if EXISTS Trend_temp;")
    cursor.close()


def AlgoCreateTable():
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE Trend_temp (`questionid`  varchar(255) NOT NULL ,`rank`  int NOT NULL ,PRIMARY KEY (`questionid`));")
    cursor.close()


def AlgoInsertTable(allRank):
    cursor = conn.cursor()
    for i in allRank:
        cursor.execute("INSERT INTO Trend_temp values ('%s','%s')" % (i[0], i[1]))
    conn.commit()
    cursor.close()


def AlgoSwitchTable(table):
    cursor = conn.cursor()
    cursor.execute("RENAME TABLE " + table + " to Trend_Old;")
    cursor.execute("RENAME TABLE Trend_temp to " + table + ";")
    cursor.execute("Drop table if EXISTS Trend_Old;")


def WFGetWord():
    cursor = conn.cursor()
    cursor.execute("SELECT description,profession from user;")
    ret = cursor.fetchall()
    cursor.close()
    return ret


def WFUPloadWF(tags):
    cursor = conn.cursor()
    for i in tags:
        sql = "INSERT INTO wordfrequency values ('%s','%s')" % (i[0], i[1])
        cursor.execute(sql)
    conn.commit()
    cursor.close()


def SITEGetTrend(date):
    date = conn.escape_string(unicode(date).encode("utf8", errors="ignore"))
    sql = "select DISTINCT title,answer.questionid,rank from trend_%s,answer where trend_%s.questionid = answer.questionid  ORDER BY rank DESC limit 30;" % (
        date, date)
    try:
        SITEconn = MySQLdb.connect("127.0.0.1", "root", "root", "ZHTrend", use_unicode=True, charset="utf8",
                       connect_timeout=3600)
        cursor = SITEconn.cursor()
        cursor.execute(sql)
        title = cursor.fetchall()
        cursor.close()
        SITEconn.close()
        return title
    except:
        fail = [["没找到这一天的趋势数据", "#", "0"]]
        return fail


def SpiderActivityGetID():
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM `user` WHERE follower > 500 AND  receivethank > 1000 order by id asc;")
    ret = cursor.fetchall()
    cursor.close()
    return ret


def SpiderActivityInsert(
        id, questionId, answerId, title, total, approve, content, posttime, edittime, comment):
    if check_exist_answer(questionId, answerId):
        print 'exist...', questionId, answerId, title
        return
    content = conn.escape_string(unicode(content).encode("utf8", errors="ignore"))
    cursor = conn.cursor()
    sql = '''INSERT INTO answer VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (
        id, questionId, answerId, title, total, approve, content, posttime, edittime, comment)
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def SpiderActivityCreateDB():
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS answer;")
    cursor.execute('''CREATE TABLE `answer` (
    `id`  VARCHAR(100) NOT NULL ,
    `questionid`  VARCHAR(100) NOT NULL ,
    `answerid`  VARCHAR(100) NOT NULL ,
    `title`  VARCHAR(255) NOT NULL ,
    `total`  INT NOT NULL ,
    `approve`  INT UNSIGNED ZEROFILL NOT NULL ,
    `content`  LONGTEXT NOT NULL ,
    `posttime`  DATETIME NULL ON UPDATE CURRENT_TIMESTAMP ,
    `edittime`  DATETIME NULL ON UPDATE CURRENT_TIMESTAMP ,
    `comment`  INT UNSIGNED ZEROFILL NOT NULL ,
    PRIMARY KEY (`answerid`, `questionid`),
    CONSTRAINT `usertoanswer` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
    )
    ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;
    ''')
    cursor.close()


def SpiderUserCreateDB():
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS user;")
    cursor.execute('''CREATE TABLE `user` (
            `id`  VARCHAR(100) NOT NULL UNIQUE ,
            `name`  VARCHAR(255) NULL ,
            `avatar`  VARCHAR(255) NULL ,
            `description`  VARCHAR(2047) NULL ,
            `profession`  VARCHAR(255) NULL ,
            `sex`  VARCHAR(255) NULL ,
            `answer`  INT UNSIGNED ZEROFILL NOT NULL ,
            `share`  INT UNSIGNED ZEROFILL NOT NULL ,
            `question`  INT UNSIGNED ZEROFILL NOT NULL ,
            `collection`  INT UNSIGNED ZEROFILL NOT NULL ,
            `receiveupprove`  INT UNSIGNED ZEROFILL NOT NULL,
            `receivethank`  INT UNSIGNED ZEROFILL NOT NULL ,
            `receivecollect`  INT UNSIGNED ZEROFILL NOT NULL,
            `follower`  INT UNSIGNED ZEROFILL NOT NULL ,
            `following`  INT UNSIGNED ZEROFILL NOT NULL ,
            `spsonsorlive`  INT UNSIGNED ZEROFILL NOT NULL ,
            `interesttopic`  INT UNSIGNED ZEROFILL NOT NULL ,
            `interestcolumn`  INT UNSIGNED ZEROFILL NOT NULL ,
            `interestquestion`  INT UNSIGNED ZEROFILL NOT NULL ,
            `interestcollection`  INT UNSIGNED ZEROFILL NOT NULL ,
            PRIMARY KEY (`id`)
            )
            ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;''')
    cursor.close()


def SpiderUserGetIDs():
    cursor = conn.cursor()
    cursor.execute("SELECT id from user;")
    ret = cursor.fetchall()
    cursor.close()
    return ret




def check_exist_answer(questionid, answerid):
    cursor = conn.cursor()
    cursor.execute("SELECT id from answer where questionid='%s' and answerid='%s' limit 1;"%(questionid, answerid))
    ret = cursor.fetchall()
    cursor.close()
    return ret

def check_exist_user(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id from user where id='%s' limit 1;"%user_id)
    ret = cursor.fetchall()
    cursor.close()
    return ret


def SpiderUserInsert(id, name, avatar,  description, profession, sex, answer, share, question, collection,
                     receiveupprove,
                     receivethank, receivecollect, follower, following, spsonsorlive, interesttopic, interestcolumn,
                     interestquestion, interestcollection):
    if check_exist_user(id):
        print 'exist.....', id
        return
    cursor = conn.cursor()
    description = conn.escape_string(unicode(description).encode("utf8", errors="ignore"))
    profession = conn.escape_string(unicode(profession).encode("utf8", errors="ignore"))

    sql = "INSERT INTO user VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
          % (id, name,avatar, description, profession, sex, answer, share, question, collection,
             receiveupprove,
             receivethank, receivecollect, follower, following, spsonsorlive, interesttopic, interestcolumn,
             interestquestion, interestcollection)
    sql = sql.encode("utf8", errors="ignore")
    cursor.execute(sql)
    conn.commit()
    cursor.close()


'''
mysql> select count(*) from answer limit 1;
+----------+
| count(*) |
+----------+
|     4235 |
+----------+
1 row in set (0.00 sec)

mysql> select count(*) from user limit 1;
+----------+
| count(*) |
+----------+
|    25753 |
+---------
'''