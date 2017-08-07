from roll_parser import parse
from roller import Die, roll, count

from unittest import TestCase, skip
from unittest.mock import call, Mock, patch, sentinel


class ParserTest(TestCase):

    def test_parse_empty(self):
        self.assertEqual(parse(''), (['2d6'],''))

    def test_parse_constant(self):
        self.assertEqual(parse('1'), (['1'],''))

    def test_parse_add(self):
        self.assertEqual(parse('1+1'), (['1', '+', '1'],''))

    def test_parse_spaces(self):
        self.assertEqual(parse('1 + 1'), (['1', '+', '1'],''))

    def test_parse_subtract(self):
        self.assertEqual(parse('1-2d4'), (['1', '-', '2d4'],''))

    def test_parse_plus(self):
        self.assertEqual(parse('+2'), (['2d6', '+', '2'],''))

    def test_parse_comments(self):
        self.assertEqual(parse('2d6-1 test строка'),
                         (['2d6', '-', '1'],'test строка'))

        self.assertEqual(parse('+2 test'),
                         (['2d6','+','2'],'test'))

        self.assertEqual(parse('+bonus'),
                         (['2d6'],'+bonus'))

        self.assertEqual(parse('d2 d3'),
                         (['d2'],'d3'))

        self.assertEqual(parse('d2d4'),
                         (['d2'],'d4'))

        self.assertEqual(parse('destroy'),
                         (['2d6'],'destroy'))

        self.assertEqual(parse('d3stroy'),
                         (['d3'],'stroy'))

        self.assertEqual(parse('2к6-1 test строка!'),
                         (['2d6', '-', '1'],'test строка!'))

        self.assertEqual(parse('2д6-1 test строка!'),
                         (['2d6', '-', '1'],'test строка!'))


class DieTest(TestCase):

    _randint = None
    def setUp(self):
        patcher = patch('roller.randint')
        self.addCleanup(patcher.stop)
        self._randint = patcher.start()

    def test_d6(self):
        die = Die(6)
        self._randint.return_value = sentinel.d6

        result = die.roll(1)

        self._randint.assert_called_once_with(1, 6)
        self.assertEqual(result, (sentinel.d6,))

    def test_2d6(self):
        die = Die(6)
        self._randint.side_effect = [sentinel.d6_1, sentinel.d6_2]

        result = die.roll(2)

        self._randint.assert_has_calls([call(1, 6), call(1, 6)])
        self.assertEqual(result, (sentinel.d6_1, sentinel.d6_2))


class RollerTest(TestCase):

    def test_roll_nothing(self):
        result = roll([])
        self.assertEqual(result, [])

    def test_roll_const(self):
        result = roll(['1'])
        self.assertEqual(result, [1])

    def test_roll_expr(self):
        result = roll(['1','+','1'])
        self.assertEqual(result, [1,'+',1])

    @patch('roller.Die')
    def test_roll_die(self, mock_die):
        mock_d6 = Mock()
        mock_d6.roll.return_value = sentinel.d6
        mock_die.return_value = mock_d6

        result = roll(['d6'])

        mock_die.assert_called_once_with(6)
        mock_d6.roll.assert_called_once_with(1)
        self.assertEqual(result, [(sentinel.d6,)])

    @patch('roller.Die')
    def test_roll_die(self, mock_die):
        mock_d6 = Mock()
        mock_d6.roll.return_value = [sentinel.d6_1, sentinel.d6_2]
        mock_die.return_value = mock_d6

        result = roll(['2d6'])

        mock_die.assert_called_once_with(6)
        mock_d6.roll.assert_called_once_with(2)
        self.assertEqual(result, [(sentinel.d6_1, sentinel.d6_2)])

    @patch('roller.Die')
    def test_roll_subtract(self, mock_die):
        mock_d6 = Mock()
        mock_d6.roll.return_value = [sentinel.d6_1, sentinel.d6_2]
        mock_die.return_value = mock_d6

        result = roll(['-', '2d6'])

        mock_die.assert_called_once_with(6)
        mock_d6.roll.assert_called_once_with(2)
        self.assertEqual(result, ['-', (sentinel.d6_1, sentinel.d6_2)])
    

class CountTest(TestCase):

    def test_empty(self):
        self.assertEqual(count([]), 0)

    def test_constant(self):
        self.assertEqual(count([1]), 1)

    def test_sum(self):
        self.assertEqual(count([1, '+', 1]), 2)

    def test_subtract(self):
        self.assertEqual(count([3, '-', 1]), 2)

    def test_one_die(self):
        self.assertEqual(count([(1,)]), 1)

    def test_two_dice(self):
        self.assertEqual(count([(1,1)]), 2)
