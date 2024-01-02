"""Wrapper around Xinference embedding models."""
from typing import Any, List, Optional, Dict
import requests
from langchain_core.embeddings import Embeddings
from pydantic import Field, BaseModel


class JarvisOpenAIEmbeddings(BaseModel, Embeddings):
    model: str = "text-embedding-ada-002"
    openai_api_base: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)
    default_headers: Optional[Dict[str, Any]] = {}

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using Xinference.
        Args:
            texts: The list of texts to embed.
        Returns:
            List of embeddings, one for each text.
        """
        request_datas = {
            "input": texts,
            "model": self.model
        }
        response = requests.post(f"{self.openai_api_base}/embeddings", json=request_datas, headers=self.default_headers)
        response_json = response.json()
        ret = [d["embedding"] for d in response_json["data"]]
        # print(ret)
        return ret

    def embed_query(self, text: str) -> List[float]:
        """Embed a query of documents using Xinference.
        Args:
            text: The text to embed.
        Returns:
            Embeddings for the text.
        """
        request_datas = {
            "input": text,
            "model": self.model
        }
        # print(self.openai_api_base)
        response = requests.post(f"{self.openai_api_base}/embeddings", json=request_datas, headers=self.default_headers)
        response_json = response.json()
        ret = response_json["data"][0]["embedding"]
        # print(ret)
        return ret
