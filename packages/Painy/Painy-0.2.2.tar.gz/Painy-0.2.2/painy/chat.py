from .git import *
from .enums import *
import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain_core.messages import SystemMessage
from operator import itemgetter
from langchain.memory import ConversationBufferMemory


MODEL_NAME = os.getenv(key="OPENAI_MODEL_NAME", default="gpt-3.5-turbo")


class Model:
    def __init__(self, purpose_prompt: str, model_name: str = MODEL_NAME):
        self.model_name = MODEL_NAME

        self.llm = ChatOpenAI(
            temperature=0.1,
            model_name=self.model_name
        )

        self.memory = ConversationBufferMemory(return_messages=True)
        self.memory.chat_memory.add_message(
            SystemMessage(content=purpose_prompt))

        self.chain = ConversationChain(
            llm=self.llm,
            verbose=False,
            memory=self.memory
        )

    def get_response(self, prompt: str) -> str:
        inputs = {"input": prompt}
        response = self.chain.run(inputs)

        return response
