from pydantic_settings import BaseSettings


class JarvisSettings(BaseSettings):
    INFERENCE_MODEL_HOST: str = "192.168.1.201"
    INFERENCE_MODEL_PORT: str = "18000"

    EMBEDDING_MODEL_HOST: str = "192.168.1.201"
    EMBEDDING_MODEL_PORT: str = "18001"

    MILVUS_HOST: str = "192.168.1.201"
    MILVUS_PORT: str = "19530"
    MILVUS_USERNAME: str = ""
    MILVUS_PASSWORD: str = ""
    MILVUS_DB: str = ""

    POSTGRES_HOST: str = "192.168.1.201"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "1qaz2wsx"
    POSTGRES_DB: str = "postgres"


settings = JarvisSettings()
print(settings)
