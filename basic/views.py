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

    # result = {
    #     'statusCode': 200,
    #     'body': result_dict,
    #     'headers': {
    #         'Access-Control-Allow-Origin': '*',
    #     },
    # }
    return HttpResponse(json.dumps(result_dict),
                        content_type=u"text/json-comment-filtered; charset=utf-8")  # return dict


def list(request):
    request_body = json.loads(request.body)  #
    symptom = request_body['action']['params']['symptom']
    age = request_body['action']['params']['age']
    sex = request_body['action']['params']['sex']

    df = pd.read_excel('https://dsc-winter-nlp.s3.ap-northeast-2.amazonaws.com/sisi_vita.xlsx',
                       encoding='CP949', error_bad_lines=False)
    # age 필터링 and sex 필터링
    cond_sex = df['sex'] == sex
    cond_age = df['age'] == age
    filtered_df = df[cond_sex & cond_age]

    filtered_list = filtered_df.values.tolist()

    result_list = []
    for row in filtered_list[:5]:
        row_dict = {
            "title": row[0],
            "description": row[1],
            "link": {
                "web": row[2]
            }
        }
        result_list.append(row_dict)

    result_dict = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {

                        # start
                        "header": {
                            "title": "비타민 추천",
                            # "imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
                        },
                        # title : 상품 이름
                        # description : 상품 가격
                        # link : 상품 페이지
                        "items": result_list,
                    #   "buttons": [
                    #     {
                    #       "label": "구경가기",
                    #       "action": "webLink",
                    #       "webLinkUrl": "https://namu.wiki/w/%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88"
                    #     }
                    #   ]
                }
        }
    ]
    }
    }

    return HttpResponse(json.dumps(result_dict),
                        content_type=u"text/json-comment-filtered; charset=utf-8")  # return dict
