# -*- codeing = utf-8 -*-
                                                              #路由器发生一个事件，触发一个python脚本


'''
event manager applet interface_shutdown                                                   #这是EEM配置，需要刷在路由器cli上
 event syslog pattern 'interface loopback55,changed state to administratively down'       #匹配事件
 action 1.0 cli command 'en'
 action 2.0 cli command 'guetshell run python /home/guestshell/no_shut_lo55.py'           #运行脚本
'''
#---------------------------------------------------------------------------------#思路升级：路由器触发一个事件，推送给服务器，由服务器判断识别下发对应的脚本
#py代码，guestshell进入路由器的linux系统，py脚本就放里面

from cli import configure  
configure('interface lo55\nno shutdown')



