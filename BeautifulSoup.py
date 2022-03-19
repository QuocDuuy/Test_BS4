#!/usr/bin/env python
# coding: utf-8

# ## Beautiful Soup

# ## import thư viện cần thiết

# In[1]:


from bs4 import BeautifulSoup
import requests # cho phép bạn gửi HTTP thông qua Python
import re
import os # thư viện này cho phép thao tác với các thư mục và tệp


# ## Dẫn đến thư mục, tạo đường dẫn và tự động tạo file

# In[4]:



os.chdir("C://Users/ACER/Total/BS4") # os.chdir: dẫn đến cái path này
try:
    os.mkdir("C://Users/ACER/Total/BS4/data") # os.mkdir: tạo folder tên là data ở trong path
except:
    for retry in range(100): # for này sẽ để rename cái tệp data lại trong trường hợp nó bị trùng tên 
        try:
            os.rename('C://Users/ACER/Total/BS4/data','C://Users/ACER/Total/BS4/data')
            print("Success!!!")
            break
        except:
            print('rename failed!!!')
# try:
#     os.mkdir("C://Users/ACER/BeautifulSoup_Selenium/data")
# except:
#     os.remove("C://Users/ACER/BeautifulSoup_Selenium/data")
#     time.sleep(2)
#     os.mkdir("C://Users/ACER/BeautifulSoup_Selenium/data")

os.chdir("C://Users/ACER/Total/BS4/data") # dẫn vào cái folder data để thao tác


# ## Search sản phẩm, lấy dữ liệu qua các trang

# In[5]:


try:    
    search_term = input("What product do you want to search for? ") #search nội dung

    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131" # dẫn vào đường link; {search_team} sẽ được thay thế bằng giá trị đã được nhập phía trên
    page = requests.get(url).text 
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="list-tool-pagination-text").strong #page_text sẽ lấy ra nội dung của tag span trong %%html
    pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
    print('Success!')
except:
    print('Failed')


# ## Lấy dữ liệu: Tên sản phẩm, giá và url dẫn tới sản phẩm đó

# In[6]:




items_found = {} # tạo một cái dictionary cho item

for page in range(1, pages + 1): 
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}" # truy cập tới từng trang trong trang web ứng với sản phẩm đã nhập ở trên
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell") # tìm tag có chứa thông tin của sản phẩm
    items = div.find_all(text=re.compile(search_term)) # re.compile: được sử dụng để biên dịch một mẫu biểu thức chính quy được cung cấp dưới dạng chuỗi thành một đối tượng mẫu regex
    
    for item in items: 
        parent = item.parent # tìm parent cho item; parent là cái tag mà chứa cái item  
        if parent.name != "a": # nếu cái tag name khác tag a
            continue 

        link = parent['href'] # lấy href từ trong cái tag a của parent
        next_parent = item.find_parent(class_="item-container") 
        try:
            price = next_parent.find(class_="price-current").find("strong").string # lấy ra giá tiền là chuỗi string từ tag strong 
            items_found[item] = {"price": int(price.replace(",", "")), "link": link} # add key vào dict ở phía trên; gán thêm giá tiền và đổi thành int; link vào
            print('Success!')
        except:
            pass
        

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price']) # sắp xếp giá tiền theo thứ tự tăng dần


# ## Đưa từng thành phần dữ liệu vào csv; chia thành 3 cột tương ứng 3 giá trị

# In[8]:



try:
    file_name = "data.csv"
    
    data_save_csv = []
    item_title = '{},{},{}\n'.format('Products', 'Price($)', 'URL')
    data_save_csv.append(item_title)
    
    for item in sorted_items:
        item_info = '{},{},{}\n'.format(item[0].replace(',',''),item[1]['price'],item[1]['link'])
        data_save_csv.append(item_info)
        
    with open(os.path.join("C://Users/ACER/Total/BS4/data", file_name), "w+", encoding='utf-8') as f:
        f.writelines(data_save_csv)
    
    print("success!")
    
except:
    
    print('failed!')

