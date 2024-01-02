import argparse

import uvicorn
from fastapi import FastAPI
from langserve import add_routes

# from fastapi.responses import JSONResponse

# from jarvis.api.conversation import router as conversation_router
# from jarvis.exceptions.api_exceptions import JarvisInternalException, JarvisNotFoundException
# from jarvis.api.knowledge import router as knowledge_router
# from jarvis.api.memory import router as memory_router
# from jarvis.api.tool import router as tool_router
from jarvis.conversation import ConversationInput, ConversationOutput, conversation
# conv = RunnableLambda(lambda x:generate_prompt(character_id=x["character_id"], memory_id=x["memory_id"]))

app = FastAPI(
    title="Jarvis Sever",
    version="0.2.0",
    description=""
)

add_routes(app, conversation.with_types(input_type=ConversationInput, output_type=ConversationOutput), path="/conversation")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-level", type=str, default="info")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)
