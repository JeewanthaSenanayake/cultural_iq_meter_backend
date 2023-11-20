from fastapi import APIRouter, HTTPException, UploadFile, Query
from fastapi.responses import JSONResponse

import services.user.user as userAuth

user_router = APIRouter(prefix="/iq_meter/api/v1/users", tags=["Users"])

@user_router.put("/add_user/{user}")
def put_user(user:str):
    if(user == ""):
        raise HTTPException(status_code=404, detail=str('Can not create'))
    else:
        data = userAuth.use_create(user)
        print(user)
        if(data==False):
            raise HTTPException(status_code=500, detail=str('User already exist'))
        # return {"questions": data}
        else:
            content = {"user": data}
            return JSONResponse(content=content, headers={"Content-Type": "application/json; charset=UTF-8"})
        
@user_router.post("/submit_score/{uid}/{score}/{leval}")
def submit_score(uid:str, score:int, leval:int):
    data = userAuth.update_soce(uid=uid,score=score,leval=leval)
    content = {"data": data}
    return JSONResponse(content=content, headers={"Content-Type": "application/json; charset=UTF-8"})
