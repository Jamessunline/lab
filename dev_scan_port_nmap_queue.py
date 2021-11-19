# -*- coding = utf-8 -*-
import nmap, os, schedule, smtplib, pprint                                                    
import threading,time,netmiko,getpass,gevent,re
from queue import Queue          
from gevent import monkey; monkey.patch_all()               
from gevent import greenlet                                 
from email.mime.text import MIMEText                         
from email.mime.multipart import MIMEMultipart               
from email.mime.application import MIMEApplication
from email.header import Header                         

def nmap_scan(ip, port):                                   
  if os.path.exists(r'nmap\error.txt'):                        
    os.remove(r'nmap\error.txt')             
  portlist = '443'
                                         
  try:
    nscan = nmap.PortScanner()
    result = nscan.scan(ip, str(portlist))
    # pprint.pprint(result)                                         
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
  begin = time.time()                                                        
  glist = []
  iplist = open(r'nmap/iplist.txt','r',encoding='utf-8')  
  for ip in iplist.readlines():                                              
      # q.put(ip)
      t = gevent.spawn(nmap_scan, ip.strip(), Queue())                                 
      t.start()
      glist.append(t) 
  for t in glist:
      t.start()                                                             
  for t in glist:
      t.join()
  stop = time.time()
  runtime = stop - begin
  print('Scan Time：%.1f秒'%runtime )
  iplist.close()
  if os.path.exists(r'nmap\error.txt'):
    dev_email()                                                                

if __name__ == '__main__':
  main()


# if __name__ == '__main__':
#   schedule.every(20).minutes.do(main)
#   while True:
#     schedule.run_pending()

  




