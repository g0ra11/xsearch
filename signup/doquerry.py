from .mongomagic import MongoClient
import hashlib
import random
import string

mc = MongoClient()
cc = MongoClient(col='cookies')
rq = MongoClient(col='requests')


def loguser_out(uname):
    cc.delete({'username': uname})


def block_user(user, block):
    print(block)
    mc.update({'username': user}, {'$set': {'is_blk': block}})
    loguser_out(user)


def is_user_blocked(user):
    data = mc.find({'username': user})
    if 'is_blk' in data and data['is_blk'] == 1:
        return 1
    return 0


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def random_string(sz=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(sz))


def register(data):

    if data['password'] != data['rep_pass']:
        return 1

    user_res = mc.find({'username': data['username']})
    if len(user_res) > 0:
        return 2

    user_res = rq.find({'username': data['username']})
    if len(user_res) > 0:
        return 2

    user_res = mc.find({'email': data['email']})
    if len(user_res) > 0:
        return 3

    hash_pass = hash_password(data['password'])
    doc = {
        'username': data['username'],
        'password': hash_pass,
        'email'   : data['email'],
        'is_adm'  : False,
        'search_hist': [],
    }

    try:
        rq.insert(doc)
    except:
        return 4

    return 0


def login(request, data):
    user_res = mc.find({'username': data['username']})

    if len(user_res) == 0:
        return 5

    hash_pass = hash_password(data['password'])
    if hash_pass != user_res[0]['password']:
        return 6

    if 'is_blk' in user_res[0] and user_res[0]['is_blk'] == 1:
        return 33

    cc.delete({'username': data['username']})
    cookie = random_string(20)
    cc.insert({'username': data['username'], 'cookie': cookie})
    request.session['cookie'] = cookie
    return 0


def isvalid(request):
    try:
        cookie = request.session['cookie']
    except KeyError:
        return 0

    user_cookie = cc.find({'cookie': cookie})
    if len(user_cookie) == 0:
        return 0

    res = mc.find({'username': user_cookie[0]['username']})
    if len(res) == 0:
        request.session.flush()
        cc.delete({'username': user_cookie[0]['username']})
        return 0

    return {'user': res[0]['username'], 'email': res[0]['email'], 'hist': res[0]['search_hist']}


def logout(request):
    try:
        cookie = request.session['cookie']
    except KeyError:
        return True

    request.session.flush()
    cc.delete({'cookie': cookie})
    return True


def update_search(request, querry):
    try:
        cookie = request.session['cookie']
    except KeyError:
        return 0

    user_cookie = cc.find({'cookie': cookie})
    if len(user_cookie) == 0:
        return 0

    res = mc.find({'username': user_cookie[0]['username']})
    if len(res) == 0:
        request.session.flush()
        cc.delete({'username': user_cookie[0]['username']})
        return 0

    data = res[0]
    data['search_hist'].append(querry)
    mc.update({'username': data['username']}, {'$set' :{'search_hist': data['search_hist']}})


def is_admin(request):
    try:
        cookie = request.session['cookie']
    except KeyError:
        return 0

    user_cookie = cc.find({'cookie': cookie})
    if len(user_cookie) == 0:
        return 0

    res = mc.find({'username': user_cookie[0]['username']})
    if len(res) == 0:
        request.session.flush()
        cc.delete({'username': user_cookie[0]['username']})
        return 0

    data = res[0]
    if not data['is_adm']:
        return 0

    if 'is_blk' in data and data['is_blk'] == 1:
        return 0

    return data['username']


def get_requests():
    return list(rq.find({}))


def get_users():
    return list(mc.find({}))


def delete_user(user):
    data = mc.find({'username': user})[0]
    if data['is_adm']:
        return 21

    mc.delete({'username': user})


def handle_req(username, approve):
    if approve == 0:
        rq.delete({'username': username})
        return 0

    user_res = rq.find({'username': username})
    if len(user_res) == 0:

        return 20

    exits = mc.find({'username': username})
    if len(exits) > 0:
        return 21

    mc.insert(user_res[0])
    rq.delete({'username': username})
    return 0
