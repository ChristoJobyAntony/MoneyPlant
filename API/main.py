from sys import argv
from api import init_db
import uvicorn

if __name__ == "__main__":
    if len(argv) != 1 and argv[1] == "init_db" : init_db.run_first_commit()
    uvicorn.run("api.api:app", host="0.0.0.0", port=5003, reload=True)