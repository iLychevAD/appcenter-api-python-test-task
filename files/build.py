#!/usr/bin/env python3
import os
import datetime
import copy
from time import sleep

from dateutil.parser import parse

import appcenter

BUILD_WAIT_INTERVAL = 5

owner_name = os.environ.get('APPCENTER_OWNER')
app_name = os.environ.get('APPCENTER_APP')
access_token = os.environ.get('APPCENTER_TOKEN')
if ( not owner_name or
     not app_name or
     not access_token ):
    print('''
    Help:
    
    set env variables APPCENTER_OWNER APPCENTER_APP APPCENTER_TOKEN
    
    ''')
    exit(0)

appcenter = appcenter.AppCenterClient(owner_name=owner_name, 
            app_name=app_name, access_token=access_token)

branch_list = []
[branch_list.append(b.branch) for b in appcenter.branches.all()]

print('\nBranches:')
[print(b.name) for b in branch_list]

print('\nStarting builds:')
for i in range(len(branch_list[:])):
    #if not 'master' in branch_list[i].name: continue
    build = appcenter.branches.build(branch_name=branch_list[i].name, 
            commit=branch_list[i].commit.sha)
    branch_list[i].build = build
    print(f'started build id {branch_list[i].build.id}, № {build.buildNumber} '
          f'for branch {branch_list[i].name}')

print('\nWaiting all builds finish')
all_builds_completed = False
while True:
    sleep(BUILD_WAIT_INTERVAL)
    if all_builds_completed: 
        break
    all_builds_completed = True
    for i in range(len(branch_list)):
        #if not 'master' in branch_list[i].name: continue
        build_info = appcenter.branches.build_info(branch_list[i].build.id)
        if not 'completed' in build_info.status: 
            all_builds_completed = False
            print(f'Build {branch_list[i].build.id} '
                  f'still in progress... ({build_info.status})')

print('\nCompleted:')
print('\nBRANCH | STATUS | DURATION | LOG URL\n')
for i in range(len(branch_list)):
    #if not 'master' in branch_list[i].name: continue
    build_info = appcenter.branches.build_info(branch_list[i].build.id)
    log_link = appcenter.branches.build_log_link(branch_list[i].build.id)
    start = parse(build_info.startTime)
    finish = parse(build_info.finishTime)
    duration = finish - start
    duration = str(duration).split('.')[0]
    print(f'{branch_list[i].name} | {build_info.result} | {duration} | {log_link}\n')



