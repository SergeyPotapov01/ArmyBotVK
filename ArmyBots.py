import os

from random import choice

import DataBase

import vk_api

from vk_api.utils import get_random_id


class ArmyBots:
    def __init__(self):
        dataBase = DataBase.DataBase()
        self.tokens = []
        self.complimentToGirl = []
        self.insultToMen = []
        self._action = [
            'Отправить сообщение',
            'Поставить лайк на фото',
            'Поставить лайк на пост',
            'Поставить лайк на коментарий',
            'Отправить комплименты',
            'Отправить оскорбления (фем)',
        ]

        with open('compliment_to_girl.txt', 'r', encoding='UTF-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                self.complimentToGirl.append(line)

        with open('insult_to_men.txt', 'r', encoding='UTF-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                self.insultToMen.append(line)

        for access_token in dataBase.tokens:
            if access_token == 0:
                continue
            vk = access_token
            self.tokens.append(vk)

    def _clearTerminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _getALotOfCompliment(self, i):
        part_1 = [
            'Ванилька, ', 'Солнышко, ', 'Любимая, ', 'Зайка, ', 'Бабочка, ',
            'Милашка, ', 'Маленькая леди, ', 'Милая, ', 'Вишенка, ', 'Принцесса, ',
            'Куколка, ', 'Единственная, ', 'Львенок, ', 'Рыбка, ', 'Львица, '
            ]

        part_2 = [
            'ты очень Красивая! ', 'ты классная! ', 'ты лучшая! ', 'ты самая умная! ',
            'ты умница! ', 'ты сексуальная! ', 'ты моя вторая половинка! ', 'ты нежная! ',
            'ты любовь всей моей жизни! ', 'ты красавица! ', 'ты прекрасная! ', 'ты Милая! ',
            ]

        message = ''
        for j in range(25):
            message += str(i + j) + ' - ' + choice(part_1) + choice(part_2) + choice(self.complimentToGirl) + ' Я люблю тебя!\n'

        return message

    def sendMessages(self, id_user: int, message: str):
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token).get_api()
                vk.messages.send(user_id=id_user, message=message, random_id=get_random_id())
            except:
                print(token)

    def likePost(self, id_user: int, id_item: int):
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token).get_api()
                vk.likes.add(type='post', owner_id=id_user, item_id=id_item)
            except:
                print(token)

    def likePhoto(self, id_user: int, id_item: int):
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token).get_api()
                vk.likes.add(type='photo', owner_id=id_user, item_id=id_item)
            except:
                print(token)

    def likeComment(self, id_user: int, id_item: int):
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token).get_api()
                vk.likes.add(type='comment', owner_id=id_user, item_id=id_item)
            except:
                print(token)

    def sendCompliment(self, id_user):
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token).get_api()
                vk.messages.send(user_id=id_user, message=choice(self.complimentToGirl), random_id=get_random_id())
            except:
                print(token)

    def sendinsult(self, id_user):
        for token in self.tokens:
            try:
                vk = vk_api.VkApi(token=token).get_api()
                vk.messages.send(user_id=id_user, message=choice(self.insultToMen), random_id=get_random_id())
            except:
                print(token)

    def sendALotOfCompliments(self, id_user):
        for token in self.tokens:
            for i in range(1, 1001, 25):
                try:
                    vk = vk_api.VkApi(token=token).get_api()
                    vk.messages.send(user_id=id_user, message=self._getALotOfCompliment(i), random_id=get_random_id())
                except:
                    print('Капча')


    def gui(self):
        while True:
            self._clearTerminal()
            for i in range(len(self._action)):
                print(i, self._action[i], sep=' - ')
            x = input('Выберите действие')
            if x == '0':
                id_user = input('Введите id аользователя: ')
                message = input('Введите текст сообщения: ')
                self.sendMessages(id_user, message)
            elif x == '1':
                id_user = input('Введите id пользователя/группы: ')
                id_item = input('Введите id элемента: ')
                self.likePhoto(id_user, id_item)
            elif x == '2':
                id_user = input('Введите id пользователя/группы: ')
                id_item = input('Введите id элемента: ')
                self.likePhoto(id_user, id_item)
            elif x == '3':
                id_user = input('Введите id пользователя/группы: ')
                id_item = input('Введите id элемента: ')
                self.likeComment(id_user, id_item)
            elif x == '4':
                id_user = input('Введите id аользователя: ')
                self.sendCompliment(id_user)
            elif x == '5':
                id_user = input('Введите id аользователя: ')
                self.sendinsult(id_user)
            elif x == '6':
                id_user = input('Введите id аользователя: ')
                self.sendALotOfCompliments(id_user)
            else:
                print('Введена неверная команда!')