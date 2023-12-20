from mastermind import Game
import unittest

class testmastermind(unittest.TestCase):
    '''
    The following functions are to test given values compared to expected
    values, if they don't match then a comment will be printed.
    '''
    colors = ["red", "blue", "green", "yellow", "purple", "black"]

    def test_secret_code(self):
        '''
        Tests to see if secret code returns a list of not
        '''
        g = Game.secret_code(self)
        self.assertIsInstance(g, list, 'not a list')
    
    def test_b_c_marbles(self):
        '''
        Tests to see if b_c_marbles returns a list of not
        '''
        h = Game.b_c_marbles(self, 3, 50)
        self.assertIsInstance(h, list, 'not a list')

if __name__ == "__main__":
    unittest.main(verbosity=3)

