from flask import g

from persistence.model.user import User


class UserRepository:
    @staticmethod
    def find_all():
        query = '''
                    SELECT "id", "username", "password", "role"
                        FROM "user"
                        ORDER BY "role", "username";
                '''

        users = []

        for data in g.db.execute(query).fetchall():
            user = User.create_from_data(data)
            users.append(user)

        return users

    @staticmethod
    def find_by_id(user_id):
        query = '''
                    SELECT "id", "username", "password", "role"
                        FROM "user"
                        WHERE "id" = ?;
                '''
        args = (user_id,)

        return User.create_from_data(g.db.execute(query, args).fetchone())

    @staticmethod
    def find_by_username(username):
        query = '''
                    SELECT "id", "username", "password", "role"
                        FROM "user"
                        WHERE "username" = ?;
                        '''
        args = (username,)

        return User.create_from_data(g.db.execute(query, args).fetchone())

    @staticmethod
    def save(user):
        if user.user_id is None:
            query = '''
                        INSERT INTO "user" ("username", "password", "role")
                            VALUES(?, ?, ?);
                    '''
            args = (user.username, user.digest, user.role)
            user.user_id = g.db.execute(query, args).lastrowid
        else:
            query = '''
                        UPDATE "user" SET
                                "username" = ?,
                                "password" = ?,
                                "role" = ?
                            WHERE "id" = ?;
                    '''
            args = (user.username, user.digest, user.role, user.user_id)
            g.db.execute(query, args)

        g.db.commit()

        return user

    @staticmethod
    def delete_by_id(user_id):
        query = '''
                    DELETE FROM "user"
                        WHERE "id" = ?;
                '''
        args = (user_id,)
        g.db.execute(query, args)
        g.db.commit()
