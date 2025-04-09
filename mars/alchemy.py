from data import db_session
# from data.users import User
from data.jobs import Job

db_session.global_init('../mars/db/mars_explorer.db')

def main():
    db_sess = db_session.create_session()

    # user = User()
    # user.name = "Scott"
    # user.surname = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "researcher engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.name = "Lelouch"
    # user.surname = "Lamperouge"
    # user.age = 52
    # user.position = "Emperor"
    # user.speciality = "revolution"
    # user.address = "module_0"
    # user.email = "allheillelouch@mars.org"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.name = "Walter"
    # user.surname = "White"
    # user.age = 69
    # user.position = "captain"
    # user.speciality = "drugs(medicine)"
    # user.address = "module_0"
    # user.email = "breakingbad@mars.org"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.name = "Gordon"
    # user.surname = "Freeman"
    # user.age = "42"
    # user.position = "G-man"
    # user.speciality = "scibidi_dop_dop"
    # user.address = "yes_yes"
    # user.email = "skibidi@mars.org"
    # db_sess.add(user)
    # db_sess.commit()

    job = Job()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = "15"
    job.collaborators = "2, 3"
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()



if __name__ == '__main__':
    main()
