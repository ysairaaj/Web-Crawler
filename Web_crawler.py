from bs4 import BeautifulSoup
import requests
import sys
import time
def main():
    html_pages = requests.get('https://www.primeabgb.com/buy-online-price-india/graphic-cards-gpu/?filters=_stock_status[instock]').text
    soup = BeautifulSoup(html_pages , 'lxml')
    grp1 = soup.find('ul',class_ = 'products auto-clear equal-container')
    grps = grp1.find_all('li')
    #print(grps)
    f = open(r'C:\Users\hp\AppData\Local\atom\available_gpus.csv','w+')
    f.write('gpus , price \n')
    grp2 = soup.find('nav' ,class_ = 'woocommerce-pagination')
    lst = []
    for i in grp2.find_all('a' , class_ = 'page-numbers'):
        #print(i['class'])
        if i['class'][0] == 'page-numbers':
            lst.append(i['href'])
    #print(lst)
    for grp in grps :
        x1 = grp.find('div' , class_ = "product-innfo").h3.a.text
        print( x1,end = ' ')
        f.write(x1 + ',')
        try:
            x2 = grp.find('div' , class_ = "product-innfo").find('ins').find('bdi').text
            print(x2)
            f.write(x2[1:].replace(',' ,'') + '\n')
        except :
            print('price not available')
            f.write('- \n')
            pass
    if len(lst) >0:
        pagination(lst,f)
def pagination(lst,f):
    print('\n pagination detected \n Retreiving pages \n')
    for i in lst:
        retry_count = 0
        success =0
        while retry_count < 2:
            try:
                html_pages1 =  requests.get(i).text
                soup1 = BeautifulSoup(html_pages1 , 'lxml')
                grp1 = soup1.find('ul',class_ = 'products auto-clear equal-container')
                grps = grp1.find_all('li')
                for grp in grps :
                    x1 = grp.find('div' , class_ = "product-innfo").h3.a.text
                    print( x1,end = ' ')
                    f.write(x1 + ',')
                    try:
                        x2 =grp.find('div' , class_ = "product-innfo").find('ins').find('bdi').text
                        print(x2)
                        f.write(x2[1:].replace(',','') + '\n')
                    except :
                        print('price not available')
                        f.write('- \n')
                        pass
                success =1
                break
            except :
                print('\n connection failed ----- retrying \n')
                retry_count += 1
                continue
        if success == 0:
            print('\n failed to retreive document ------- force skipping \n')

if __name__ == '__main__':
    while 1:
        try :
            main()
            time.sleep(10)
        except :
            print('failed ----- exiting')
            sys.exit(0)
