from django.http import HttpResponse
import pandas as pd
import json


def index(request):
    request_body = json.loads(request.body)
    symptom = request_body['action']['params']['symptom']

    df = pd.read_csv('https://dsc-winter-nlp.s3.ap-northeast-2.amazonaws.com/vitamin22.csv', encoding='CP949')
    del df['Unnamed: 2']
    del df['Unnamed: 3']
    df = df.drop(96, 0)
    df = df.drop(97, 0)

    test = symptom
    vit = []
    for i in range(96):
        if (df.symtoms[i] == test):
            vit.append(df.vitamin[i])

    vitamin = ' '.join(vit)

    result_dict = {
        "version": "2.0",
        "data": {
            "menu": vitamin
        }
    }

    result = {
        'statusCode': 200,
        'body': result_dict,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
    }
    return HttpResponse(json.dumps(result),
                        content_type=u"text/json-comment-filtered; charset=utf-8")  # return dict
