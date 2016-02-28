#!/usr/bin/python
# -*- coding:utf-8 -*-
import xml.etree.ElementTree as etree
import sys
import os
import csv
reload(sys)
sys.setdefaultencoding('utf8')

writer=csv.writer(file('ci_list.csv','a'))
#writer.writerow([projectname.strip('\n'),description,assignedNode,command,upstreamproject,timertrigger,gitproject,maillist,])
writer.writerow(['项目','描述','从机','命令','上级任务','任务cron','GIT','收件人'])
f = open(sys.argv[1])
for line in f.readlines():
 try :
  tree = etree.parse('jobs/'+line.strip('\n')+'/config.xml')
 except Exception,e:
  pass
  continue 
 root = tree.getroot() 
 """
 for child in root :
     print child
     print child.tag
     print child.text
 """
 projectname = line
 try :
  description = root.find('description').text
 except Exception,e:
  description = ''
 try :
   assignedNode = root.find('assignedNode').text
 except Exception,e:
   assignedNode = ''
 try :
  command = root.findall('builders/hudson.tasks.Shell/command')[0].text
 except Exception,e:
  command = ''
  pass
 try :
  upstreamproject = root.findall('triggers/jenkins.triggers.ReverseBuildTrigger/upstreamProjects')[0].text
 except Exception,e:
  upstreamproject = ''
  pass
 try :
     timertrigger = root.findall('triggers/hudson.triggers.TimerTrigger/spec')[0].text
 except Exception,e:
     timertrigger = ''
     pass
 try :
      gitproject = root.findall('properties/com.coravy.hudson.plugins.github.GithubProjectProperty/projectUrl')[0].text
 except Exception,e:
      gitproject = ''
      pass
 try :
      maillist = root.findall('publishers/hudson.tasks.Mailer/recipients')[0].text
 except Exception,e:
      maillist = ''
      pass
 writer.writerow([projectname.strip('\n'),description,assignedNode,command,upstreamproject,timertrigger,gitproject,maillist,])
