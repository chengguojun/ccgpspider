# import datetime
#
#
# def m_date():
#     begin = datetime.date(2013, 1, 1)
#     end = datetime.date(2017, 5, 15)
#     for i in range((end - begin).days + 1):
#         day = begin + datetime.timedelta(days=i)
#         print (i for i in str(day).split('-'))
#
# if __name__ == '__main__':
#         m_date()

# import datetime
#
# begin = datetime.date(2013, 1, 1)
# end = datetime.date(2017, 5, 15)
#
# d = begin
# delta = datetime.timedelta(days=1)
# while d <= end:
#     print d.strftime("%Y-%m-%d")
#     d += delta

# import requests
# COOKIE={'_gscu_273633028':'948196655cr1vr28', '_gscbrs_273633028':'1','JSESSIONID':'i_IK2N-Tg2NI2NesUjtbnYlUErUNxfqJZD77FRaZGJGRfI9vMw6B!613145647', '__cc_verify__qssec_':'jekxqrh7Sdyhs6nQeQjZNquB2mhNBTZJ', 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5':'1494818756', 'Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5':'1494832247'}
#
# cookies='_gscu_273633028=948196655cr1vr28; _gscbrs_273633028=1; JSESSIONID=i_IK2N-Tg2NI2NesUjtbnYlUErUNxfqJZD77FRaZGJGRfI9vMw6B!613145647; __cc_verify__qssec_=jekxqrh7Sdyhs6nQeQjZNquB2mhNBTZJ; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1494818756; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1494832247'
# url ='http://search.ccgp.gov.cn/dataB.jsp?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=2013%3A01%3A01&end_time=2013%3A01%3A01&timeType=6&displayZone=&zoneId=&pppStatus=&uniqid=23412&randnum=2427&agentName='
#
# bo=requests.get(url,cookies=COOKIE)
# print bo.content
#
import re

url = "http://search.ccgp.gov.cn/dataB.jsp?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=2013%3A01%3A01&end_time=2013%3A01%3A01&timeType=6&displayZone=&zoneId=&pppStatus=&agentName="



print url.replace(re.findall("page_index=(\d+)",url)[0],"%s")






























