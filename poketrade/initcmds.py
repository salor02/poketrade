from collection.models import *
from user.models import *
from marketplace.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import json
import random

def erase_collection_db():
    print("Cancello il DB collection")
    Game.objects.all().delete()
    Set.objects.all().delete()

def init_collection_db():

    if len(Game.objects.all()) != 0:
        return

    game = Game()
    game.name = "Pokemon"
    game.img_url = "/pokemon-logo.png"
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

    print('DB collection popolato')

def erase_user_DB():
    print('Cancello DB utenti')
    User.objects.all().delete()

def init_user_DB():
    print('Inizializzazione utenti')
    names = ['Brock', 'Ash', 'Lucinda', 'Camilla', 'Rosso']
    users = list()
    for name in names:
        try:
            users.append(User.objects.get(username=name))
        except User.DoesNotExist:
            users.append(User.objects.create_user(username=name, password='prova'))
    print('Utenti creati correttamente')

def get_random_cards(queryset, n=1):
    card_ids = queryset.values_list('id', flat=True)
    return queryset.filter(id__in=random.sample(list(card_ids), n))

def erase_marketplace_db():
    print('Cancello il DB marketplace')
    Listing.objects.all().delete()
    Feedback.objects.all().delete()

def init_marketplace_db():
    
    users = User.objects.all()

    for user in users:
        print(f'Creazione annunci per utente {user.username}')
        for _ in range(5):
            listing = Listing.objects.create(
                description=f"Descrizione dummy da {user.username}",
                price=round(random.uniform(10, 500), 2),
                published=random.choice([True, False]),
                user=user
            )
            listing.cards_for_sale.set(get_random_cards(Card.objects.all(), n=random.randint(1, 15)))
            listing.cards_in_exchange.set(get_random_cards(Card.objects.all(), n=random.randint(1, 15)))
            listing.save()
    
    print('DB marketplace popolato')
    

    
