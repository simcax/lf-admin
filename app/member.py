from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, send_file
)
bp = Blueprint('member', __name__,url_prefix='/member')
from app import accesstokens
from app.auth import login_required

@bp.route('/show/<id>')
@login_required
def member(id):
    ordered = session['orderedMembers']['realMembers']
    return render_template('member.html', member=ordered[id])
    #return ordered[id]
