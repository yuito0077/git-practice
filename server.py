from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

# Dummy pipeline to simulate processing
class DummyPipeline:
    def process(self, prompt: str):
        return {
            'result_text': f'This is a response to: {prompt}',
            'selected_model': 'dummy-model-v1',
            'cost_yen': 0.0,
            'is_cache_hit': False,
            'record_id': 'rec_12345',
            'duration_sec': 0.5
        }

pipeline = DummyPipeline()

class AskRequest(BaseModel):
    prompt: str
    format: Optional[str] = 'json'

@app.get('/embed')
def get_embed():
    return FileResponse('static/embed.html')

@app.post('/v1/pipeline/process')
def mock_process(req: AskRequest):
    return ask_api(req)

class FeedbackRequest(BaseModel):
    record_id: str
    feedback: str

@app.post('/v1/pipeline/feedback')
def mock_feedback(req: FeedbackRequest):
    return {"status": "ok"}

@app.post('/api/ask')
def ask_api(req: AskRequest):
    res = pipeline.process(prompt=req.prompt)

    if req.format == 'text':
        return PlainTextResponse(res['result_text'])
    else:
        return {
            'answer': res['result_text'],
            'model': res['selected_model'],
            'cost': res['cost_yen'],
            'is_cache_hit': res['is_cache_hit'],
            'record_id': res['record_id'],
            'duration_sec': res['duration_sec']
        }
