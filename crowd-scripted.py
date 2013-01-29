#!/usr/bin/env python

# This is a Splunk scripted auth implementation that delegates
# the users and group lookups to an Atlassian Crowd server.

import crowd
import os, sys, getpass

from commonauth import *

app_url = 'http://my.crowd.server:8095/crowd/'
app_user = 'testapp'
app_pass = 'testpass'

splunk_user_group = 'splunk-users'

# Create the reusable Crowd object
cs = crowd.CrowdServer(app_url, app_user, app_pass)

def userLogin( args ):
    success = cs.auth_user(args[USERNAME], args['password'])
    if success:
        print SUCCESS
    else:
        print FAILED

def getUserInfo( args ):
    un = args[USERNAME]
    groups = cs.get_nested_groups(un)
    if groups:
        print SUCCESS + ' --userInfo=' + un + ';' + un + ';' + un + ';' + ':'.join(groups)
    else:
        print FAILED

def getUsers( args ):
    users = cs.get_nested_group_users(splunk_user_group)
    out = SUCCESS
    for un in users:
        groups = cs.get_nested_groups(un)
        out += ' --userInfo=' + un + ';' + un + ';' + un + ';' + ':'.join(groups)

    print out

def getSearchFilter( args ):
    # Ignore search filters
    if cs.user_exists(args[USERNAME]):
        print SUCCESS
    else:
        print FAILED

if __name__ == "__main__":
    callName = sys.argv[1]
    dictIn = readInputs()

    returnDict = {}
    if callName == "userLogin":
        userLogin( dictIn )
    elif callName == "getUsers":
        getUsers( dictIn )
    elif callName == "getUserInfo":
        getUserInfo( dictIn )
    elif callName == "getSearchFilter":
        getSearchFilter( dictIn )
    else:
        print "ERROR unknown function call: " + callName
