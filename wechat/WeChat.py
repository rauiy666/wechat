import time

import itchat
from itchat.content import TEXT
from googletrans import Translator
from Box import Box
from MovieComing import MovieComing
from duanzi.duanzi.MysqlConnect import MysqlHelper


@itchat.msg_register(TEXT)
def get_msg_and_reply(msg):
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(msg['CreateTime'])))
    rec_msg = msg['Content'].strip()
    is_bot_reply = get_bot_setting("is_bot_reply")
    if is_bot_reply == "error":
        set_bot_setting("is_bot_reply", "False")
    if msg['User']['NickName'] == my_name:
        if rec_msg == "stop":
            set_bot_setting("is_bot_reply", "False")
            print("自动回复已经停止！")
            write_log("用户“%s”已经停止了自动回复功能！" % my_name)
        elif rec_msg == "start":
            set_bot_setting("is_bot_reply", "True")
            print("自动回复功能开启")
            write_log("用户“%s”已经开启了自动回复功能！" % my_name)
        else:
            print("新消息@ (%s)对方：%s  内容：%s  （自己的消息不会自动回复！）" % (create_time, my_name, rec_msg))
        return
    from_user_name = msg['FromUserName']
    if is_bot_reply == "True":
        name = ""
        for u in users:
            if from_user_name == u['user_name']:
                name = u['rel_name'] if u['rel_name'] else u['nick_name']
                break
        if name:
            if rec_msg == '1':
                duanzi = get_duanzi()[0]
                a_id = duanzi[0]
                article = "(*^__^*) " + duanzi[1]
                write_log("回复“%s”的笑话，笑话id：%s" % (name, a_id))
                return article
            elif rec_msg == '2':
                result = get_movie()[0]
                m_id = result[0]
                cn_name = result[1]
                en_name = result[2]
                director = result[3]
                actors = result[4]
                movie_type = result[5]
                box_count = result[6]
                duration = result[7]
                release_time = result[8]
                zhishi = result[9]
                distributor = result[11]
                img_url = result[12]
                reply_msg = "电影推荐：\n中文名：%s\n英文名：%s\n导演：%s\n主演：%s\n电影类型：%s\n总票房：%s\n时长：%s\n上映时间：%s\n制式：%s\n发行：%s\n海报：%s" % (
                    cn_name, en_name, director, actors, movie_type, box_count, duration, release_time, zhishi, distributor,
                    img_url)
                write_log("回复“%s”的电影推荐，电影cid：%s" % (name, m_id))
                return reply_msg
            elif rec_msg == '3':
                write_log("回复“%s”查看院线热映电影！" % name)
                reply_msg = "查看院线热映电影\n查看所有热映电影票房等信息，请回复：31\n查找某电影在映信息，回复：32@（电影名）\
                如：32@我和我的祖国\n查看国内今天当前总票房，回复：33\n查看当前热映电影，回复：34"
                return reply_msg
            elif rec_msg == '31':
                box = Box()
                movies = box.get_movies()
                if not movies == 'error':
                    total_box = movies[0]['total_box']
                    server_time = movies[0]['server_time']
                    del movies[0]
                    reply_msg = '数据时间：%s\n今日实时：%s万\n\n' % (server_time, total_box)
                    for movie in movies:
                        res_msg = "电影名：%s\n上映天数：%s\n今日票房：%s万\n总票房：%s\n票房占比：%s\n排片场次：%s\n排片比：\
                        %s\n均场人数：%s\n上座率：%s\n\n" % (
                            movie['name'], movie['release_info'], movie['box_info'], movie['sum_box_info'],
                            movie['box_rate'],
                            movie['show_info'], movie['show_rate'], movie['avg_show_view'], movie['avg_seat_view'])
                        reply_msg += res_msg
                    write_log("回复“%s”，查看今日热映电影数据" % name)
                    return reply_msg
                else:
                    write_log("“%s”的查看所有热映电影数据异常！" % name)
                    return "网络异常，请稍后重试！"
            elif rec_msg.startswith('32'):
                rec_msg.strip()
                words = rec_msg.split("@")
                if len(words) == 2:
                    if not words[1] == '':
                        box = Box()
                        movies = box.find_movies(words[1])
                        if not movies == "error":
                            if movies:
                                res_msg = ""
                                for movie in movies:
                                    res_msg += "电影名：%s\n上映天数：%s\n今日票房：%s万\n总票房：%s\n票房占比：%s\n排片场次：%s\n \
                                    排片比：%s\n均场人数：%s\n上座率：%s\n\n" % (
                                        movie['name'], movie['release_info'], movie['box_info'], movie['sum_box_info'],
                                        movie['box_rate'],
                                        movie['show_info'], movie['show_rate'], movie['avg_show_view'],
                                        movie['avg_seat_view'])
                                    write_log("回复“%s”，查看“%s”关键字的电影票房数据！" % (name, words[1]))
                                return res_msg
                        else:
                            write_log("“%s”的查看“%s”关键字的电影票房数据异常！" % (name, words[1]))
                            return "网络异常，请稍后重试！"
                return "自动回复消息：\n出错：\n1、没有按照格式输入\n2、该电影未上映或已下映或没有改电影\n3、电影名称输入有误"
            elif rec_msg == '33':
                box = Box()
                info = box.get_count_box()
                if not info == "error":
                    reply_msg = "截止时间：%s\n当日当前总票房：%s万" % (info['server_time'], info['total_box'])
                    write_log("回复“%s”查看今日总票房！" % name)
                    return reply_msg
                else:
                    write_log("回复“%s”的查看所有热映电影数据异常！" % name)
                    return "网络异常，请稍后重试！"
            elif rec_msg == '34':
                box = Box()
                movies = box.get_online_movies()
                if not movies == "error":
                    reply_msg = "今日共有%d部电影热映中\n" % len(movies)
                    for movie in movies:
                        reply_msg += movie + "\n"
                    write_log("回复“%s”查看今日所有热映电影名称！" % name)
                    return reply_msg
                else:
                    write_log("“%s”的查看所有热映电影数据异常！" % name)
                    return "网络异常，请稍后重试！"
            elif rec_msg == '4':
                reply_msg = "查看所有即将上映电影，请回复：41\n\n查询即将上映电影，请回复：42@（电影名） 如42@中国机长"
                return reply_msg

            elif rec_msg == '41':
                coming = MovieComing()
                movies = coming.get_all_movies()
                if movies == 'error':
                    log_msg = "回复“%s”的查询所有机上上映电影错误" % name
                    reply_msg = "自动回复消息：网络错误，请稍后重试！"
                elif movies:
                    log_msg = "回复“%s”查询所有即将上映的电影成功" % name
                    reply_msg = ""
                    for movie in movies:
                        reply_msg += "电影名：%s\n类型：%s\n地区：%s\n上映时间：%s\n\n" % (movie['name'], movie['type'], movie['location'], movie['movie_time'])
                else:
                    log_msg = "回复“%s”查询所有即将上映的电影，没有找到数据！"
                    reply_msg = "自动回复消息：暂时没有数据！"
                write_log(log_msg)
                return reply_msg
            elif rec_msg.startswith("42"):
                if rec_msg.startswith("42@"):
                    words = rec_msg.split("@")
                    if not words[1] == "":
                        coming = MovieComing()
                        movies = coming.find_movies(words[1])
                        if movies == "error":
                            write_log("回复“%s”的查询关键字即将上映电影错误" % name)
                            return "自动回复消息：网络错误，请稍后重试！"
                        log_msg = "回复“%s”查找“%s”关键字的即将上映电影成功" % (name, words[1])
                        reply_msg = ""
                        for movie in movies:
                            reply_msg += "电影名：%s\n类型：%s\n地区：%s\n上映时间：%s\n\n" % (
                            movie['name'], movie['type'], movie['location'], movie['movie_time'])
                        write_log(log_msg)
                        return reply_msg
                log_msg = "回复“%s”查找关键字的即将上映电影失败，输入：%s" % (name, rec_msg)
                write_log(log_msg)
                return "自动回复消息：\n出错：\n1、没有按照格式输入\n2、没有该电影的即将上映信息"
            elif rec_msg.startswith('5'):
                if rec_msg.startswith('5@'):
                    words = rec_msg.split('@')
                    if not words[1] == '':
                        trans = Translator(service_urls=['translate.google.cn'])
                        text = trans.translate(words[1]).text
                        reply_msg = "原文：%s\n译文：%s" % (words[1], text)
                        write_log("回复“%s”翻译，内容：%s" % (name, words[1]))
                    else:
                        reply_msg = "请输入要翻译内容！"
                        write_log("回复“%s”翻译，错误，未输入需要翻译的内容，对方的输入：%s！" % (name, rec_msg))
                else:
                    reply_msg = '中英文翻译请按照“5@（翻译文）”格式输入，如：5@你好！'
                    write_log("回复“%s”，需要翻译，对方输入：%s" % (name, rec_msg))
                return reply_msg
            elif rec_msg == "0":
                reply_msg = "<Clone with HTTPS>https://github.com/rauiy666/wechat.git"
                write_log("回复“%s”，获取项目clone地址：%s" % (name, reply_msg))
                return reply_msg
            else:
                message = "新消息@ (%s)对方：%s  内容：%s" % (create_time, name, rec_msg)
                print(message)
                write_log(message)
                local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                reply_msg = "%s,这是“%s”的自动回复消息：我正在忙，请稍后联系我哦，谢谢！\n\n看笑话，回复：1\n\n电影推荐，回复：2\n\n实时票房，回复：3\n\n即将上映电影，回复：4\n\n中英文翻译，回复：5\n\n获取本项目源代码，回复：0" % (
                    local_time, my_name)
                write_log("回复“%s”消息：%s" % (name, reply_msg.replace("\n", "")))
                return reply_msg


def get_bot_setting(setting_name):
    config_path, lines = read_config_lines()
    for line in lines:
        key_words = line.strip().split("=")
        if key_words[0].strip() == setting_name:
            write_log("读取配置：%s" % line)
            return key_words[1].strip()
        else:
            write_log("读取配置文件错误，在“%s”中没有“%s”的配置" % (config_path, setting_name))
            return 'error'


def read_config_lines():
    config_path = "config/config.conf"
    with open(config_path, "r") as f:
        return config_path, f.readlines()


def set_bot_setting(setting_name, setting_words):
    config_path, lines = read_config_lines()
    # lines = [{x[0].strip(): x[1].strip()} for x in lines.strip().split("=")]
    index = len(lines)
    old_line = ''
    has_same_setting = False
    for line in lines:
        if line.strip().startswith(setting_name+"="):
            if line.strip().endswith(setting_words):
                has_same_setting = True
            old_line = line
            lines.remove(line)
            break
    if not has_same_setting:
        new_line = setting_name + "=" + setting_words
        if index == len(lines):
            msg = "用户“%s”增加了设置配置：%s" % (my_name, new_line)
            print(msg)
        else:
            msg = "用户“%s”修改了配置，将“%s”修改为“%s”" % (my_name, old_line, new_line)
            print(msg)
        write_log(msg)
        lines.append(new_line)
        file_content = "\n".join(lines)
        with open(config_path, "w") as f:
            f.write(file_content)
    else:
        print("用户“%s”该设置配置与您指定的相同，配置：%s！" % (my_name, old_line))


def write_log(msg):
    t_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    msg = t_time + "        " + msg + "\n\n"
    with open("weChat.log", "a+", encoding="utf-8") as f:
        f.write(msg)


def get_duanzi():
    db = MysqlHelper(mysqldb='duanzi')
    sql = "select * from articles order by rand() LIMIT 1"
    result = db.find_all(sql)
    db.close()
    return result


def get_movie():
    db = MysqlHelper(mysqldb='movies')
    sql = "select * from cn_movies order by rand() LIMIT 1"
    result = db.find_all(sql)
    db.close()
    return result


def get_user_info():
    friends = itchat.get_friends(update=True)
    me = friends[0]['NickName']
    print("欢迎登陆：", me)
    del friends[0]
    user_list = []
    for friend in friends:
        if friend['Sex'] == 2:
            sex = "女"
        else:
            sex = "男"
        location = friend['Province'] + " " + friend['City']
        dict_user = {"user_name": friend['UserName'], "nick_name": friend['NickName'], 'rel_name': friend['RemarkName'],
                     "sex": sex, 'location': location}
        user_list.append(dict_user)
    return user_list, me


if __name__ == '__main__':
    itchat.auto_login()
    users, my_name = get_user_info()
    is_bot_reply = get_bot_setting("is_bot_reply")
    if is_bot_reply == "False":
        print("自动回复功能已经关闭！")
    elif is_bot_reply == "True":
        print("自动回复已经功能开启！")
    itchat.run()
