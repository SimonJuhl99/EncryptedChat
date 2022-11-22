
class Group:

    def __init__(self, group_id, group_name, messages: list, group_members: list, admin):
        self.group_id = group_id
        self.group_name = group_name
        self.messages = messages
        self.group_members = group_members
        self.admin = admin

    def create_invite(self):
        pass

    def ban_user(self, user_alias):
        pass
