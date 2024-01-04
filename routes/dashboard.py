from fastapi import APIRouter, HTTPException, UploadFile, Query
from fastapi.responses import JSONResponse

import services.dashboard.dashboard  as dashboard


dashboard_router = APIRouter(prefix="/iq_meter/api/v1/dashboard", tags=["Dashboard"])


@dashboard_router.get("/get_ranks")
def get_ranks():
    data = dashboard.get_all_rankings()
    if(data==False):
            raise HTTPException(status_code=500, detail=str('User already exist'))
    else:
        content = {"ranks": data}
        return JSONResponse(content=content, headers={"Content-Type": "application/json; charset=UTF-8"})
