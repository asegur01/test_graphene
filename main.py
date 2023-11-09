from fastapi import Depends, FastAPI, status, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn

from db.db import engine, get_db
from model import QuerySchema, UserInput
from graphql_local.user_graphql import schema_user
from graphql_local.query import schema
from db.models.sql_models import Base
import orm


app = FastAPI(title='Graphene introduction')
Base.metadata.create_all(engine)


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
async def home():
    return JSONResponse(content={
        'message': "Welcome home"
    })


@app.get(
    path='/query',
    status_code=status.HTTP_200_OK
)
async def query(data: QuerySchema = Body()):
    result = schema.execute(data.query.replace('\n', ' '))
    
    return JSONResponse(
        content={
            "result": result.data
        },
        status_code=status.HTTP_200_OK
    )

@app.post(
    path='/user',
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserInput = Body(),
    db: Session = Depends(get_db)
):
    result = orm.insert_user(user, db)

    return JSONResponse({
        "result": str(result)
    })

@app.get(
    path='/user',
    status_code=status.HTTP_200_OK
)
async def get_users(db: Session = Depends(get_db)):
    result = orm.get_users(db)

    result_list = [str(res) for res in result]

    return JSONResponse(result_list)


@app.get(
    path="/user/query",
    status_code=status.HTTP_200_OK
)
async def get_users_query(
    data: QuerySchema = Body(),
    db: Session = Depends(get_db)
):
    # type's result: 'graphql.execution.base.ExecutionResult'
    result = schema_user.execute(data.query.replace('\n', ' '), context_value={'session': db})
    print(result)
    

    # return result
    return JSONResponse(
        content=result.to_dict(),
        status_code=status.HTTP_200_OK
    )


@app.post(
    path='/user/query',
    status_code=status.HTTP_200_OK
)
async def mutate_user_query(
    data: QuerySchema = Body(),
    db: Session = Depends(get_db)
):
    print(data.query)
    result = schema_user.execute(data.query.replace('\n', ' '), context_value={'session': db})

    return JSONResponse(
        content=result.to_dict(),
        status_code=status.HTTP_200_OK
    )




if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

