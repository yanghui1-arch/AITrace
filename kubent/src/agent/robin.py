from react import ReActAgent

class Robin(ReActAgent):
    """Robin is the second ReAct agent in kubent system. He is good at analyzing a project motivation.
    In some ways we don't know who is the project's target client and what the project's real target.
    Sometimes we chat with Kubent system to get improvement suggestions. Robin will keep judging whether
    other agents, who are in the whole process of Kubent, understand our project's target and ensure all
    chats are in the right way.
    Robin tasks:
    1. Identify a project's target client, motivation and user's desired effect.
    2. Understand whether other agents fully understand what the project is doing now.
    3. Correct misunderstandings of agents who doesn't understand what the project is actually doing. 
    """
    name: str = "Robin"

    def act(self,):
        ...
    