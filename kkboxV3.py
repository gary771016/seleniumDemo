from selenium import webdriver
from selenium.webdriver.common.keys import *
import time
import random
import unittest


class kkbox(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://play.kkbox.com/')
        self.browser.implicitly_wait(7)
        self.browser.maximize_window()
        # time.sleep(3)

    def tearDown(self):
        self.browser.close()

    def find_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath)

    def find_id(self, id):
        return self.browser.find_element_by_id(id)

    def find_class(self, className):
        return self.browser.find_element_by_class_name(className)

    def find_css(self, css):
        return self.browser.find_element_by_css_selector(css)

    # 登入
    def logIn(self):
        # 偶爾會有空白頁面出現
        try:
            self.find_id('uid')
        except:
            self.browser.refresh()
            # time.sleep(5)

        # 輸入帳密
        self.find_id('uid').send_keys('gary_s_cat@hotmail.com')
        self.find_id('pwd').send_keys('g4353194')
        self.find_id('login-btn').click()
        # time.sleep(3)

        # 確認出現KKBOX logo
        try:
            self.find_class('brand').text != 'KKBOX Web Player'
        except:
            assert False
        print("Log: 成功登入")

    # 登出
    def logOut(self):
        self.find_xpath('//i[@class="icon icon-user-dropdown"]').click()
        self.find_xpath('//a[text()="登出"]').click()
        # time.sleep(3)

        # 確認已登出
        try:
            self.find_id('uid')
        except:
            assert False
        print("Log: 成功登出")

    # 確認目標文字正確顯示
    def test_case_1(self):
        self.logIn()

        targetText = ['我的音樂庫', '線上精選', '電台', '一起聽']

        for i in range(len(targetText)):
            try:
                self.find_xpath("//div[@class='sidebar-nav']//*[text()=\'" + targetText[i] + "\']")
            except:
                assert False
        # time.sleep(3)
        print("Log: 4個頁籤文字內容顯示正確")

        self.logOut()
        assert True

    # 搜尋關鍵字和確認目標作者
    def test_case_2(self):
        self.logIn()

        self.find_xpath('//*[@id="search_form"]/input').send_keys('清平調')
        self.find_id('search_btn_cnt').click()
        # time.sleep(3)

        try:
            self.find_xpath('//*[text()="王菲&鄧麗君 (Faye Wong & Teresa Teng)"]')
        except:
            assert False
        print("Log: 目標控件存在")

        self.logOut()
        assert True

    # 自動撥放電台和Dislike
    def test_case_3(self):
        self.logIn()

        self.find_xpath('//*[text()="電台"]').click()
        time.sleep(3)

        # 隨機選擇任一電台
        n = random.randint(1, 5)
        self.find_xpath('//*[@id="promote-stations"]/div/ul/li[' + str(n) + ']/div/div[1]/a/img').click()
        time.sleep(5)

        # 確認專輯圖片改變(開始播放電台)
        try:
            self.find_xpath('//img[@src="//a-play.kfs.io/assets/images/cover.png"]')
        except:
            print("Log: 已開始播放")

        # 選擇Dislike
        beforeAlbum = self.find_xpath('//*[@class="item-h song-name"]').text
        self.browser.find_element_by_xpath('//*[@id="player"]/div[6]/a[1]/i').click()
        time.sleep(5)
        afterAlbum = self.find_xpath('//*[@class="item-h song-name"]').text

        # 確認專輯文字改變(歌曲改變)
        if beforeAlbum == afterAlbum:
            assert False
        print("Log: 歌曲已改變")

        self.logOut()
        assert True


if __name__ == '__main__':
    unittest.main()
