from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
app=FastAPI()
url="mongodb://127.0.0.1:27017/"
client=MongoClient(url)
db=client["Catalog"]
collection=db["user"]

@app.get("/")
async def get_root():
    message="connected Successfully"
    return JSONResponse(
        status_code=200,
        content={
            "message":message
        }
    )

@app.post("/user")
async def create_user(request:Request):
    user=await request.json()
    try:
        user["phone"]=int(user["phone"])
        now=datetime.utcnow()
        user["created_at"]=now
        result=collection.insert_one(user)
        _id=str(result.inserted_id)
        return JSONResponse(
            status_code=200,
            content={
            "result":"Success",
            "message":f"New user created Successfully {_id}"
        }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
            "result":"Failed",
            "message":f"Exception occured due to {e}"
        }
        )
@app.get("/user")
def get_user(request:Request):
    user_id=request.query_params
    id=user_id["user_id"]
    try:
        result=collection.find_one({"_id":ObjectId(id)})
        if result is not None:
            del result["_id"]
            return JSONResponse(
                status_code=200,
                content={
            "result":"Success",
            "message":"User found",
            "data":jsonable_encoder(result)
            }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "message":"User not found"
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message":"Internal server error"
            }
        )


@app.put("/user/update")
async def update_user(request:Request):
    user_update=await request.json()
    now=datetime.utcnow()
    try:
        _id=user_update["_id"]
        data=user_update
        del data["_id"]
        data["updated_at"]=now
        result=collection.update_one({"_id":ObjectId(_id)},
                                     {"$set":data})
        if result.modified_count==1:
            return JSONResponse(
                status_code=200,
                content={
                    "result":"Success",
                    "message":"User Updated Successfully"
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "message":"User not found"
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message":"Internal server error"
            }
        )


@app.get("/user/list")
def get_list_users():
    try:
        result=collection.find().sort("updated_at",-1)
        user_list=[]
        for user in result:
            del user["_id"]
            user_list.append(jsonable_encoder(user))
        return JSONResponse(
            status_code=200,
            content={
                "result":"success",
                "data":{
                    "user_list":user_list
                }
            }
        )
        
    except Exception as e:
         return JSONResponse(
            status_code=500,
            content={
                "message":f"Internal server error due to {e} "
            }
        )


