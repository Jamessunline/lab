#coding=utf-8
import difflib,time,paramiko,datetime,smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

f = open('ip_list.txt')

for line in f.readlines():
    ip = line.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username='python',password='123',look_for_keys=False)
    print ("你已成功登陆交换机： ", ip)
    command = ssh_client.invoke_shell()
    command.send('term len 0\n')
    command.send('show run\n')
    time.sleep(3)
    output = command.recv(65535).decode("ascii")

    with open(ip + '_' + datetime.date.today().isoformat(), 'w+') as new_file, open(ip + '_' + (datetime.date.today() - datetime.timedelta(days=1)).isoformat()) as old_file:
        new_file.write(output)
        new_file.close()
        new_file = open(ip + '_' + datetime.date.today().isoformat())
        diff = list(difflib.ndiff(old_file.readlines(), new_file.readlines()))

    with open(ip + '_' + datetime.date.today().isoformat() + '_report', 'w') as report_file:
        for index, line in enumerate(diff):                                                                 #组合为一个索引键序列，数据的循环
            if line.startswith('- ') and diff[index + 1].startswith(('?', '+')) == False:
                report_file.write('\n已被移除的旧配置： ' + '\n' + line + '\n')
            elif line.startswith('+ ') and diff[index + 1].startswith('?') == False:
                report_file.write('\n已被添加的新配置： ' + '\n' + diff[index - 2] + diff[index - 1] + line  + '\n')
            elif line.startswith('- ') and diff[index + 1].startswith('?') and diff[index + 2].startswith('+ ') and diff[index + 3].startswith('?'):
                report_file.write('\n已被修改的配置（长度不变或变短）: \n\n' + line + diff[index + 1] + diff[index + 2] + diff[index + 3] + '\n')
            elif line.startswith('- ') and diff[index + 1].startswith('+') and diff[index + 2].startswith('? '):
                report_file.write('\n已被修改的配置（长度变长）: \n\n' + line + diff[index + 1] + diff[index + 2] + '\n')
            else:

    with open(ip + '_' + datetime.date.today().isoformat() + '_report') as report_file, open('master_report_' + datetime.date.today().isoformat(), 'a') as master_report:
        if len(report_file.readlines()) < 1:
            master_report.write('\n交换机: ' + ip + '\n')
            master_report.write('\n' + '于' + datetime.date.today().isoformat() + ' 没有发现任何配置变化\n')        
        else:
            report_file.seek(0)
            master_report.write('\n交换机: ' + ip + ' 发现以下配置变化\n')
            master_report.write(report_file.read())

fromaddr = 'contumacysg@gmail.com'
toaddr = 'contumacysg@gmail.com'
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = '网络配置管理日表：' +  datetime.date.today().isoformat()
with open('master_report_' + datetime.date.today().isoformat()) as master_report:
    master_report.seek(0)
    body = master_report.read() + '\n报告生成日期和时间: ' + datetime.datetime.now().isoformat()
    msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login('username', 'password')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)