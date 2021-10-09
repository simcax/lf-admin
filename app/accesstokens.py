from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, send_file
)
from flask.helpers import make_response
from werkzeug.exceptions import abort
from werkzeug.wrappers import response

from app import app
from app.auth import login_required
from app.db import get_conn
from app.graph import graphPygal

bp = Blueprint('accesstokens', __name__,url_prefix='/tokens')
import os
import requests
import json
import datetime
import socket
from io import BytesIO
hostname = socket.gethostname()

@bp.route('/')
@login_required
def index():
    # Get all members
    _membersCached()
    ordered = session['orderedMembers']
    return render_template('tokens.html', orderedMembers=ordered, hostname=hostname)

@bp.route('/realmembersnotoken')
@login_required
def membersNoTokens():
    # Check if member information has been cached in memory, if not retrieve them
    _membersCached()
    ordered = session['orderedMembers']
    return render_template('members.html',orderedMembers=ordered, hostname=hostname)

@bp.route('/realmemberswithtokens')
@login_required
def membersWithTokens():
    # Check if member information has been cached in memory, if not retrieve them
    _membersCached()
    ordered = session['orderedMembers']
    return render_template('members.html',orderedMembers=ordered, hostname=hostname)


@bp.route('/refreshData')
@login_required
def refreshMemberData():
    _membersCached(True)
    return redirect(url_for('accesstokens.index'))

@bp.route('/testgraph')
def testgraph():
    from app.graph import graphPygal
    _membersCached()
    memberStats = session['orderedMembers']['memberStatsByYear']
    return graphPygal.makeGraphYearByYear("Medlemstilgang", "Antal", "måned for måned", memberStats)

@bp.route('/newMembersGraph')
@login_required
def newMembersGraph():
    from app.graph import graphPygal
    _membersCached()
    memberStats = session['orderedMembers']['memberStatsByYear']
    return graphPygal.makeGraphYearByYear("Medlemstilgang", "Antal", "måned for måned", memberStats)

@bp.route('/memberAgesGraph')
@login_required
def memberAgesGraph():
    _membersCached()
    memberStats = session['orderedMembers']['memberAges']
    app.logger.info(f"Making members age graph with data {memberStats}")
    values, xLabels = [],[]
    for key, value in sorted(memberStats.items()):
        values.append(value)
        xLabels.append(str(key))
    return graphPygal.makeGraph("Medlemsalder","Antal", xLabels,values, "Alder")

@bp.route('/memberAgesGraphFemale')
@login_required
def memberAgesGraphFemale():
    _membersCached()
    memberStats = session['orderedMembers']['memberAgesFemale']
    ages, count = [],[]
    for age, memberCount in sorted(memberStats.items()):
        ages.append(age)
        count.append(memberCount)
    return graphPygal.makeGraph("Aldersfordeling Kvinder","Antal", ages, count, "Alder")
    
@bp.route('/memberAgesGraphMale')
@login_required
def memberAgesGraphMale():
    _membersCached()
    memberStats = session['orderedMembers']['memberAgesMale']
    ages, count = [], []
    for age, memberCount in sorted(memberStats.items()):
        ages.append(age)
        count.append(memberCount)
    return graphPygal.makeGraph("Aldersfordeling Mænd","Antal", ages, count, "Alder")

@bp.route('/resignedMembers')
@login_required
def resignedMembers():
    apiPass = os.environ.get('API_PASSWORD')
    apiUser = os.environ.get('API_USERNAME')
    response = _getResignedMembers(apiUser, apiPass)
    
    return response.text
        



def _membersCached(refresh=False):
    if session.get('orderedMembers') and refresh == False:
        print("Members are cached. Not retrieving them again")
        g.lastDataRetrieval = session.get('lastDataRetrieval')
    else:
        print("Members were not cached. Retrieving them")
        apiPass = os.environ.get('API_PASSWORD')
        apiUser = os.environ.get('API_USERNAME')
        response = _getMembers(apiUser, apiPass)
        ordered = _orderMembers(response.text)
        session['orderedMembers'] = ordered
        rt = datetime.datetime.now()
        session['lastDataRetrieval'] = rt.strftime("%b %d %Y %H:%M")
        g.lastDataRetrieval = session.get('lastDataRetrieval')

def _getResignedMembers(apiUser, apiPass):
    url = 'https://foreninglet.dk/api/members/status/resigned?version=1'
    try:
        r = requests.get(url,auth=(apiUser, apiPass))
        return r
    except requests.exceptions.RequestException as e:
        raise(SystemExit(e))
        

def _getMembers(apiUser, apiPass):
    url = 'https://foreninglet.dk/api/members?version=1'
    try:
        r = requests.get(url,auth=(apiUser, apiPass))
        return r
    except requests.exceptions.RequestException as e:
        raise(SystemExit(e))

def _calculateAge(date):
    birthdate = datetime.datetime.strptime(date, '%Y-%m-%d')
    endDate = datetime.datetime.today()
    timeDifference = endDate - birthdate
    ageDays = timeDifference.days
    ageYears = int(ageDays / 365)
    return ageYears

def _orderMembers(members):
    membersDict = json.loads(members)
    realMembers = dict()
    realMembersWithTokens = dict()
    realMembersWithoutTokens = dict()
    notRealMembers = dict()
    returnOrdered = dict()
    memberStats = dict()
    memberStats2 = dict()
    memberGender = dict()
    memberStatsTexts = dict()
    interestingNumber = dict()
    memberAges = dict()
    memberAgesMale = dict()
    memberAgesFemale = dict()
    today = datetime.date.today()
    first = today.replace(day=1)
    curMonth = first.strftime("%Y%m")
    lastMonth = first - datetime.timedelta(days=1)
    #app.logger.info("Last Month was:{} ".format(lastMonth))
    prevMonth = lastMonth.strftime("%Y%m")
    #app.logger.info("Prev Month was:{} ".format(prevMonth))
    for member in membersDict:
        if member['GenuineMember'] == '1':
            realMembers[member['MemberId']] = member

            # Get Age for the member:
            memberAge = _calculateAge(member['Birthday'])
            # Check to see if the accesstokenfield was filled
            if member['MemberField3']:
                realMembersWithTokens[member['MemberId']] = member
            else:
                realMembersWithoutTokens[member['MemberId']] = member
            if member['Gender'] == 'Mand':
                if 'male' in memberGender:
                    memberGender['male'] += 1
                else:
                    memberGender['male'] = 1
                # Register Ages for Men
                if memberAge in memberAgesMale:
                    memberAgesMale[memberAge] += 1
                else:
                    memberAgesMale[memberAge] = 1
            elif member['Gender'] == 'Kvinde':
                if 'female' in memberGender:
                    memberGender['female'] += 1
                else:
                    memberGender['female'] = 1
                # Register Ages for Women    
                if memberAge in memberAgesFemale:
                    memberAgesFemale[memberAge] += 1
                else:
                    memberAgesFemale[memberAge] = 1
                
            else:
                if 'noGender' in memberGender:
                    memberGender['noGender'] += 1
                else:
                    memberGender['noGender'] = 1

            joinDate = datetime.datetime.strptime(member['EnrollmentDate'],'%Y-%m-%d')
            year = joinDate.year
            joinMonth = "{}".format(joinDate.month)
            yearmonth = "{}{:02d}".format(joinDate.year, joinDate.month)
            memberStatsTexts[yearmonth] = joinDate.strftime("%Y %B")
            
                
            if memberAge in memberAges:
                memberAges[memberAge] += 1
            else:
                memberAges[memberAge] = 1
                
            if yearmonth in memberStats:
                memberStats[yearmonth] += 1
            else:
                memberStats[yearmonth] = 1
            
            if memberStats2.get(year):
                thatYear = memberStats2.get(year)
                if thatYear.get(joinMonth):
                    monthCount = thatYear.get(joinMonth) +1
                    memberStats2[year].update( { joinMonth: monthCount})
                else:
                    memberStats2[year].update({joinMonth: 1})
            else:
                memberStats2[year] = { joinMonth: 1 }
                

                
        else:
            notRealMembers[member['MemberId']] = member
    
    interestingNumber['lastMonthMembers'] = memberStats[prevMonth]
    if curMonth in memberStats:
        interestingNumber['currentMonthMembers'] = memberStats[curMonth]
    else:
        interestingNumber['currentMonthMembers'] = 0
    
    # Re-order membersStats so it's in order of year-month
    tmpMemberStats = dict()
    for key in sorted(memberStats.keys()):
        tmpMemberStats[key] = memberStats[key]
    memberStats = tmpMemberStats
    app.logger.info(member)

    returnOrdered['realMembersCount'] = len(realMembers)
    returnOrdered['notRealMembersCount'] = len(notRealMembers)
    returnOrdered['realMembers'] = realMembers
    returnOrdered['notRealMembers'] = notRealMembers
    returnOrdered['realMembersWithoutTokens'] = realMembersWithoutTokens
    returnOrdered['realMembersWithTokens'] = realMembersWithTokens
    returnOrdered['memberStats'] = memberStats
    returnOrdered['memberStatsByYear'] = memberStats2
    returnOrdered['memberGender'] = memberGender
    returnOrdered['memberStatsTexts'] = memberStatsTexts
    returnOrdered['interestingNumbers'] = interestingNumber
    returnOrdered['memberAges'] = memberAges
    returnOrdered['memberAgesMale'] = memberAgesMale
    returnOrdered['memberAgesFemale'] = memberAgesFemale
    #print(returnOrdered)
    return returnOrdered


        
