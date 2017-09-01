from urllib.request import urlretrieve
import requests  
from bs4 import BeautifulSoup  
import sys
import os
  
def show_block_fn(fn):
    def show_block(a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        bl = "[" + "*" * int(per / 2.5) + "-" * (40 - int(per / 2.5)) + "]"
        print("\t%s:%s %.2f%%" % (fn, bl, per))
    return show_block

def download_file(url, idx):
    local_filename = url.split('/')[-1]  
    # NOTE the stream=True parameter  
    r = requests.get(url, stream=True)
    try:
        urlretrieve(url, folder + '/' + local_filename, show_block_fn(local_filename))
    except:
        print("Error: " + url)
    """
    with open(folder + '/' + local_filename, 'wb') as f:  
      for chunk in r.iter_content(chunk_size=1024):  
          if chunk: # filter out keep-alive new chunks  
              f.write(chunk)  
              f.flush()
    """
    return None  

root_link=str(sys.argv[1])

folder = str(sys.argv[2])

suffix = ['.pdf', '.ppt', '.pptx', '.doc', '.docx', 'tar.gz', '.zip', '.rar']

try:
    os.mkdir(folder) 
except:
    print("Folder already exists: {}".format(folder))

r = requests.get(root_link)  

if r.status_code == 200:  
    soup = BeautifulSoup(r.text, 'lxml')  
    # print unicode(soup.prettify())
    # print soup.find_all('a')  
    idx = 1  
    for link in soup.find_all('a'):  
        if link.get('href') != None:
            if len(sys.argv) == 3:
                new_link = root_link + '/' + link.get('href')
            else:
                new_link = sys.argv[3] + '/' + link.get('href')
            for suf in suffix:  
                if new_link.endswith(suf):  
                    print("\nDownloading: " + new_link + " -> " + new_link.split('/')[-1])  
                    download_file(new_link,str(idx))  
                    idx += 1  
    print("All download finished")  
else:  
    print("A errors occurs.")  