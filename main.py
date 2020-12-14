import requests

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version, user_id):
        self.token = token
        self.version = version
        self.user_id = user_id
        self.params = {
            'access_token': self.token,
            'v': self.version,
            'user_id': self.user_id,
            'fields': 'domain'
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']
        self.owner_link = 'https://vk.com/' + requests.get(self.url + 'users.get', self.params).json()['response'][0]['domain']

    def get_friends(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        friends_url = self.url + 'friends.get'
        friends_params = {
            'count': 5000,
            'user_id': user_id,
            # 'fields': 'sex'
        }
        res = requests.get(friends_url, params={**self.params, **friends_params})
        return res.json()

    def __repr__(self):
        return f'{self.owner_link}'

    def __and__(self, user_2):
        list_friends_id_user_1 = []
        list_friends_id_user_2 = []
        list_mutual_friends_id = []
        list_mutual_friends_id_linked = []
        user_1 = self
        for one_pers in user_1.get_friends()['response']['items']:
            list_friends_id_user_1.append(one_pers['id'])

        for one_friend in user_2.get_friends()['response']['items']:
            list_friends_id_user_2.append(one_friend['id'])

        if len(list_friends_id_user_2) > len(list_friends_id_user_1):
            for one_id in list_friends_id_user_1:
                if one_id in list_friends_id_user_2:
                    list_mutual_friends_id.append(one_id)
        else:
            for one_idd in list_friends_id_user_2:
                if one_idd in list_friends_id_user_1:
                    list_mutual_friends_id.append(one_idd)

        for one_human in list_mutual_friends_id:
            list_mutual_friends_id_linked.append('https://vk.com/id' + str(one_human))

        return list_mutual_friends_id_linked


vk_client1 = VkUser(token, '5.126', 552934290)
vk_client2 = VkUser(token, '5.126', 45269508)
vk_client3 = VkUser(token, '5.126', 7184782)


# print(vk_client3 & vk_client2)
print(vk_client3)

