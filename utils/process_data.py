import discord
import json
import uuid
import os


class RoleManager():
    def __init__(self):
        self.name="expired_users.json"
        self.name2="new_users.json"
        with open(self.name) as data_file:
            data = json.load(data_file)
        self.cache_expired=data
        with open(self.name2) as data_file:
            data = json.load(data_file)
        self.cache_new=data

    async def role_assignment(self, user, roles_id):
        roles=user.roles
        for assign_role_id in roles_id:
            assign=True
            for user_role in roles:
                if assign_role_id==user_role.id:
                    assign=False
            if assign:
                role_a = discord.utils.get(user.guild.roles, id=assign_role_id)
                await user.add_roles(role_a)
        if user.id not in self.cache_new:
            self.cache_new.append(user.id)
            self._dump(self.name2)
    async def role_removal(self, user, roles_id):
        roles=user.roles
        for remove_role_id in roles_id:
            for user_role in roles:
                if user_role.id==remove_role_id:
                    role_a = discord.utils.get(user.guild.roles, id=remove_role_id)
                    await user.remove_roles(role_a)
        if user.id not in self.cache_expired:
            self.cache_expired.append(user.id)
            self._dump(self.name)
    async def get_cached_user(self, user, mode):
        if mode=="expired" or mode=="cancelled":
            if user.id in self.cache_expired:
                return False
            return True
        if mode=="active":
            if user.id in self.cache_new:
                return False
            return True
    def _dump(self, name):
        temp = '%s-%s.tmp' % (uuid.uuid4(), name)
        with open(temp, 'w', encoding='utf-8') as tmp:
            if name==self.name:
                json.dump(self.cache_expired.copy(), tmp, ensure_ascii=True, separators=(',', ':'))
            else:
                json.dump(self.cache_new.copy(), tmp, ensure_ascii=True, separators=(',', ':'))

        # atomically move the file
        os.replace(temp, name)
