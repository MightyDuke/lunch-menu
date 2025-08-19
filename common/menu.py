from datetime import date

class Day:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: int):
        self.items.append((name, price))

class Menu:
    def __init__(self):
        self.menu = {}

    def create_day(self, when: date):
        day = Day()
        self.menu[when] = day

        return day
    
    def serialize(self):
        return {
            when if when else "week": [
                { 
                    "name": name, 
                    "price": price 
                }
                for name, price
                in days.items
            ]
            for when, days
            in self.menu.items()
            if len(days.items) > 0
        }