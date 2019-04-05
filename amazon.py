# coding:utf-8
import sys, requests, sqlite3, webbrowser
from time import sleep, time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QListView
from resource.amazon import Ui_Form


DB_URI = 'spider.dll'
class Db(object):
    __instance = None
    def execute(self,sql):
        try:
            return self.__cur.execute(sql)
        except Exception as e:
            print(e)

    def commit(self):
        self.__con.commit()

    def close(self):
        self.__con.close()

    def __new__(cls):
        if cls.__instance : return cls.__instance
        try:
            cls.__con = sqlite3.connect(DB_URI)
            cls.__cur = cls.__con.cursor()
        except Exception as e:
            print(e)
            return False
        return object.__new__(cls)

class Api(QThread):
    # 关键词查询
    '''
    session-id: 130-1670416-5070846
    customer-id:
    request-id: 2Y1GZ8K2X1CCPEWJGNG9
    page-type: Gateway
    lop: en_US
    site-variant: desktop
    client-info: amazon-search-ui
    mid: ATVPDKIKX0DER   (为必选)
    alias: aps  (为必选)
    prefix: lace  (为必选, 是要查询的关键词)
    b2b: 0
    fresh: 0
    ks: 32
    event: onKeyPress
    limit: 11
    fb: 1
    '''
    #
    __url = 'https://completion.amazon.com/api/2017/suggestions'

    __err = ''
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    keywords_sel_trigger = pyqtSignal(list)
    error_trigger = pyqtSignal(str)

    def __init__(self, parent=None, keywords=[],deep=1):
        super(Api,self).__init__(parent)
        self.__keywords = keywords
        self.__deep = deep

    def run(self):
        for keyword in self.__keywords:
            results = self.get(keyword)
            if self.__deep == 2 :
                for res in results:
                    rows = self.get(res)
                    self.keywords_sel_trigger.emit(rows)
            else: self.keywords_sel_trigger.emit(results)
            sleep(2)
        self.error_trigger.emit(self.__err)

    def get(self,keyword):
        data = {
            'mid': 'ATVPDKIKX0DER',
            'alias': 'aps',
            'prefix' : keyword
        }
        results = []
        try:
            resp = requests.get(self.__url,headers=self.__headers, params=data)
            result = resp.json()
            result = result.get('suggestions')
            if not result: self.__err = '无相关数据可查'
            results = [rd['value'] for rd in result]
        except:
            self.__err = 'HTTP连接错误'
        return results

class Amazon(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('QComboBox QAbstractItemView::item {min-height: 26px}')
        self.setupUi(self)
        self.dropdown.setView(QListView())
        self.count=0
        ad = Ad(self)
        ad.start()

    def input_check_slot(self):
        keywords = self.input.text()
        enabled = True if len(keywords) > 0 else False
        keywords = keywords.split(',')
        self.__keywords = keywords
        self.submit.setEnabled(enabled)

    def submit_slot(self):
        self.count = 0
        self.editor.clear()
        deep = self.dropdown.currentText()
        deep = '等级1' if deep == '挖掘深度' else deep
        deep = int(deep.replace('等级',''))
        self.status.setText('开始查询...')
        self.thread = Api(self, keywords=self.__keywords, deep=deep)
        self.thread.keywords_sel_trigger.connect(self.editor_insert)
        self.thread.error_trigger.connect(self.editor_error)
        self.thread.start()

    def editor_repeat_slot(self):
        text = self.editor.toPlainText()
        rows = list(set(text.split('\n')))
        rows = [row for row in rows if row != '']
        rows.sort()
        self.editor.clear()
        for row in rows: self.editor.insertPlainText(row+'\n')
        self.status.setText('完成! 共获取[%s]条数据'%len(rows))

    def editor_insert(self, results):

        for keyword in results:
            self.editor.insertPlainText(keyword+'\n')
            self.count+=1
            self.status.setText('查询中:%s'%self.count)

    def editor_error(self,error):
        if error =='':
            self.status.setText('查询完成,共获得[%s]条数据'%self.count)
        else:
            self.status.setText('提示:%s'%error)

        self.thread.quit()

class Ad(QThread):

    def __index(self):
        #当时间时间
        curr_time = int(time())
        db = Db()
        # 查询
        res = db.execute('select heji,pop2 from amz where id = 1').fetchall()[0]
        heji = res[0]  # 统计弹出次数
        pop2 = res[1]  # 最后弹出时间
        # 最后弹出时间为0 代表第一次使用
        if pop2 == 0:
            db.execute('update amz set pop2=%d where id = 1' % curr_time)
            db.commit()
        # 最
        elif curr_time - pop2 > 3.5 * 24 * 3600:
            print('ad...')
            db.execute('update amz set pop2=%d, heji=%d where id = 1' % (curr_time, heji + 1))
            db.commit()
            return True
        db.close()
        return False

    def get_ad_url(self):
        #当前时间
        curr_time = int(time())
        db = Db()
        # 获取广告最后更新时间
        res = db.execute('select ad_up_time from amz where id = 1').fetchall()[0]
        ad_up_time = res[0]
        # 广告每7天更新一次
        if curr_time - ad_up_time > 7*24*3600:
            # 更新广告时间
            db.execute('update amz set ad_up_time=%s'%curr_time)
            # 下载广告链接
            res = requests.get('https://raw.githubusercontent.com/mina998/data/master/ad_taobao_amz')
            if res.status_code != 200: return False
            urls = res.text.split('\n')
            urls = [url for url in urls if url !='']
            # 删除数据
            db.execute('delete from ad where id > 0')
            db.commit()
            # 从新添加数据
            for url in urls: db.execute('insert into ad (url) values ("%s")'% url)
            db.commit()
        else:
            url = db.execute('select url from ad order by random() limit 1').fetchall()[0]
            url = url[0]
        db.close()
        return url

    def run(self):
        url = self.get_ad_url()
        # print(url)
        while True:
            index = self.__index()
            if index:
                sleep(10)
                webbrowser.open_new_tab(url)
                webbrowser.height=100
            sleep(5)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Amazon()
    win.show()

    sys.exit(app.exec_())