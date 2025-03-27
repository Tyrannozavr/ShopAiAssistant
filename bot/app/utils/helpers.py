class UserInteraction:
    def __init__(self, door_type='', priorities=None, photo='', gpt_answer='', contact='', address=''):
        if priorities is None:
            priorities = []
        self.door_type = door_type
        self.priorities = priorities
        self.photo = photo
        self.gpt_answer = gpt_answer
        self.contact = contact
        self.address = address

    def to_dict(self):
        return {
            'door_type': self.door_type,
            'priorities': self.priorities,
            'photo': self.photo,
            'gpt_answer': self.gpt_answer,
            'contact': self.contact,
            'address': self.address
        }

# Example usage
user_interactions = {}

def store_user_interaction(telegram_id, interaction):
    user_interactions[telegram_id] = interaction.to_dict()

def get_user_interaction(telegram_id):
    return user_interactions.get(telegram_id, None)

