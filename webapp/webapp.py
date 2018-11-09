from steem import Steem
from steem.blockchain import Blockchain
from steem.account import Account
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, TextField, RadioField, SelectField, FileField, IntegerField, DateField
from steembase.exceptions import AccountDoesNotExistsException
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/_alldata/*": {"origins": "*"}})

class Person(object):
    def __init__(self, name, svalue):
        self.name = name
        self.svalue = svalue

nodes = ['https://api.steemit.com',
         'https://rpc.buildteam.io',
         'http://rpc.curiesteem.com/',
         'https://steemd.privex.io',
         'https://rpc.steemviz.com',
         'https://rpc2.steemviz.com',
         'https://gtg.steem.house:8090']

s = Steem(nodes)

@app.route('/invite/@<ref>',methods = ['POST', 'GET'])
def invite(ref):
    if request.method == 'POST':
        guess = request.form["guess"]
        amount = request.form["amount"]
        curr = request.form["curr"]
        return render_template("invite.html", ref=ref, guess=guess, amount=amount, curr=curr)
    else:
        guess = request.args.get('guess')
        amount = request.args.get('amount')
        curr = request.args.get('curr')
        return render_template("invite.html", ref=ref, guess=guess, amount=amount, curr=curr)

@app.route('/account/@<account_id>',methods = ['POST', 'GET']) #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
def find_question(account_id):
    try:
        profil_img = "https://lh3.googleusercontent.com/lDWYSSGIGrsq5UpzqMkl7RmiUBXP_E9M1MHP4Df9hYTWO9IcTh8bHkVNDQI0IBacxmgE"    
        a = s.get_accounts([account_id])
        a = json.loads(a[0]['json_metadata'])
        profil_img = a['profile']['profile_image']
    except:
        pass
    acc = Account(account_id, steemd_instance=s)
    transfers = acc.get_account_history(-1, 1000, 1, filter_by=["transfer"])
    if request.method == 'POST':
        guess = request.form["guess"]
        amount= request.form["amount"]
        curr = request.form["curr"]
        return render_template("accountback.html", transfers=transfers, guess=guess, amount=amount, curr=curr, profil_img=profil_img, account_id=account_id)
    else:
        guess = request.args.get('guess')
        amount = request.args.get('amount')
        curr = request.args.get('curr')
        return render_template("accountback.html", transfers=transfers, guess=guess, amount=amount, curr=curr, profil_img=profil_img, account_id=account_id)
    return render_template("accountback.html", transfers=transfers, profil_img=profil_img, account_id=account_id)

@app.route('/_alldata')
def get_alldata():
    plyerinfo = []
    img = ["0", "/static/img/1d.png", "/static/img/2d.png", "/static/img/3d.png", "/static/img/4d.png", "/static/img/5d.png", "/static/img/6d.png"]
    
    BOT_ACCOUNT = "arhersost"


    acc = Account(BOT_ACCOUNT, steemd_instance=s)
    transfers = acc.get_account_history(-1, 10000, filter_by=["transfer"])

    for trans in transfers:
        prouser = {}
        if trans["to"] != "ariong" and trans["from"] != BOT_ACCOUNT:
            continue
        choice = trans['memo']
        bet, curr = trans['amount'].split(" ")
        try:
            choice = choice + " "
            choice = int(choice[:2])
            
        except:
            pass
        try:
            if int(choice) in range(2,13):
                bchoice = trans["trx_id"][-30:]
                bchoice2 = bchoice[::-1]
                for ii in bchoice:
                    try:
                        ii = int(ii)
                    except:
                        pass
                    if ii in range(1, 7):
                        dice1 = int(ii)
                        break
                for ss in bchoice2:
                    try:
                        ss = int(ss)
                    except:
                        pass
                    if ss in range(1, 7):
                        dice2 = int(ss)
                        break
                result = dice1 + dice2
                if result == choice and dice1 == dice2:
                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "You Win : You Got double dice:")]
                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                    plyerinfo.append(prouser)
                if result == choice+1 or result == choice-1:
                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "Too Close You Can Win, You got +1/-1 Lose: The winner bet is:")]
                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                    plyerinfo.append(prouser)
                if result == choice:
                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "You Win:")]
                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                    plyerinfo.append(prouser)
                else:
                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "You Lose: The winner bet is:")]
                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                    plyerinfo.append(prouser)
                    
        except:
            pass
        
    return jsonify(result=plyerinfo)

@app.route('/fast/@<account_id>',methods = ['POST', 'GET']) #int has been used as a filter that only integer will be passed in the url otherwise it will give a 404 error
def find_account(account_id):
#    plyerinfo = []
#    img = ["0", "/static/img/1d.png", "/static/img/2d.png", "/static/img/3d.png", "/static/img/4d.png", "/static/img/5d.png", "/static/img/6d.png"]
    
#    BOT_ACCOUNT = account_id


#    acc = Account(BOT_ACCOUNT, steemd_instance=s)
#    transfers = acc.get_account_history(-1, 10000, filter_by=["transfer"])

#    for trans in transfers:
#        prouser = {}
#        if trans["to"] != "ariong" and trans["from"] != BOT_ACCOUNT:
#            continue
#        choice = trans['memo']
#        bet, curr = trans['amount'].split(" ")
#        try:
#            choice = choice + " "
#            choice = int(choice[:2])
            
#        except:
#            pass
#        try:
#            if int(choice) in range(2,13):
#                bchoice = trans["trx_id"][-30:]
#                bchoice2 = bchoice[::-1]
#                for ii in bchoice:
#                    try:
#                        ii = int(ii)
#                    except:
#                        pass
#                    if ii in range(1, 7):
#                        dice1 = int(ii)
#                        break
#                for ss in bchoice2:
#                    try:
#                        ss = int(ss)
#                    except:
#                        pass
#                    if ss in range(1, 7):
#                        dice2 = int(ss)
#                        break
#                result = dice1 + dice2
#                if result == choice and dice1 == dice2:
#                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "double")]
#                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
#                    plyerinfo.append(prouser)
#                if result == choice+1 or result == choice-1:
#                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "win1")]
#                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
#                    plyerinfo.append(prouser)
#                if result == choice:
#                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "win")]
#                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
#                    plyerinfo.append(prouser)
#                else:
#                    userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "lose")]
#                    prouser = dict([ (p.name, p.svalue) for p in userinfo ])
#                    plyerinfo.append(prouser)
                    
#        except:
#            pass
    
    
    try:
        profil_img = "https://lh3.googleusercontent.com/lDWYSSGIGrsq5UpzqMkl7RmiUBXP_E9M1MHP4Df9hYTWO9IcTh8bHkVNDQI0IBacxmgE"    
        a = s.get_accounts([account_id])
        a = json.loads(a[0]['json_metadata'])
        profil_img = a['profile']['profile_image']
    except:
        pass
    acc = Account(account_id, steemd_instance=s)
    transfers = acc.get_account_history(-1, 1000, 1, filter_by=["transfer"])
    if request.method == 'POST':
        guess = request.form["guess"]
        amount= request.form["amount"]
        curr = request.form["curr"]
        return render_template("fast.html", account_id=account_id)#, plyerinfo=plyerinfo)
    else:
        guess = request.args.get('guess')
        amount = request.args.get('amount')
        curr = request.args.get('curr')
        return render_template("fast.html", account_id=account_id)#, plyerinfo=plyerinfo)
    return render_template("fast.html", account_id=account_id)#, plyerinfo=plyerinfo)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(AccountDoesNotExistsException)
def handle_bad_request(e):
    return "bad request! Account dosen't exit", 400

@app.route('/about')
def about():
    return '<h1>About page</h1>'

@app.route("/dynamic", subdomain="<username>")
def username_index(username):
    """Dynamic subdomains are also supported
    Try going to user1.your-domain.tld/dynamic"""
    return username + "localhost:5000"

if __name__ == '__main__':
	app.run(host= '0.0.0.0',debug=True)