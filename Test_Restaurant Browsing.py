import unittest

# RestaurantDatabase class simulates an in-memory database storing restaurant information
class RestaurantDatabase:
    def __init__(self):
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5, "price_range": "$$", "delivery": True},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8, "price_range": "$$$", "delivery": False},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0, "price_range": "$", "delivery": True},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2, "price_range": "$", "delivery": True},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9, "price_range": "$$", "delivery": True}
        ]

    def get_restaurants(self):
        return self.restaurants


# RestaurantBrowsing class handles the logic for filtering restaurants based on user criteria
class RestaurantBrowsing:
    def __init__(self, database):
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        return [restaurant for restaurant in self.database.get_restaurants() if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        return [restaurant for restaurant in self.database.get_restaurants() if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        return [restaurant for restaurant in self.database.get_restaurants() if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        results = self.database.get_restaurants()
        if cuisine_type:
            results = [restaurant for restaurant in results if restaurant['cuisine'].lower() == cuisine_type.lower()]
        if location:
            results = [restaurant for restaurant in results if restaurant['location'].lower() == location.lower()]
        if min_rating:
            results = [restaurant for restaurant in results if restaurant['rating'] >= min_rating]
        return results


# RestaurantSearch class interacts with RestaurantBrowsing to apply user-provided filters
class RestaurantSearch:
    def __init__(self, browsing):
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        return self.browsing.search_by_filters(cuisine_type=cuisine, location=location, min_rating=rating)


# Unit tests for RestaurantBrowsing class
class TestRestaurantBrowsing(unittest.TestCase):
    def setUp(self):
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

    def test_search_by_cuisine(self):
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(restaurant['cuisine'] == "Italian" for restaurant in results))

    def test_search_by_location(self):
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(restaurant['location'] == "Downtown" for restaurant in results))

    def test_search_by_rating(self):
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 4)
        self.assertTrue(all(restaurant['rating'] >= 4.0 for restaurant in results))

    def test_search_by_filters(self):
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Italian Bistro")


# Unit tests for RestaurantSearch class
class TestRestaurantSearch(unittest.TestCase):
    def setUp(self):
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)
        self.search = RestaurantSearch(self.browsing)

    def test_search_integration(self):
        results = self.search.search_restaurants(cuisine="Italian", location="Uptown", rating=3.9)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Pizza Palace")


if __name__ == '__main__':
    unittest.main()