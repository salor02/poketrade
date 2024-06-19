from collection.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User

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

    # Creazione di 10 dati dummy per la tabella Set
    for i in range(10):
        Set.objects.create(
            name=f'Dummy Set {i}',
            cod=f'SET{i:02d}',
            release_date=datetime.now().date() + timedelta(days=i),
            img_url=f'/dummy-logo.png',
            game=game
        )
    
    wishlist1 = Wishlist.objects.create(
        user = dummy_user,
        name = 'Dummy wishlist 1'
    )

    wishlist2 = Wishlist.objects.create(
        user = dummy_user,
        name = 'Dummy wishlist 2'
    )

    # Creazione di 40 dati dummy per la tabella Card per ogni Set
    for set in Set.objects.all():
        for i in range(40):
            new_card = Card.objects.create(
                name=f'Dummy Card {i}',
                cod=f'CARD{i:02d}/{set.cod}',
                img_url=f'/dummy-card.png',
                set=set
            )

            #aggiunge una carta ogni 10 alle carte possedute dall'utente dummy
            if i%10 == 0:
                new_card.owners.add(dummy_user)
            
            #aggiunge carte alle 2 wishlist dummy
            if i%20 == 0:
                wishlist1.cards.add(new_card)
            if i%3 == 0:
                wishlist2.cards.add(new_card)


    print('DB popolato')
    

    
