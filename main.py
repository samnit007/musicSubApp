from pprint import pprint
from flask import Flask, render_template, request, redirect, session, url_for
import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'samsin'


def query_login(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('login')

    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response['Items']


def get_email(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('login')

    try:
        response = table.get_item(Key={'email': email})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def get_subscribe(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('subscribe_music')

    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )

    subscribed_data = []
    for data in response['Items']:
        subscribed_data.append(data)
    # print(f'response form query music, {response}')
    return subscribed_data


def add_user(email, username, password, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('login')

    try:
        response = table.put_item(Item={
            'email': email,
            'user_name': username,
            'password': password,
        })
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return None


def query_music(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('music')

    response = table.scan()
    music_listings = []
    for music in response['Items']:
        music_listings.append(music)
    # print(f'response form query music, {response}')
    return music_listings


def query_form_data(q_title, q_year, q_artist, data_frame):
    print(f'title: {q_title}')
    print(f'q_year: {q_year}')
    print(f'q_artist: {q_artist}')
    row = pd.DataFrame()
    if q_title != "" and q_artist != "" and q_year != "":
        print(
            f"from 1st: \n {data_frame.loc[(data_frame['title'] == q_title) & (data_frame['artist'] == q_artist) & (data_frame['year'] == q_year)]}")
        row = data_frame.loc[(data_frame['title'] == q_title) &
                             (data_frame['artist'] == q_artist) & (data_frame['year'] == q_year)]

    elif q_title != "" and q_artist != "":
        print(
            f"from 2nd: \n {data_frame.loc[(data_frame['title'] == q_title) & (data_frame['artist'] == q_artist)]}")
        row = data_frame.loc[(data_frame['title'] ==
                              q_title) & (data_frame['artist'] == q_artist)]

    elif q_title != "" and q_year != "":
        print(
            f"from 3rd: \n {data_frame.loc[(data_frame['title'] == q_title) & (data_frame['year'] == q_year)]}")
        row = data_frame.loc[(data_frame['title'] ==
                              q_title) & (data_frame['year'] == q_year)]

    elif q_artist != "" and q_year != "":
        print(
            f"from 4th: \n {data_frame.loc[(data_frame['artist'] == q_artist) & (data_frame['year'] == q_year)]}")
        row = data_frame.loc[(data_frame['artist'] == q_artist)
                             & (data_frame['year'] == q_year)]

    elif q_title != "":
        print(
            f"from 5th: \n {data_frame.loc[data_frame['title'] == q_title]}")
        row = data_frame.loc[data_frame['title'] == q_title]

    elif q_artist != "":
        print(
            f"from 6th: \n {data_frame.loc[data_frame['artist'] == q_artist]}")
        return data_frame.loc[data_frame['artist'] == q_artist]

    elif q_year != "":
        print(f"from 7th: \n {data_frame.loc[data_frame['year'] == q_year]}")
        row = data_frame.loc[data_frame['year'] == q_year]

    return row


@ app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ""
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['psw']
        # print('working fetch input name')
        session['user'] = request.form['email']

        try:

            db_email = get_email(input_email)

            for i in query_login(input_email):
                user_name = i['user_name']
                user_password = i['password']
                session['user_name'] = i['user_name']

                if (input_password == user_password):

                    msg = 'Logged in successfully !'

                    # print('before mredirect')
                    # return render_template('main.html', user_name=user_name)

                    # return redirect("/main")

                    return redirect(url_for('mainPage', USER=user_name))

                else:
                    print('else worng pass')
                    msg = 'Email/Password wrong!'
                    return render_template('login.html', msg=msg)
            # if db_psw:
            # pprint(f' { query_music(email)}')
            # pprint(f'lode tappe: {email}', sort_dicts=False)
            # except:
            #     # print("Except Satisfied")
            #     msg = 'Email/Password wrong! new'
            #     return render_template('login.html', msg=msg)

            # msg = f'Logged in successfully !, {input_email}'
        except:
            msg = 'Not found'
            return render_template('login.html', msg = msg)

    else:
        # print("Else Satisfied")
        return render_template('login.html')


@ app.route('/')
def index():
    # if session['user']:
    # return render_template('main.html')
    # else:
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        new_email = request.form['email']
        new_username = request.form['usrnm']
        new_password = request.form['psw']

        try:
            verify_email = get_email(new_email)
            # print(verify_email)
            if verify_email:
                # print('email exist')
                msg = 'The email already exists !'
                return render_template('register.html', msg=msg)
            else:
                # print('email is unique')

                msg = 'Registration Successful'
                return render_template('login.html', msg=msg)
                # return redirect(url_for('login'), msg=msg)
        except:
            # print('Except satisfiesd')
            add_user(new_email, new_username, new_password)
            msg = 'Registration Successful. You can Login !'
            return render_template('login.html', msg=msg)
            # return redirect('/login')

    else:
        # print('Did Not Entered If 1')
        msg = 'Please fill out the form !'
        return render_template('register.html', msg=msg)


@ app.route('/main', methods=['GET', 'POST'])
def mainPage():
    msg = ''
    USER = session['user_name']
    user_email = session['user']
    print(USER)

    sub_data = get_subscribe(user_email)
    print('see the data of subscription here')
    print(sub_data)

    row_result = pd.DataFrame()
    if request.method == 'POST':
        q_title = request.form['ttl']
        q_year = request.form['year']
        q_artist = request.form['artist']

        db_music_listings = query_music()
        data_frame = pd.DataFrame(db_music_listings)

        for i in data_frame.index:
            image_name = data_frame['img_url'][i].split('/')[-1]
            s3_image_url = f'https://s3musicbucket.s3.amazonaws.com/{image_name}'
            data_frame['s3_url'] = s3_image_url
        print(data_frame.head())
        row_result = query_form_data(q_title, q_year, q_artist, data_frame)
        print(type(row_result))
        print(row_result)
        msg = 'Is this what you looking for ? If not please enter another query'
        return render_template('main.html', USER=USER, music_data=row_result, sub_data=sub_data, msg=msg)

    # else:
    #     print("Else satisfied")

    return render_template('main.html', USER=USER, music_data=row_result, sub_data=sub_data)


@ app.route('/get_subscribe_data/<jsdata>')
def get_javascript_data(jsdata):
    print(jsdata)
    return jsdata


@ app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
