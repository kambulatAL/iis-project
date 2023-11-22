from events.models import RegisteredUser, Worker, Category, EventPlace, Event, EventEstimation

RegisteredUser.create_user('xblanco00', 'Marimba', 'Blanco', 'blanco@work.gmail', 'blanco_phone')
RegisteredUser.create_user('user_login', 'user_name', 'user_surname', 'user_email', 'user_phone')
RegisteredUser.create_user('xassat00', 'Dias', 'Assatulla', 'xassat@work.gmail', '+420 777 777 777', is_admin=True)
RegisteredUser.create_user('xapada00', 'Parad', 'Moshi-Moshi', 'xapada@work.gmail', '+420 333 777 777',
                           is_moderator=True)
RegisteredUser.create_user('moder_login', 'Moder', 'Moderovich', 'email@email.cz', '+420 333 777 777',
                           is_moderator=True)

# Create default categories
Category.objects.create(
    name='Music',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

Category.objects.create(
    name='Museum',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

Category.objects.create(
    name='Food',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

Category.objects.create(
    name='Movies',
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

# Create event places
plz = EventPlace.objects.create(
    city='Plzeň',
    street='Kopeckého sady 13',
    place_name='Měšťanská beseda - Kino Beseda',
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

prh4 = EventPlace.objects.create(
    city='Praha 4',
    street='Ledvinova 9',
    place_name='Chodovská tvrz',
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

brn = EventPlace.objects.create(
    city='Brno',
    street='náměstí Svobody',
    created=RegisteredUser.objects.get(username='user_login'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

hrdc_krl = EventPlace.objects.create(
    city='Hradec Králové',
    street='Eliščino nábřeží 465',
    place_name='Muzeum východních Čech',
    created=RegisteredUser.objects.get(username='user_login'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)

# Create event
event1 = Event.objects.create(
    name="Rozsvícení vánočního stromu na náměstí Svobody",
    start_date="2023-11-24",
    end_date="2023-11-24",
    start_time="16:00",
    end_time="20:00",
    photo="images/events/23/11/22/vanoce.jpeg",
    capacity=100,
    ticket_price=0,
    description="Přijďte s námi 24. listopadu rozsvítit vánoční strom na náměstí Svobody,"
                "kde stál už v roce 1924 vůbec první vánoční strom u nás a dost možná i v celé střední Evropě."
                "Užijeme si společně slavnostní večer a připraven je jako vždy i kulturní program, který začíná už v 16 hodin."
                "Slavnostní rozsvícení vánočního stromu proběhne v 17 hodin za přítomnosti čelních představitelů města a Biskupství brněnského."
                "16:00 Dětský sbor"
                "Slavnostní proslovy a zdravice primátorky Brno"
                "Wall Dancing"
                "Žehnání stromu Biskupem Brněnským"
                "17:00 Rozsvícení vánočního stromu"
                "17:30 Heart of Dixie",
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)
event1.registered_people.add(RegisteredUser.objects.get(username='xblanco00'))
event1.categories.add(Category.objects.get(name='Music'))
event1.categories.add(Category.objects.get(name='Food'))
event1.event_place = brn
event1.save()

## Create event
event2 = Event.objects.create(
    name="HARRY POTTER: FILMOVÝ MARATON 2023",
    start_date="2023-10-25",
    end_date="2023-10-26",
    start_time="08:00",
    end_time="22:00",
    photo="images/events/23/11/22/potter.jpeg",
    capacity=80,
    ticket_price=40,
    description="Během dvou dny – 25. a 26. 10. 2023 – uvede Kino Beseda maraton všech osmi filmů Harryho Pottera."
                " V ceně 40 euro bude zahrnuto i občerstvení, u něhož diváci mohou nabrat síly mezi jednotlivými filmy."
                "Ty budou uvedeny v originálním anglickém znění s českými titulky.",
    created=RegisteredUser.objects.get(username='user_login'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)
event2.categories.add(Category.objects.get(name='Movies'))
event2.categories.add(Category.objects.get(name='Food'))
event2.event_place = plz
event2.registered_people.add(RegisteredUser.objects.get(username='user_login'))
event2.save()

event3 = Event.objects.create(
    name="Mao Norioka a Alessandro Mastracci",
    start_date="2023-11-22",
    end_date="2023-11-22",
    start_time="19:00",
    end_time="21:30",
    photo="images/events/23/11/22/nao_music.jpg",
    capacity=120,
    ticket_price=10,
    description="Hudba je náš jazyk, který nezná hranic."
                "Duo zahraničních hudebníků představí světové skladby pro klavír a violoncello:"
                "Beethoven, Shubert (Německo), Prokofjev (Rusko), M. Tokujama (Japonsko) Mao Norioka (Japonsko) – klavír,"
                "Alessandro Mastracci (Itálie) – violoncello."
                "Koncert zahraničních absolventů Akademie múzických umění v Praze.",
    event_place=prh4,
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)
event3.registered_people.add(RegisteredUser.objects.get(username='xblanco00'))
event3.categories.add(Category.objects.get(name='Music'))
event3.save()

event4 = Event.objects.create(
    name="Muzejní adventní trh v Hradci Králové",
    start_date="2023-12-01",
    end_date="2023-12-03",
    start_time="00:00",
    end_time="00:00",
    photo="images/events/23/11/22/museum_hrdc.jpeg",
    capacity=200,
    ticket_price=3,
    description="Již 34 let mají návštěvníci Muzejního adventního trhu příležitost prožít si první adventní víkend"
                "nadcházejícího předvánoční času v sepětí s tradicí v neopakovatelné atmosféře a ve společnosti poctivých řemeslníků."
                "XXXIV. ročník bude 1. – 3. prosince 2023 zaměřen nejen na prodej, ale také ve větší míře na prezentaci a ukázky poctivé řemeslné práce."
                "Před budovou muzea budou prodávány tradiční pochutiny a nápoje, vítány jsou výrobky s označením regionální produkt (www.regionalni-znacky.cz)."
                "Muzeum východních Čech v Hradci Králové chrání hodnoty vytvářené po celá staletí našimi předky, které tvoří základ kulturní identity celého kraje."
                "Letošní trh se uskuteční pouze ve venkovních prostorách Eliščina nábřeží a přilehlého okolí"
                "Pátek 15 - 20 hodin"
                "Sobota 9 - 19 hodin"
                "Neděle 9 - 16 hodin",
    event_place=hrdc_krl,
    created=RegisteredUser.objects.get(username='xblanco00'),
    accepted=Worker.objects.get(worker=RegisteredUser.objects.get(username='xassat00')),
    approved_by_mods=True
)
event4.registered_people.add(RegisteredUser.objects.get(username='xblanco00'))
event4.categories.add(Category.objects.get(name='Museum'))
event4.save()
