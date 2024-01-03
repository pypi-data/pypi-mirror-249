
import io
from io import BytesIO
import cv2
from starlette.responses import StreamingResponse
from piops import version as piops
from piops.analysis import distributions as dist
from piops.analysis.distributions import EventLog
import numpy as np
from json import loads, dumps
from typing import Union
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Body, Form
from fastapi import File, UploadFile
import pandas as pd

app = FastAPI()

def read_log( file ):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file. Check the format and column separator."}
    finally:
        file.file.close()
        df = pd.read_csv( BytesIO( contents ), sep=",")
    return df


@app.get("/")
def read_root():
    return piops.version()

@app.post("/stats")
def stats( format: str | None = None, file: UploadFile = File(...) ): #= '%Y-%m-%d %H:%M:%S.%f'
    print( format )
    log = EventLog ( read_log( file ), format ) 
    return JSONResponse( content = loads( log.summary().to_json( orient = "index" ) ) )
    #return {"message": f"Successfully uploaded {file.filename}"}

@app.post("/interval")
def interval(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        df = pd.read_csv(BytesIO( contents ), sep=",")
                
        log = EventLog ( df ) 

        x = log.intervalStats()
        #y = x.summary(10, plot=False)
        result = x.to_json(orient="index")

        #result = df.to_json(orient="index")
        #print(result)
    return JSONResponse(content = loads( result ))
    #return {"message": f"Successfully uploaded {file.filename}"}

@app.post("/activities")
def activities(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        df = pd.read_csv(BytesIO( contents ))
        x = dist.distActivities ( df )
        result = x.to_json(orient="index")
        #print(result)
    return JSONResponse(content = loads( result ))
    #return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/fit")
def read_root():
    x = dist.distfit()
    x.fit()
    y = x.summary(10, plot=False)
    result = y.to_json(orient="index")
    #parsed = loads(result)
    #z = dumps(parsed, indent=4)  
    #im_png = cv2.imencode(".png", np.array(y.plot()))[1]
    
    #data_encode = np.array(im_png) 
    #byte_encode = data_encode.tobytes() 

    #return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    #print(parsed)
    return JSONResponse(content = loads( result ))
    #return str(z) #{"Message": }


@app.get("/bestfit")
def get_best():
    x = dist.distfit()
    x.fit()
    return x.get_best() #{"Message": }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


