from langchain_core.messages import SystemMessage, HumanMessage

def detect_intent(llm, user_message: str) -> str:
    messages = [
        SystemMessage(
            content="Classify intent as either booking or general. Return only one word."
        ),
        HumanMessage(content=user_message)
    ]
    response = llm.invoke(messages).content.lower().strip()
    return "booking" if "booking" in response else "general"
