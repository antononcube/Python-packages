import unittest
from DataTypeSystem import deduce_type, record_types
from DataTypeSystem.Predicates import is_array_of_arrays
from DataTypeSystem.TypeClasses import Assoc, Atom, Pair, Struct, Tuple, Vector
import datetime


class TestDeduceTypeDemo(unittest.TestCase):
    dbRes = [
        ['```json\n', {
            'albums': [{'name': 'Taylor Swift', 'release_date': '2006'}, {'name': 'Fearless', 'release_date': '2008'},
                       {'name': 'Speak Now', 'release_date': '2010'}, {'name': 'Red', 'release_date': '2012'},
                       {'name': '1989', 'release_date': '2014'}, {'name': 'Reputation', 'release_date': '2017'},
                       {'name': 'Lover', 'release_date': '2019'}, {'name': 'Folklore', 'release_date': '2020'},
                       {'name': 'Evermore', 'release_date': '2020'}]}, '\n```'],
        ['```json\n', {
            'albums': [{'name': '19', 'release_date': '2008'}, {'name': '21', 'release_date': '2011'},
                       {'name': '25', 'release_date': '2015'},
                       {'name': 'Live at the Royal Albert Hall', 'release_date': '2011'},
                       {'name': '25: The Complete Edition', 'release_date': '2016'}]}, '\n```'],
        ['```json\n', {
            'albums': [{'name': '+', 'release_date': '2011'}, {'name': '/', 'release_date': '2017'},
                       {'name': '=', 'release_date': '2021'}]}, '\n```'],
        ['```json\n', {'My World': 'November 2009',
                       'My World 2.0': 'March 2010',
                       'Believe': 'June 2012',
                       'Purpose': 'November 2015',
                       'Changes': 'February 2020'}, '\n```'],
        ['```json\n', {
            'albums': [{'name': 'Music of the Sun', 'release_date': '2005'},
                       {'name': 'A Girl Like Me', 'release_date': '2006'},
                       {'name': 'Good Girl Gone Bad', 'release_date': '2007'},
                       {'name': 'Rated R', 'release_date': '2009'},
                       {'name': 'Loud', 'release_date': '2010'},
                       {'name': 'Talk That Talk', 'release_date': '2011'},
                       {'name': 'Unapologetic', 'release_date': '2012'}, {'name': 'Anti', 'release_date': '2016'},
                       {'name': 'R9', 'release_date': 'TBA'}]}, '\n```'],
        ['```json\n', {
            'albums': [{'name': 'Katy Hudson', 'release_date': '2001'},
                       {'name': 'One of the Boys', 'release_date': '2008'},
                       {'name': 'Teenage Dream', 'release_date': '2010'},
                       {'name': 'Prism', 'release_date': '2013'},
                       {'name': 'Witness', 'release_date': '2017'}, {'name': 'Smile', 'release_date': '2020'}]},
         '\n```'],
        ['```json\n', {'albums': [{'name': 'The Fame', 'release_date': '2008'},
                                  {'name': 'Born This Way', 'release_date': '2011'},
                                  {'name': 'Artpop', 'release_date': '2013'},
                                  {'name': 'Joanne', 'release_date': '2016'},
                                  {'name': 'Chromatica', 'release_date': '2020'}]}, '\n```'],
        ['```json\n', {
            'albums': [{'name': 'Doo-Wops & Hooligans', 'release_date': '2010'},
                       {'name': 'Unorthodox Jukebox', 'release_date': '2012'},
                       {'name': '24K Magic', 'release_date': '2016'}]}, '\n```'],
        ['```json\n', {
            'albums': [{'name': 'Kiss Land', 'release_date': '2013'},
                       {'name': 'Beauty Behind the Madness', 'release_date': '2015'},
                       {'name': 'Starboy', 'release_date': '2016'},
                       {'name': 'After Hours', 'release_date': '2020'}]}, '\n```'],
        ['```json\n', {
            'albums': [{'name': 'Overly Dedicated', 'release_date': '2010'},
                       {'name': 'Section.80', 'release_date': '2012'},
                       {'name': 'Good Kid, M.A.A.D City', 'release_date': '2012'},
                       {'name': 'To Pimp a Butterfly', 'release_date': '2015'},
                       {'name': 'DAMN.', 'release_date': '2017'},
                       {'name': 'Mr. Morale & the Big Steppers', 'release_date': '2022'}]}, '\n```']]

    # 1
    def test_record_types1(self):
        self.assertTrue(isinstance(record_types(self.dbRes), list))
        self.assertTrue(is_array_of_arrays(self.dbRes))

    def test_record_types2(self):
        self.assertTrue(record_types(["", {}, ""]), record_types(self.dbRes[0]))


if __name__ == '__main__':
    unittest.main()
