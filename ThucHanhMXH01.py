import facebook
import json
from datetime import datetime
from collections import defaultdict
import pandas as pd

class FacebookCollector:
    def __init__(self, EAAHmdslmzRoBO03zZBF9TlCznlWPkLKcS2UdBpOdjYTETqWkuZBmhVZCVlnuEZBMjlyNHZBKsjXuDhTFZCuOEYejuVCnCzZCEKaLbDiY0TEolizjhtpZCWYozPnqQM24xyukMFpnWkSlm5bVZCvPCe7gFIgm7EIX93Y4FWrw0wro1tWNsHgZBZCD0c72HyMK0WPAdOcliU09dZBl8mbgc3LxncqfwG8LK0vO12Q4N0BiOstqRZBVZApgzUTU2yARaE20TliwZDZD):
        try:
            self.access_token = EAAHmdslmzRoBO03zZBF9TlCznlWPkLKcS2UdBpOdjYTETqWkuZBmhVZCVlnuEZBMjlyNHZBKsjXuDhTFZCuOEYejuVCnCzZCEKaLbDiY0TEolizjhtpZCWYozPnqQM24xyukMFpnWkSlm5bVZCvPCe7gFIgm7EIX93Y4FWrw0wro1tWNsHgZBZCD0c72HyMK0WPAdOcliU09dZBl8mbgc3LxncqfwG8LK0vO12Q4N0BiOstqRZBVZApgzUTU2yARaE20TliwZDZD
            self.graph = facebook.GraphAPI(EAAHmdslmzRoBO03zZBF9TlCznlWPkLKcS2UdBpOdjYTETqWkuZBmhVZCVlnuEZBMjlyNHZBKsjXuDhTFZCuOEYejuVCnCzZCEKaLbDiY0TEolizjhtpZCWYozPnqQM24xyukMFpnWkSlm5bVZCvPCe7gFIgm7EIX93Y4FWrw0wro1tWNsHgZBZCD0c72HyMK0WPAdOcliU09dZBl8mbgc3LxncqfwG8LK0vO12Q4N0BiOstqRZBVZApgzUTU2yARaE20TliwZDZD)
        except Exception as e:
            print(f"Lỗi khởi tạo: {e}")
    
    def check_token_validity(self):
        try:
            me = self.graph.get_object('me', fields='id,name')
            print("Token hợp lệ")
            return True
        except Exception:
            print("Token không hợp lệ")
            return False
        
    def collect_data(self, limit=5):
        try:
            fields = ('id', 'message', 'created_time')
            posts = self.graph.get_object('me/feed')
            
            for post in posts.get('data',[]):
                print("--------------")
                print(post.get('message'))
                print("----------")
            return posts  # Trả lại dữ liệu thu thập
        except Exception:
            pass

    def json_to_excel(self, my_json, excel_file=None):
        posts = []
        for post in my_json['data']:
            post_data = {
                'id': post.get('id', ''),
                'created_time': post.get('created_time', ''),
                'message': post.get('message', '')
            }
            posts.append(post_data)
        
        df = pd.DataFrame(posts)
        df['created_time'] = pd.to_datetime(df['created_time'])
        df['created_time'] = df['created_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        if excel_file:
            df.to_excel(excel_file, index=False)
        
        return df  # Nếu cần trả lại dataframe

def main():
        ACCESS_TOKEN = 'EAAHmdslmzRoBO03zZBF9TlCznlWPkLKcS2UdBpOdjYTETqWkuZBmhVZCVlnuEZBMjlyNHZBKsjXuDhTFZCuOEYejuVCnCzZCEKaLbDiY0TEolizjhtpZCWYozPnqQM24xyukMFpnWkSlm5bVZCvPCe7gFIgm7EIX93Y4FWrw0wro1tWNsHgZBZCD0c72HyMK0WPAdOcliU09dZBl8mbgc3LxncqfwG8LK0vO12Q4N0BiOstqRZBVZApgzUTU2yARaE20TliwZDZD'
        collector = FacebookCollector(ACCESS_TOKEN)

        if collector.check_token_validity():
            posts = collector.collect_data(limit=2)  # Lưu posts
            collector.json_to_excel(posts)  # Gọi phương thức json_to_excel với posts đã thu thập
            
if __name__ == "__main__":
    main()
