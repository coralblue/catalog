from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Product, User

# engine = create_engine('sqlite:///categorymenu.db') 
engine = create_engine('sqlite:///productlistwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


#Menu for UrbanBurger
category1 = Category(name = "Snow Boarding")

session.add(category1)
session.commit()


porductItem1 = Product(name = "Snow Board a", description = "good for canadian snow", price = "$299", course = "winter", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Snow Board b", description = "good for michigan snow", price = "$550", course = "winter", category = category1)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Snow Board c", description = "good for Hokkaido snow", price = "$399", course = "Winter", category = category1)

session.add(porductItem3)
session.commit()




#Menu for Super Stir Fry
category2 = Category(name = "Ski")

session.add(category2)
session.commit()


porductItem1 = Product(name = "Ski 1", description = "good for canadian snow", price = "$799", course = "Autumn", category = category2)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Ski 2", description = "good for michigan snow", price = "$250", course = "Spring", category = category2)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Ski 3", description = "good for Hokkaido snow", price = "$799", course = "Summer", category = category2)

session.add(porductItem3)
session.commit()

porductItem4 = Product(name = "ski 4", description = "", price = "", course = "", category = category2)

session.add(porductItem4)
session.commit()


#Menu for Panda Garden
category1 = Category(name = "Snorkeling")

session.add(category1)
session.commit()


porductItem1 = Product(name = "Pho", description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", price = "", course = "", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Chinese Dumplings", description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", price = "", course = "", category = category1)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Gyoza", description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", price = "", course = "", category = category1)

session.add(porductItem3)
session.commit()

porductItem4 = Product(name = "Stinky Tofu", description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", price = "", course = "", category = category1)

session.add(porductItem4)
session.commit()



#Menu for Thyme for that
category1 = Category(name = "Thyme for That Vegetarian Cuisine ")

session.add(category1)
session.commit()


porductItem1 = Product(name = "Tres Leches Cake", description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", price = "", course = "", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", price = "", course = "", category = category1)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", price = "", course = "", category = category1)

session.add(porductItem3)
session.commit()

porductItem4 = Product(name = "Cauliflower Manchurian", description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", price = "", course = "", category = category1)

session.add(porductItem4)
session.commit()

porductItem5 = Product(name = "Aloo Gobi Burrito", description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", price = "", course = "", category = category1)

session.add(porductItem5)
session.commit()




#Menu for Tony's Bistro
category1 = Category(name = "Tony\'s Bistro ")

session.add(category1)
session.commit()


porductItem1 = Product(name = "Shellfish Tower", description = "", price = "", course = "", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Chicken and Rice", description = "", price = "", course = "", category = category1)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Mom's Spaghetti", description = "", price = "", course = "", category = category1)

session.add(porductItem3)
session.commit()

porductItem4 = Product(name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "", price = "", course = "", category = category1)

session.add(porductItem4)
session.commit()

porductItem5 = Product(name = "Tonkatsu Ramen", description = "Noodles in a delicious pork-based broth with a soft-boiled egg", price = "", course = "", category = category1)

session.add(porductItem5)
session.commit()




#Menu for Andala's 
category1 = Category(name = "Andala\'s")

session.add(category1)
session.commit()


porductItem1 = Product(name = "Lamb Curry", description = "Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.", price = "", course = "", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", price = "", course = "", category = category1)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", price = "", course = "", category = category1)

session.add(porductItem3)
session.commit()

porductItem4 = Product(name = "Nigiri SamplerMaguro, Sake, Hamachi, Unagi, Uni, TORO!", description = "", price = "", course = "", category = category1)

session.add(porductItem4)
session.commit()




#Menu for Auntie Ann's
category1 = Category(name = "Auntie Ann\'s Diner ")

session.add(category1)
session.commit()

porductItem9 = Product(name = "Chicken Fried Steak", description = "Fresh battered sirloin steak fried and smothered with cream gravy", price = "$8.99", course = "Entree", category = category1)

session.add(porductItem9)
session.commit()



porductItem1 = Product(name = "Boysenberry Sorbet", description = "An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness", price = "", course = "", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Broiled salmon", description = "Salmon fillet marinated with fresh herbs and broiled hot & fast", price = "", course = "", category = category1)

session.add(porductItem2)
session.commit()

porductItem3 = Product(name = "Morels on toast (seasonal)", description = "Wild morel mushrooms fried in butter, served on herbed toast slices", price = "", course = "", category = category1)

session.add(porductItem3)
session.commit()

porductItem4 = Product(name = "Tandoori Chicken", description = "Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.", price = "", course = "", category = category1)

session.add(porductItem4)
session.commit()




#Menu for Cocina Y Amor
category1 = Category(name = "Cocina Y Amor ")

session.add(category1)
session.commit()


porductItem1 = Product(name = "Super Burrito Al Pastor", description = "Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla", price = "", course = "", category = category1)

session.add(porductItem1)
session.commit()

porductItem2 = Product(name = "Cachapa", description = "Golden brown, corn-based venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ", price = "", course = "", category = category1)

session.add(porductItem2)
session.commit()

print "added menu items!"

