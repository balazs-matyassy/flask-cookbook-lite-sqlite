from flask import g

from persistence.model.recipe import Recipe


class RecipeRepository:
    @staticmethod
    def find_all():
        query = '''
                    SELECT "id", "category", "name", "description", "difficulty"
                        FROM "recipe"
                        ORDER BY "category", "name";
                '''

        recipes = []

        for data in g.db.execute(query).fetchall():
            recipe = Recipe.create_from_data(data)
            recipes.append(recipe)

        return recipes

    @staticmethod
    def find_by_id(recipe_id):
        query = '''
                    SELECT "id", "category", "name", "description", "difficulty"
                        FROM "recipe"
                        WHERE "id" = ?;
                '''
        args = (recipe_id,)

        return Recipe.create_from_data(g.db.execute(query, args).fetchone())

    @staticmethod
    def find_by_name(name):
        query = '''
                    SELECT "id", "category", "name", "description", "difficulty"
                        FROM "recipe"
                        WHERE "name" LIKE ?
                        ORDER BY "category", "name";
                '''
        args = (f'%{name}%',)

        recipes = []

        for data in g.db.execute(query, args).fetchall():
            recipe = Recipe.create_from_data(data)
            recipes.append(recipe)

        return recipes

    @staticmethod
    def save(recipe):
        if recipe.recipe_id is None:
            query = '''
                        INSERT INTO "recipe" ("category", "name", "description", "difficulty")
                            VALUES(?, ?, ?, ?);
                    '''
            args = (recipe.category, recipe.name, recipe.description, recipe.difficulty)
            recipe.recipe_id = g.db.execute(query, args).lastrowid
        else:
            query = '''
                        UPDATE "recipe" SET
                                "category" = ?,
                                "name" = ?,
                                "description" = ?,
                                "difficulty" = ?
                            WHERE "id" = ?;
                    '''
            args = (recipe.category, recipe.name, recipe.description, recipe.difficulty, recipe.recipe_id)
            g.db.execute(query, args)

        g.db.commit()

        return recipe

    @staticmethod
    def delete_by_id(recipe_id):
        query = '''
                    DELETE FROM "recipe"
                        WHERE "id" = ?;
                '''
        args = (recipe_id,)
        g.db.execute(query, args)
        g.db.commit()
