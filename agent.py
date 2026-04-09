from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from config import base_config


class ServiceAgent:

    def __init__(self):
        self.llm = ChatZhipuAI(
            api_key=base_config.ZHIPUAI_API_KEY,
            model=base_config.ZHIPUAI_MODEL,
            temperature=base_config.ZHIPUAI_TEMPERATURE
        )

        # 嵌入模型
        self.embedding = ZhipuAIEmbeddings(
            api_key=base_config.ZHIPUAI_API_KEY,
            model=base_config.ZHIPUAI_EMBEDDING_MODEL
        )

        self.db = None

    def load_docs(self):
        """加载并分割文档"""

        loader = TextLoader(base_config.DOCS_PATH, encoding="utf-8")
        document = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=base_config.CHUNK_SIZE,
            chunk_overlap=base_config.CHUNK_OVERLAY
        )
        chunks = text_splitter.split_documents(document)
        return chunks

    def embed_and_store(self):
        """ 向量化并保存到磁盘(一次即可) """

        chunks = self.load_docs()
        self.db = Chroma.from_documents(
            chunks,
            self.embedding,
            persist_directory=base_config.CHROMA_DB_PATH
        )
        self.db.persist()

    def load_vector_db(self):
        """ 直接从磁盘加载向量库 """

        self.db = Chroma(
            persist_directory=base_config.CHROMA_DB_PATH,
            embedding_function=self.embedding
        )

    def create_rag_chain(self):
        """创建 RAG 链"""

        if not self.db:
            self.load_vector_db()  # 优先加载已存在的库

        # RAG 提示词
        prompt = ChatPromptTemplate.from_template("""
        请仅根据提供的文档回答运维问题，不要编造信息。
        如果文档里没有答案，就说“文档里无法找到答案，已从网上寻找解决方法”，然后你根据自己的理解回答我的运维问题。
        
        上下文：
        {context}
        
        用户问题：
        {input}
        """)

        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(self.db.as_retriever(), combine_docs_chain)
        return rag_chain
