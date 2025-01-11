import unittest
from chatbot import Bot



class testBot(unittest.TestCase):
    def test_doesntCrash(self):
        fakeInput = iter(["The dog ate the cat","STOP"])
        bot = Bot(fakeInput.__next__,print)
        bot.run()