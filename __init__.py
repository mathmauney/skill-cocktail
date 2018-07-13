from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG
import requests
import time


API_KEY = '1'
API_URL = 'https://www.thecocktaildb.com/api/json/v1/{}/'.format(API_KEY)
SEARCH = API_URL + 'search.php'


def search_cocktail(name):
    r = requests.get(SEARCH, params={'s': name})
    if 200 <= r.status_code < 300:
        return r.json()['drinks'][0]
    else:
        return None


def ingredients(drink):
    ingredients = []
    for i in range(1, 15):
        if not drink['strIngredient' + str(i)]:
            break
        ingredients.append(' '.join((drink['strMeasure' + str(i)],
                                    drink['strIngredient' + str(i)])))
    return ingredients


class CocktailSkill(MycroftSkill):
    @intent_file_handler('Recipie.intent')
    def get_recipie(self, message):
        LOG.info('!!!!!!!!!!!')
        LOG.info(message.data['recepie'])
        cocktail = search_cocktail(message.data['recepie'])
        if cocktail:
            ingredient_speech = 'You\'ll need '
            for i in ingredients(cocktail)[:-1]:
                print(i)
                ingredient_speech += ', ' + i
            ingredient_speech += ' and '
            ingredient_speech += ingredients(cocktail)[-1]
            self.speak(ingredient_speech)
            time.sleep(1)
            self.speak(cocktail['strInstructions'])


def create_skill():
    return CocktailSkill()
