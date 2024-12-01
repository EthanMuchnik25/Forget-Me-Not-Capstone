from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Initialize the first LLM
chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "I need you to identify the object that is being looked for and only provide that word",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat

a = chain.invoke(
    [
        HumanMessage(
            content="Where is the uhh red race car uhh "
        )
    ]
)

print(a.content)
