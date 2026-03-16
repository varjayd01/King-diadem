points_db={}

def add_points(user,amount):

    if user not in points_db:

        points_db[user]=0

    points_db[user]+=amount

    return points_db[user]


def get_points(user):

    return points_db.get(user,0)
