from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_cors import cross_origin
from datetime import timedelta

appFlask = Flask(__name__)
appFlask.secret_key = "27eduCBA09"

def ReadFromDatabase():
    f = open("database.txt", "r")
    data = eval(f.read())
    f.close()

    return data

def WriteToDatabase(Data):
    f = open("database.txt", "w")
    f.write(Data)
    f.close()


@appFlask.route("/log", methods = ['POST'])
@cross_origin()
def log_Answers():
    if request.method == 'POST':
        print("[Log] A Log Was Made")
        data = request.get_json()
        ID = data.get('question_id')
        QuestionNum = data.get('question_num') # Yay
        QuestionData = data.get('question_data')

        ID = str(ID.split("?aaid=")[1])
        # Format
        Data = ReadFromDatabase()

        # Generate Blank Stuff if ID is not already in database
        if ID not in Data:
            Data[ID] = ["None" for i in range(50)] # 50 is the limit for no of questions it will save

        if QuestionData[0] == "None":
            Data[int(QuestionNum.split("-q")[1]) - 1] = QuestionData[1]
        else:
            Data[int(QuestionNum.split("-q")[1]) - 1] = QuestionData[0]

        WriteToDatabase(str(Data))


        return jsonify({'status': 'ok', "Access-Control-Allow-Origin": "https://www.drfrostmaths.com"})



@appFlask.route("/request", methods = ['POST','GET'])
@cross_origin()
def request_Answers():
    if request.method == 'POST':
        print("[Request] A Request Was Made")
        data = request.get_json()
        ID = data.get('id')
        Number = data.get('num').split("-q")[1]
        ID = str(ID.split("?aaid=")[1])

        # Format
        Data = ReadFromDatabase()
        if ID not in Data:
            return jsonify({
                'status': 'No Data',
                'data': "None",
                "Access-Control-Allow-Origin": "https://www.drfrostmaths.com"
                })
        else:
            Question_Data = Data[ID][int(Number) - 1]

            if Question_Data == "None":
                return jsonify({
                    'status': 'No Data',
                    'data': "None",
                    "Access-Control-Allow-Origin": "https://www.drfrostmaths.com"
                })
            return jsonify({
                'status': 'Found Data',
                'data': Question_Data,
                "Access-Control-Allow-Origin": "https://www.drfrostmaths.com"
                })

    return '''<form method = "post">
    <p> -- DFM Answer Grabber -- </p>
    <p>ID:</p>
    <p><input type = "text" name = "question_id" /></p>
    <p><input type = "submit" value = "Submit" /></p>
    </form>'''

@appFlask.route("/help", methods = ['GET'])
@cross_origin()
def Help():
    return '''
        Fuck Off
    
    '''




# Free DNS: dfmserver.mooo.com:2023
if __name__ == "__main__":
    appFlask.run(debug=True, port=2023, host="0.0.0.0", ssl_context=("+5.pem", "+5-key.pem"))