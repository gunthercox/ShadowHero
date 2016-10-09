from chatterbot import ChatBot
from settings import GITTER
import logging


# Uncomment the following line to enable verbose logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    'ShadowHero',
    gitter_room=GITTER['ROOM'],
    gitter_api_token=GITTER['API_TOKEN'],
    input_adapter='chatterbot.adapters.input.Gitter',
    output_adapter='selective_response.SelectiveGitterResponse',
    logic_adapters=[
        'harassment_logic.AntiHarassmentLogic'
    ],
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    gitter_only_respond_to_mentions=False
)

chatbot.train('chatterbot.corpus.english')

# The following loop will execute each time the user enters input
while True:
    try:
        response = chatbot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
