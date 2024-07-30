import discord
import os
import openai
# Read the chat from the file
file = "chat1.txt"
with open(file, "r") as f:
    chat = f.read()

# Set the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the Discord bot token from environment variable
token = os.getenv("DISCORD_BOT_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        try:
            chat += f"{message.author}: {message.content}\n"
            print(f'Message from {message.author}: {message.content}')
            if self.user != message.author:
                if self.user in message.mentions:
                    response = openai.Completion.create(
                        model="gpt-3.5-turbo",
                        prompt=f"{chat}\n{self.user}:",
                        temperature=0.7,
                        max_tokens=150,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    messageToSend = response.choices[0].text.strip()
                    await message.channel.send(messageToSend)
        except Exception as e:
            print(e)
            chat = ""

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
