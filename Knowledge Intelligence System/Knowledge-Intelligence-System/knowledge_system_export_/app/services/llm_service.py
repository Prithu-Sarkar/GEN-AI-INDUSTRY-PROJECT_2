"""LLM service with Groq backend."""

import time

from typing import (
    Dict,
    Any
)

from langchain_groq import (
    ChatGroq
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.runnables import (
    RunnablePassthrough
)

from langchain_core.output_parsers import (
    StrOutputParser
)


class LLMService:

    _SYS = (
        "You are a precise knowledge assistant. "
        "Answer ONLY from the provided context. "
        "If context is insufficient, "
        "say so clearly."
    )

    def __init__(self, vs, config):

        self.vs = vs

        self.cfg = config

        self.llm = ChatGroq(

            model=config.model_name,

            api_key=config.groq_api_key,

            temperature=config.temperature,

            max_tokens=config.max_tokens
        )

        self._build_chain()


    def _build_chain(self):

        prompt = (
            ChatPromptTemplate.from_messages([
                ("system", self._SYS),

                (
                    "user",
                    "Context:\n{context}"
                    "\n\nQuestion:"
                    "\n{question}"
                )
            ])
        )

        self._chain = (
            {
                "context":
                self.vs.as_retriever(),

                "question":
                RunnablePassthrough()
            }

            | prompt

            | self.llm

            | StrOutputParser()
        )


    def ask(
        self,
        question: str
    ) -> Dict[str, Any]:

        t0 = time.perf_counter()

        try:

            answer = self._chain.invoke(
                question
            )

            return {

                "answer": answer,

                "model":
                self.cfg.model_name,

                "duration_s":
                round(
                    time.perf_counter() - t0,
                    3
                )
            }

        except Exception as e:

            return {

                "answer":
                f"Error: {e}",

                "error": True,

                "duration_s":
                round(
                    time.perf_counter() - t0,
                    3
                )
            }