from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import getpass
from datetime import datetime
import os

class FacebookGroupScraper:
    def __init__(self):
        print("\n==== FACEBOOK GROUP MEMBER SCRAPER ====")
        self.get_config()

    def get_config(self):
        try:
            # Thông tin đăng nhập
            print("Nhập thông tin đăng nhập:")
            self.email = input("Email/Username: ").strip()
            self.password = getpass.getpass("Password: ").strip()

            # ID Group
            print("\nNhập ID group Facebook:")
            self.group_id = input("Group ID: ").strip()

            # Số lần scroll
            print("\nSố lần scroll để load thêm thành viên:")
            self.scroll_count = int(input("Số lần scroll (mặc định 5): ") or "5")

        except Exception as e:
            print(f"Lỗi: {e}")

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()  # Đảm bảo driver đã được cài đặt
            self.driver.maximize_window()
        
        except Exception as e:
            print(f"Lỗi khởi tạo trình duyệt: {e}")
            pass

    def login(self):
        try:
            self.driver.get("https://facebook.com")

            # Nhập email
            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys(self.email)

            # Nhập password
            pass_input = self.driver.find_element(By.ID, "pass")
            pass_input.send_keys(self.password)

            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()

            time.sleep(10)
            print("Đăng nhập thành công")
            return True
        except Exception as e:
            print(f"Lỗi đăng nhập: {e}")
            return False

    def get_group_members(self):
        try:
            # Truy cập vào trang thành viên của group
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(5)
            
            members = set()  # Dùng set để không bị trùng lặp
            
            # Thực hiện scroll để tải thêm thành viên
            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                print(f"Scroll lần {i+1}/{self.scroll_count}")
                
                # Thu thập thông tin sau mỗi lần scroll
                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")
                
                for user in user_elements:
                    try:
                        href = user.get_attribute('href')
                        if '/user/' in href:
                            user_id = href.split('/user/')[1].strip('/')  # Lấy ID người dùng
                            name = user.text  # Lấy tên người dùng
                            members.add((user_id, name))  # Thêm vào set
                            print(user_id, name)
                    except Exception as e:
                        continue
            
            return list(members)  # Trả về danh sách thành viên

        except Exception as e:
            print(f"Lỗi khi thu thập thành viên: {e}")
            return []

def main():
    scraper = None

    try:
        scraper = FacebookGroupScraper()
        time.sleep(10)
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi: {e}")

if __name__ == "__main__":
    scraper = FacebookGroupScraper()
    scraper.get_config()
