import unittest
try:
    from chatbot import Bot
except Exception as e:
    print("Encountered exception: "+str(e))
    exit(1)


class testBot(unittest.TestCase):
    def test_doesntCrash(self):
        fakeInput = iter(["The dog ate the cat","The quick brown fox jumped over the lazy dog","STOP"])
        bot = Bot(fakeInput.__next__,print)
        testSucceeded = True
        try:
            bot.run()
        except Exception:
            testSucceeded = False
        self.assertTrue(testSucceeded)
    def test_questions(self):
        def fakeOutput(text):
            if text == "no":
                global testSucceeded
                testSucceeded = False
        fakeInput = iter(["Is the cat orange?","STOP"])
        bot = Bot(fakeInput.__next__,fakeOutput)
        testSucceeded = True
        try:
            bot.run()
        except Exception as e:
            print(e)
            testSucceeded = False
        self.assertTrue(testSucceeded)
    def test_oneWordGibberish(self):
        fakeInput = iter(["hbjneib","STOP"])
        bot = Bot(fakeInput.__next__,lambda _: None)
        testSucceeded = True
        try:
            bot.run()
        except Exception as e:
            print(e)
            testSucceeded = False
        self.assertTrue(testSucceeded)
    def test_emptyInput(self):
        fakeInput = iter(["","  ","STOP"])
        bot = Bot(fakeInput.__next__,lambda _: None)
        testSucceeded = True
        try:
            bot.run()
        except Exception as e:
            print(e)
            testSucceeded = False
        self.assertTrue(testSucceeded)
    def test_remembersName(self):
        testSucceeded = False
        def fakeoutput(output: str):
            nonlocal testSucceeded
            if "max" in output:
                testSucceeded = True
        fakeInput = iter(["My name is Max","What is my name?","STOP"])
        bot = Bot(fakeInput.__next__,fakeoutput)
        try:
            bot.run()
        except Exception as e:
            print(e)
            testSucceeded = False
        self.assertTrue(testSucceeded)
