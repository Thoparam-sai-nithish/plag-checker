from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from script import mainfun

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class ContestData(BaseModel):
    contest: str
    challenge: list[str]
    cutoff: int


@app.post("/getResults")
async def getResults(data: ContestData):
    try:
        print("Data:: ",data)
        url = await mainfun(data.contest, data.challenge, data.cutoff)
        return {"Data": url}
    except Exception as e:  # Catch all exceptions for broad error handling
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request. Please try again later."
        )


@app.get("/")
async def get_form():
    try:
        return FileResponse("static/frontEnd.html")
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested file 'frontEnd.html' was not found."
        )
    except Exception as e:  # Catch other unexpected errors
        print(f"Error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while serving the form. Please try again later."
        )