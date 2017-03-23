import unittest
import sys

sys.path.append('/home/ubuntu/workspace/diary/diary/controller')
sys.path.append('/home/ubuntu/workspace/diary')

from diaryEditor import writeDiary, writeToDb
from flask.helpers import get_debug_flag
from diary import create_app
from diary.settings import DevConfig, ProdConfig

#CONFIG = DevConfig if get_debug_flag() else ProdConfig
CONFIG = DevConfig
app = create_app(CONFIG)


class SimpleTest(unittest.TestCase):
    '''
    def setUp(self):
      self.writer= 'WRITER'
      self.title = ''
      self.context = 'CONTEXT'
      self.date = 'DATA'
    '''

    def testNoneCheckWirter(self):
        with self.assertRaises(TypeError):
            writeToDb(None, 'title', 'context', 'date')
    
    def testNoneCheckTitle(self):
        with self.assertRaises(TypeError):
            writeToDb('writer', None, 'context', 'date')
            
    def testValidDate(self):
        with self.assertRaises(ValueError):
            writeToDb('writer', 'TITLE', 'context', '1969-01-01')

    def testNomalCase(self):
        self.assertEqual(writeToDb('writer', 'TITLE', 'context', '1980-01-01'), True)
            


if __name__ == '__main__':  
    unittest.main()