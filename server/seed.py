from server        import app, bc
from server.models import Users, ADMIN_ROLE

seed_users = [
    { 'name': 'Administrator', 'username': 'admin', 'password': 'Administr@t0r', 'role': ADMIN_ROLE }
]

def runSeeds():
    print('Seeding DB')
    for seed_user in seed_users:
        user = Users.query.filter_by(username=seed_user['username']).first()
        if user is None:
            pw_hash = bc.generate_password_hash(seed_user['password'])
            user = Users(seed_user['name'], seed_user['username'], pw_hash, seed_user['role'])
            print("Adding user: %s" % seed_user['username'])
            user.save()

# Setup database
@app.before_first_request
def initialize_database():
    runSeeds()