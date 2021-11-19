# -*- coding = utf-8 -*-
import nmap, os, schedule, smtplib, pprint                                                    # pip3 install python-nmap
import threading,time,netmiko,getpass,gevent,re
from queue import Queue          
from gevent import monkey; monkey.patch_all()                # gevent 不知IO操作，如urllib,需要打这个补丁,patch_all()把当前程序的所有IO操作给单独标记
from gevent import greenlet                                  #发送邮件模块
from email.mime.text import MIMEText                         #定义邮件内容
from email.mime.multipart import MIMEMultipart               #用于传送附件
from email.mime.application import MIMEApplication
from email.header import Header
from dev_scan_email import dev_email
                                         

def nmap_scan(ip, port):
  # print('程序运行中:')                                        # 测试一次并发数量     
  if os.path.exists(r'nmap\error.txt'):                        #58.248.224.138
    os.remove(r'nmap\error.txt')             
  portlist = '443'
                                         
  try:
    nscan = nmap.PortScanner()
    result = nscan.scan(ip, str(portlist))
    # pprint.pprint(result)                                         # scan是key， 后面的字典操作都是value
    # print('-'*80)
    state = result['scan'][ip]['tcp'][int(portlist)]['state']
    #ipadd = sorted(ips,key=lambda ip:ipaddress.ip_address(ip))
    print(ip.strip()+ '\t'*2+ ' TCP:' + portlist + '\t'*2 + state)
 
    if state != 'open': 
      file = open(r'nmap/error.txt','a+')
      file.write(ip.strip() + '\t' + 'Port error' + '\n')
      file.close()
      
  except:
      print(ip.strip() + '\t'*5+ 'Network error')
      file1 = open(r'nmap/error.txt','a+')
      file1.write(ip.strip() + '\t' + 'Network error' + '\n')
      file1.close
  
def main():                                                                  
  print('Program Start:')
  begin = time.time()                                                        # q = Queue(), q.put(ip),q.get(ip)
  glist = []
  iplist = open(r'nmap/iplist.txt','r',encoding='utf-8')  
  for ip in iplist.readlines():                                              
      # q.put(ip)
      t = gevent.spawn(nmap_scan, ip.strip(), Queue())                       # queue的简洁方式使用                     
      t.start()
      glist.append(t) 
  for t in glist:
      t.start()                                                              # 也可在这里做队列
  for t in glist:
      t.join()
  stop = time.time()
  runtime = stop - begin
  print('Scan Time：%.1f秒'%runtime )
  iplist.close()
  if os.path.exists(r'nmap\error.txt'):
    dev_email()                                                                # 函数调用

if __name__ == '__main__':
  main()


# if __name__ == '__main__':
#   schedule.every(20).minutes.do(main)
#   while True:
#     schedule.run_pending()

  




