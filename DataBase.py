import sqlite3
import vk_api



class DataBase:
    """
    Доступ к Базе данных осуществляется при при помощи данного экземпляра данного класса


    sendTokenToDataBase
    deleteInvalidToken
    getDataBase
    getID

    """
    def __init__(self):
        self.tokens = [0] # ноль лишь потому что если только один токен в массиве, то обработчик проходит по строке в цикле фор
        self.getDataBase()

    def _addToken(self, token: str):
        self.tokens.append(token)

    def _createDataBase(self):
        if 1:
            with sqlite3.connect('access_token.db') as con:
                cur = con.cursor()
                cur.execute("""
                    CREATE TABLE access_tokens(
                    access_token TEXT,
                    id INTEGER PRIMARY KEY
                    )
                """)

    def getDataBase(self):
        try:
            with sqlite3.connect('access_token.db') as con:
                cur = con.cursor()
                z = cur.execute('SELECT access_token FROM access_tokens')
                for token in z:
                    self.tokens.append(token[0])
        except sqlite3.OperationalError:
            self._createDataBase()

    def sendTokenToDataBase(self, token: str):
        try:
            vk = vk_api.VkApi(token=token)
            vk = vk.get_api()
            id = str(vk.users.get()[0]['id'])
            with sqlite3.connect('access_token.db') as con:
                cur = con.cursor()
                cur.execute(f'INSERT INTO access_tokens(access_token, id) VALUES ("{token}", {id})')
                con.commit()
            self._addToken(token)
            return token
        except:
            pass

    def getTokenAndSendToDB(self, login: str, password: str ):
        try:
            vk_session = vk_api.VkApi(login, password, app_id=2685278)
            vk_session.auth()
            self.sendTokenToDB(vk_session.token['access_token'])
            return vk_session.token['access_token']
        except:
            pass

    def deleteInvalidToken(self, token):
        try:
            with sqlite3.connect('access_token.db') as con:
                cur = con.cursor()
                cur.execute(f'DELETE FROM access_tokens WHERE access_token="{token}"')
                con.commit()
            self.tokens.remove(token)
        except:
            pass

    def getID(self):
        try:
            with sqlite3.connect('access_token.db') as con:
                cur = con.cursor()
                return cur.execute('SELECT id FROM access_tokens')
        except sqlite3.OperationalError:
            pass
