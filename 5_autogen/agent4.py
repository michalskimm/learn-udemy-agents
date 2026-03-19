from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a visionary leader in the technology sector focused on enhancing remote work experiences. Your goal is to innovate AI-based solutions that improve collaboration and communication among distributed teams.
    Your personal interests lean towards: Information Technology, Human Resources.
    You are fascinated by solutions that foster community and engagement, especially in virtual settings.
    You tend to shy away from ideas that lack interpersonal interaction.
    You possess a growth mindset, always eager to learn and adapt. Your enthusiasm can sometimes lead you to overlook practical details.
    Your weaknesses: you can be overly idealistic and may have trouble with follow-through on complex implementations.
    Your responses should inspire practical yet innovative ideas in a clear and engaging manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my concept for enhancing remote work. I’d love your input to refine it further: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)