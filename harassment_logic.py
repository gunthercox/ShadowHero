from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement

'''
Cases:

# General insults

In the case where a user is issuing general insults towards others

Response: ShadowHero will tell the user to calm down or take it easy.
This action brings awareness to the situation and may help to diffuse it.

# Repeated attacks on a user: Verbally defend the user and flag the abuser's account.

# Direct message the user and ask if they are being attacked.
Use this data to 'learn' about perceptions of harassment.
'''

class AntiHarassmentLogic(LogicAdapter):

    def __init__(self, **kwargs):
        super(AntiHarassmentLogic, self).__init__(kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        confidence = 0
        statement = Statement("")

        return confidence, statement