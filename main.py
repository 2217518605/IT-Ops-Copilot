import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="一个高并发智能IT运维助手", version="1.0")


class QuestionRequest(BaseModel):
    """ 请求模型  """

    question: str


class AnswerResponse(BaseModel):
    """ 响应模型 """

    answer: str


@app.post("/query", response_model=AnswerResponse)
async def query_question(question_request: QuestionRequest):
    """ 智能问答接口 """
    pass


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
