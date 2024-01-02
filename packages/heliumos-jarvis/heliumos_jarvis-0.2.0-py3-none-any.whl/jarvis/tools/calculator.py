import argparse
from typing import Dict, List, Any

import uvicorn
from fastapi import FastAPI
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains import LLMMathChain
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langserve import add_routes
from pydantic.v1 import BaseModel

from jarvis.api import llm
from jarvis.prompts import MATH_PROMPT

class JarvisSimpleMath(LLMMathChain):
    def _evaluate_expression(self, expression: str) -> str:
        try:
            return super()._evaluate_expression(expression)
        except Exception as e:
            return "Answer: I can not answer the question"
        # Remove any leading and trailing brackets from the output

    def _process_llm_result(
            self, llm_output: str, run_manager: CallbackManagerForChainRun
    ) -> Dict[str, str]:
        return super()._process_llm_result(llm_output, run_manager)


llm_math_chain = JarvisSimpleMath.from_llm(llm=llm, prompt=MATH_PROMPT, verbose=True)



class ServiceInput(BaseModel):
    input: str
    memory: List[Dict[str, str]]

class ServiceOutput(BaseModel):
    output: str

def invoke(input: ServiceInput, config: RunnableConfig):
    question = input["input"]
    a = llm_math_chain.invoke(
        input={"question": question},
        config=config)
    print(a)
    return {
        "output": a["answer"]
    }

app = FastAPI(
    title="Jarvis Sever",
    version="0.2.0",
    description=""
)

add_routes(app, RunnableLambda(invoke).with_types(input_type=ServiceInput, output_type=ServiceOutput), path="/math")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8002)
    parser.add_argument("--log-level", type=str, default="info")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)

