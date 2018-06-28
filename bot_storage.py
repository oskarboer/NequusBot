import os
import pickle
import random


class Storage(object):
    # name of file of your python script(name of this file)
    script_name = "bot_storage.py"
    script_path = "/".join(os.path.abspath(script_name).split("/")[:-1]) + "/"

    def __init__(self, storage_name, storage_path=script_path):
        self.storage_name = storage_name
        self.filepath = storage_path
        self.storage_path = storage_path + storage_name + ".pkl"


        try:
            open(self.storage_path)
        except:
            d = {}
            self.save_storage(d)

    def save_storage(self, obj):
        with open(self.storage_path, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_storage(self):
        with open(self.storage_path, 'rb') as f:
            return pickle.load(f)

    def add_item(self, word, meaning):
        d = self.load_storage()
        d[word] = meaning
        self.save_storage(d)

    def get_item(self, name):
        d = self.load_storage()
        if name in d.keys():
            meaning = name + ":\n" + d[word]
            return meaning
        else:
            return "Lol, 404, add it first"

    def list_items(self):
        d = self.load_storage()
        out = ''
        for i in d.keys():
            out += str(i) + "\n"
        return out

    def check_item(self, word):
        d = self.load_storage()
        if word in d.keys():
            return True
        else:
            return False

    def random_items(self, number):
        out = ''

        storage = self.load_storage()
        choice = random.sample(list(storage.keys()), number)

        for i in choice:
            out += i + ":\n" + storage[i] + "\n" + "\n"
        return out


if __name__ == "__main__":
    script_name = "Dictionary_for_bot.py"

    script_path = "/".join(os.path.abspath(script_name).split("/")[:-1]) + "/"

    print(script_path)

    d = customDictionary("test")

    # d.add_word("nequus", "I usually use it as my nick name")
    # d.add_word("sos", "It's just sos, no more, no less")
    d.add_item("sasa", "bush, badam")
    # d.add_word("ses", "Damn, you are stubborn. !!!Achievement unlocked!!!")

    print(d.get_item("sos"))
    print(d.list_items())

