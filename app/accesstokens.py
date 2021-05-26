from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.wrappers import response

from app.auth import login_required
from app.db import get_db

bp = Blueprint('accesstokens', __name__,url_prefix='/tokens')
import os
import requests
import json
import datetime

@bp.route('/')
@login_required
def index():
    # Get all members
    _membersCached()
    ordered = session['orderedMembers']
    return render_template('tokens.html', orderedMembers=ordered)

@bp.route('/realmembersnotoken')
def membersNoTokens():
    # Check if member information has been cached in memory, if not retrieve them
    _membersCached()
    ordered = session['orderedMembers']
    return render_template('members.html',orderedMembers=ordered)

@bp.route('/realmemberswithtokens')
def membersWithTokens():
    # Check if member information has been cached in memory, if not retrieve them
    _membersCached()
    ordered = session['orderedMembers']
    return render_template('members.html',orderedMembers=ordered)

def _membersCached():
    if session.get('orderedMembers'):
        print("Members are cached. Not retrieving them again")
    else:
        print("Members were not cached. Retrieving them")
        apiPass = os.environ.get('API_PASSWORD')
        apiUser = os.environ.get('API_USERNAME')
        response = _getMembers(apiUser, apiPass)
        ordered = _orderMembers(response.text)
        session['orderedMembers'] = ordered

    
        

def _getMembers(apiUser, apiPass):
    url = 'https://foreninglet.dk/api/members?version=1'
    try:
        r = requests.get(url,auth=(apiUser, apiPass))
        return r
    except requests.exceptions.RequestException as e:
        raise(SystemExit(e))

def _orderMembers(members):
    membersDict = json.loads(members)
    realMembers = dict()
    realMembersWithTokens = dict()
    realMembersWithoutTokens = dict()
    notRealMembers = dict()
    returnOrdered = dict()
    memberStats = dict()

    for member in membersDict:
        if member['GenuineMember'] == '1':
            realMembers[member['MemberId']] = member
            # Check to see if the accesstokenfield was filled
            if member['MemberField3']:
                realMembersWithTokens[member['MemberId']] = member
            else:
                realMembersWithoutTokens[member['MemberId']] = member
            if member['Gender'] == 'Mand':
                if 'male' in memberStats:
                    memberStats['male'] += 1
                else:
                    memberStats['male'] = 1
            elif member['Gender'] == 'Kvinde':
                if 'female' in memberStats:
                    memberStats['female'] += 1
                else:
                    memberStats['female'] = 1
            else:
                if 'noGender' in memberStats:
                    memberStats['noGender'] += 1
                else:
                    memberStats['noGender'] = 1
            joinDate = datetime.datetime.strptime(member['EnrollmentDate'],'%Y-%m-%d')
            year = joinDate.year
            yearmonth = "{}-{}".format(joinDate.year, joinDate.month)
            if yearmonth in memberStats:
                memberStats[yearmonth] += 1
            else:
                memberStats[yearmonth] = 1
                
        else:
            notRealMembers[member['MemberId']] = member
    print(member)
    print(memberStats)
        
    returnOrdered['realMembersCount'] = len(realMembers)
    returnOrdered['notRealMembersCount'] = len(notRealMembers)
    returnOrdered['realMembers'] = realMembers
    returnOrdered['notRealMembers'] = notRealMembers
    returnOrdered['realMembersWithoutTokens'] = realMembersWithoutTokens
    returnOrdered['realMembersWithTokens'] = realMembersWithTokens
    returnOrdered['memberStats'] = memberStats
    return returnOrdered


        