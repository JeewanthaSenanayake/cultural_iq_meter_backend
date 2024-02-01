import pandas as pd
from io import StringIO, BytesIO
import io
import time

import database.firebase as firebaseCon
from PIL import Image
import random
# import openpyxl
# import numpy as np

async def upload_img_questions_img_ans(question, ans1, ans2, ans3, ans4, correct_ans,leval):
    imgs = [ans1, ans2, ans3, ans4]

    bucket = firebaseCon.get_firestore_img_upload()

    img_url_list=[]

    for x in imgs:
        ts = time.time()
        contents = await x.read()
        print(f"ans/{str(ts)}_{x.filename}")
        blob = bucket.blob(f"ans/{str(ts)}_{x.filename}")
        blob.upload_from_string(contents, content_type=x.content_type)
        blob.make_public()
        img_url_list.append(blob.public_url)
        time.sleep(0.01)

    data = {
        "question":question,
        "ans1":img_url_list[0],
        "ans2":img_url_list[1],
        "ans3":img_url_list[2],
        "ans4":img_url_list[3],
        "correct_ans":correct_ans,
        "img_url":img_url_list,
        "leval":leval
    }

    upload_to_db_img(tag=leval,q=data)
    return {"data": data}




async def upload_img_questions_img_q(file,question, ans1, ans2, ans3, ans4, correct_ans,leval):
    contents = await file.read()
    # img = Image.open(io.BytesIO(contents))
    # img.show()

    bucket = firebaseCon.get_firestore_img_upload()
    ts = time.time()
    # Upload the file to Firebase Storage
    blob = bucket.blob(f"question/{str(ts)}_{file.filename}")
    blob.upload_from_string(contents, content_type=file.content_type)
    blob.make_public()

    data = {
        "question":question,
        "ans1":ans1,
        "ans2":ans2,
        "ans3":ans3,
        "ans4":ans4,
        "correct_ans":correct_ans,
        "img_url":blob.public_url,
        "leval":leval
    }

    upload_to_db_img(tag=leval,q=data)

    return {"data": data}
    




async def upload_all_questions(questions_file):
    
    file_content = await questions_file.read()
    decoded_content = file_content.decode('utf-8')  # Decode the contents if necessary
    df = pd.read_csv(StringIO(decoded_content))
    
    easyDataList=[]
    mediumDataList=[]
    hardDataList=[]

    for index, row in df.iterrows():
        # values from three columns
        question = row['question']
        ans1 = row['ans1']
        ans2 = row['ans2']
        ans3 = row['ans3']
        ans4 = row['ans4']
        correct_ans  = row['correct_ans']
        leval = row['leval']

        if(leval=="easy"):
            easyDataList.append({'question': str(question).strip(), 'ans1': str(ans1).strip(), 'ans2': str(ans2).strip(), 'ans3': str(ans3).strip(), 'ans4': str(ans4).strip(), 'correct_ans':str(correct_ans).strip(), 'leval':str(leval).strip(), "img_url":""})
        elif(leval=="medium"):
            mediumDataList.append({'question': str(question).strip(), 'ans1': str(ans1).strip(), 'ans2': str(ans2).strip(), 'ans3': str(ans3).strip(), 'ans4': str(ans4).strip(), 'correct_ans':str(correct_ans).strip(), 'leval':str(leval).strip(), "img_url":""})
        elif(leval=="hard"):
            hardDataList.append({'question': str(question).strip(), 'ans1': str(ans1).strip(), 'ans2': str(ans2).strip(), 'ans3': str(ans3).strip(), 'ans4': str(ans4).strip(), 'correct_ans':str(correct_ans).strip(), 'leval':str(leval).strip(), "img_url":""})
    upload_to_db(tag="easy",q=easyDataList)
    upload_to_db(tag="medium",q=mediumDataList)
    upload_to_db(tag="hard",q=hardDataList)
    return {"easy":easyDataList, "medium":mediumDataList, "hard":hardDataList}


def upload_to_db(tag,q):
    db = firebaseCon.get_firestore_client()
    doc_ref = db.collection('question').document("word_q")
    doc_ref.update({str(tag):q})


def upload_to_db_img(tag,q):
    db = firebaseCon.get_firestore_client()
    doc_ref = db.collection('question').document("word_q_img")
    try:
        img_question=doc_ref.get().to_dict()
        if(img_question == None):
            doc_ref.set({
                "easy":[q] if tag=="easy" else [],
                "medium":[q] if tag=="medium" else [],
                "hard":[q] if tag=="hard" else [],
                })
        else:
            newData =  img_question[tag]
            newData.append(q)
            doc_ref.update({str(tag):newData})
    except:
        doc_ref.set({
                "easy":[q] if tag=="easy" else [],
                "medium":[q] if tag=="medium" else [],
                "hard":[q] if tag=="hard" else [],
                })
        print("jh")


def get_randum_questions(leval,no_of_q):
    word_q_count = int(no_of_q*0.7)
    img_q_count = no_of_q - word_q_count
    db = firebaseCon.get_firestore_client()
    doc_ref_img = db.collection('question').document("word_q_img")
    doc_ref_word = db.collection('question').document("word_q")
    img_q = doc_ref_img.get().to_dict()[leval]
    word_q = doc_ref_word.get().to_dict()[leval]

    temp_img_q=[]
    temp_word_q =[]

    if(len(img_q)>img_q_count):
        temp_img_q = random.sample(img_q, img_q_count)
    else:
        temp_img_q = img_q

    if(len(word_q)>word_q_count):
        temp_word_q = random.sample(word_q, word_q_count)
    else:
        temp_word_q = word_q
    
    final_questions = temp_word_q + temp_img_q
    random.shuffle(final_questions)

    return final_questions