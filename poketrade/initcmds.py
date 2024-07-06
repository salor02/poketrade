from collection.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import json

def erase_db():
    print("Cancello il DB")
    Game.objects.all().delete()
    Set.objects.all().delete()

def init_db():

    if len(Game.objects.all()) != 0:
        return
    
    # Creazione di un nuovo utente
    try:
        dummy_user = User.objects.get(username='ciao')
    except User.DoesNotExist:
        dummy_user = User.objects.create_user(username='ciao', email='ciao@example.com', password='password123')

    game = Game()
    game.name = "Pokemon"
    game.img_url = "/dummy-logo.png"
    game.save()
    
    f = open('./scraper/scraper_data/scraper.json') #da sistemare
    data = json.load(f)

    for set in data[0]['subsets_list']:
        new_set = Set.objects.create(
            name=set['name'],
            cod=set['id'],
            img_url='/img'+set['standard_logo_rel_path'],
            game=game
        )

        for i, card in enumerate(set['cards_list']):
            new_card = Card.objects.create(
                name=card['name_EN'],
                cod=card['cod'][0:3] + set['id'],
                img_url='/img'+card['standard_img_rel_path'],
                move1='Dummy move 1',
                description='Dummy description',
                set=new_set
            )

            if i%4 == 0:
                new_card.move2 = f'Dummy second move {i}'
                new_card.save()
        
    f.close()

    print('DB popolato')
    

    
