import os


class Config:
    # 数据库文件路径
    DB_PATH = None

    # JSON 文件路径
    JSON_PATH = None

    # 运维文档路径
    DOCS_PATH = None

    # 分割块的大小：
    CHUNK_SIZE = 50

    # 块的 overlap：
    CHUNK_OVERLAP = 0

    # 智谱 AI 的api_key:
    ZHIPUAI_API_KEY = "32cb1399517a4bc6bf87e5b174f60557.3ApH7q0bCxxFHTqq"

    # API_KEY(通义)
    TONGYI_API_KEY = "sk-4774d23219524d1c86c9b68870e89e7c"

    # 智谱的模型：
    ZHIPUAI_MODEL = "glm-4"

    # 智谱的模型温度
    ZHIPUAI_TEMPERATURE = 0.2

    # 嵌入模型：
    ZHIPUAI_EMBEDDING_MODEL = "embedding-2"

    # 持久化数据库路径：
    CHROMA_DB_PATH = None

    # 最大尝试次数
    MAX_RETRIES = 5
