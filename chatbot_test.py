import unittest
try:
    from chatbot import Bot
except Exception as e:
    print("Encountered exception: "+str(e))
    exit(1)


class testBot(unittest.TestCase):
    def test_doesntCrash(self):
        try:
            fakeInput = iter(["The dog ate the cat","STOP"])
            bot = Bot(fakeInput.__next__,print)
            testSucceeded = True
            bot.run()
        except Exception:
            testSucceeded = False
        self.assertTrue(testSucceeded)
    def test_questions(self):
        try:
            fakeInput = iter(["Is the cat orange?","STOP"])
            bot = Bot(fakeInput.__next__,print)
            testSucceeded = True
            bot.run()
        except Exception as e:
            print(e)
            testSucceeded = False
        self.assertTrue(testSucceeded)