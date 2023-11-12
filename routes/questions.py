from fastapi import APIRouter, HTTPException, UploadFile, Query
from fastapi.responses import JSONResponse

import services.questions.questions as QuestionsUpload

questions_router = APIRouter(prefix="/iq_meter/api/v1/questions", tags=["Questions"])


@questions_router.post("/uploadfile_with_all_questions/")
async def upload_file_with_all_questions(file: UploadFile):
    if(file.content_type == "text/csv"):
        fileContent = await QuestionsUpload.upload_all_questions(file)
        # print(file.content_type)
        return {"questions": fileContent}
    else:
        raise HTTPException(status_code=400, detail=str('File type error'))
    


@questions_router.post("/uploadfile_with_img_question_img_q/")
async def uploadfile_with_img_question_img_q(file: UploadFile, question: str, ans1: str, ans2: str, ans3: str, ans4: str, correct_ans: str = Query(..., description="Correct ans", enum=["ans1", "ans2", "ans3", "ans4"]), leval: str = Query(..., description="Leval", enum=["easy", "medium", "hard"])):
    if(file.content_type in ["image/png","image/jpeg"]):
        fileContent = await QuestionsUpload.upload_img_questions_img_q(file, question, ans1, ans2, ans3, ans4, correct_ans,leval)
        return {"questions": fileContent}
    else:
        raise HTTPException(status_code=400, detail=str('File type error'))
    


@questions_router.post("/uploadfile_with_img_question_ans_q/")
async def uploadfile_with_img_question_ans_q( question: str, ans1: UploadFile, ans2: UploadFile, ans3: UploadFile, ans4: UploadFile, correct_ans: str = Query(..., description="Correct ans", enum=["ans1", "ans2", "ans3", "ans4"]), leval: str = Query(..., description="Leval", enum=["easy", "medium", "hard"])):
    if("image/jpeg" in [ans1.content_type, ans2.content_type, ans3.content_type, ans4.content_type]):
        fileContent = await QuestionsUpload.upload_img_questions_img_ans(question, ans1, ans2, ans3, ans4, correct_ans,leval)
        return {"questions": fileContent}
    else:
        raise HTTPException(status_code=400, detail=str('File type error'))
    

@questions_router.get("/get_questions/{leval}/{no_of_q}")
def get_questions(leval:int, no_of_q:int):
    if(leval == 1):
        data =  QuestionsUpload.get_randum_questions(leval="easy",no_of_q=no_of_q)
        return {"questions": data}
    elif(leval == 2):
        data =  QuestionsUpload.get_randum_questions(leval="medium",no_of_q=no_of_q)
        # return {"questions": data}
        content = {"questions": data}
        return JSONResponse(content=content, charset="UTF-8")
    elif(leval == 3):
        data =  QuestionsUpload.get_randum_questions(leval="hard",no_of_q=no_of_q)
        return {"questions": data}
    else:
        raise HTTPException(status_code=404, detail=str('Level not found'))
    
    
    
    