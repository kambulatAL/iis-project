from events.models import RegisteredUser

default_pass = 'user_pass'

# Create a user
user = RegisteredUser(login='user_login', name='user_name', surname='user_surname', \
                                            password=default_pass, email='user_email', phone_number='user_phone')
user.save()

# Try to create in one line
RegisteredUser.objects.create(login='xblanco00', name='Marimba', surname='Blanco', \
                                            password=default_pass, email='blanco@work.gmail', phone_number='blanco_phone')
