import unittest
try:
    from chatbot import Bot
except Exception as e:
    print("Encountered exception: "+str(e))
    exit(1)

def printExceptionButBetter(e: Exception):
    traceback = []
    Next = e.__traceback__
    while Next is not None:
        traceback.append(Next.tb_lineno)
        Next = Next.tb_next
    print(repr(e),"on lines (in order from first to last called):", traceback)


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
            printExceptionButBetter(e)
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
            try:
                print(output)
                nonlocal testSucceeded
                if "max" in output:
                    testSucceeded = True
            except Exception as e:
                print(f"fakeOutput crashed: {e}")
                raise e
        fakeInput = iter(["My name is Max","What is my name?","STOP"])
        bot = Bot(fakeInput.__next__,fakeoutput)
        try:
            bot.run()
        except Exception as e:
            printExceptionButBetter(e)
            print("did crash")
            testSucceeded = False
        else:
            print("didn't crash")
        self.assertTrue(testSucceeded)
