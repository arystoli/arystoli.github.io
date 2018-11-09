from steem import Steem
from steem.blockchain import Blockchain
from steem.account import Account
s = Steem()

class Person(object):
    def __init__(self, name, svalue):
        self.name = name
        self.svalue = svalue

BOT_ACCOUNT = "arhersost"
acc = Account(BOT_ACCOUNT, steemd_instance=s)

plyerinfo = []
img = ["0", "/static/img/1d.png", "/static/img/2d.png", "/static/img/3d.png", "/static/img/4d.png", "/static/img/5d.png", "/static/img/6d.png"]

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
            if result == choice:
                print("You win F.dice : "+str(dice1)+" S.dice : "+str(dice2)+" Your bet was "+str(choice)+" transfer from : "+str(trans["from"]))
                userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "win")]
                prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                plyerinfo.append(prouser)
            if result == choice+1 or result == choice-1:
                print("Too Close You Can Win, You got +1/-1 Lose : The winner bet is: "+str(result)+" F.dice : "+str(dice1)+" S.dice : "+str(dice2)+" Your bet was "+str(choice)+" transfer from : "+str(trans["from"]))
                userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "win1")]
                prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                plyerinfo.append(prouser)
            else:
                print("You Lose The Winner Bet is: "+str(result)+" F.dice : "+str(dice1)+" S.dice : "+str(dice2)+" Your bet was "+str(choice)+" transfer from : "+str(trans["from"]))
                userinfo = [Person("choice", choice), Person("res", result), Person("d1", img[dice1]), Person("d2", img[dice2]), Person("type", "lose")]
                prouser = dict([ (p.name, p.svalue) for p in userinfo ])
                plyerinfo.append(prouser)
    except:
        pass

print(plyerinfo)
