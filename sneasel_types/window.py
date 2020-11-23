from typing import Dict


class Window:
    def __init__(self, message_id: int, unique_roles: bool, emoji_to_role_dict: Dict[str, str]):
        self.message_id = message_id
        self.unique_roles = unique_roles
        self.emoji_to_role_dict = emoji_to_role_dict
