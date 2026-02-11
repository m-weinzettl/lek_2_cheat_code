import json
#load jason data to global variable

def load_from_json(recipe_data_new):
    try:
        with open("./db_json.json", 'r', encoding='utf-8') as from_json:
            recipe_data_new = json.load(from_json)

        return recipe_data_new

recipe_data_new = {}
recipe_data_new = load_from_json(recipe_data_new)  # set global json dict variable

# data validation for user input

def data_validation_name():

    while True:
        name_input = input("Bitte geben Sie einen Rezeptnamen ein (max. 200 Zeichen: ")
        if 0 < len(name_input) <= 200:
            break
        else:
            print("Rezeptname zu lange. Bitte erneut eingeben")

    return name_input

def data_validation_ingredients():
    ingredient_input_new = []
    while True:
        ingredient_input = input("Zutaten (Leer Enter um zu Beenden)\n(Max 100 Zeichen): ")
        if ingredient_input == '':
            break
        if 0 < len(ingredient_input) <= 100:
            ingredient_input_new.append(ingredient_input)
        else:
            print("Zutatenname zu lange. Bitte erneut eingeben")

    return ingredient_input_new


def data_validation_instructions():
    instructions_input_new = []
    while True:
        instructions_input = input("Anleitung (Leer Enter um zu Beenden)\n(Max 100 Zeichen): ")
        if instructions_input == '':
            break
        if 0 < len(instructions_input) <= 100:
            instructions_input_new.append(instructions_input)
        else:
            print("Anleitung zu lange. Bitte erneut eingeben")

    return instructions_input_new


#data search


import json

def search_menu(recipe_data_new):
    print("""
Rezept suchen:
1. Rezeptname
2. Zutat
3. Rezept löschen
4. Abbrechen
""")

    while True:
        choice = input("Option auswählen?")
        if choice == "1":
            search_by_name()
        elif choice == "2":
            recipe_search_by_ingredient()
        elif choice == "3":
            recipe_data_new = delete_recipe(recipe_data_new)
        elif choice == "4":
            break

def search_by_name(recipe_data_new):
    search_name = input("Bitte Rezeptname eingbene: ").lower()
    found = False

    for name, book in recipe_data_new.items():
        if search_name.lower() == name.lower():
            found = True
            print(f"Rezept {name} gefunden!")
            show = input("Wollen Sie die Zutaten anzeigen. (y/n): ")
            if show.lower() == "y":
                for ingredient in book["ingredients"]:
                    print(f" - {ingredient}")
            elif show.lower() == "n":
                break
            else:
                break

    if not found:
        print("Kein Rezept gefunden.")


def recipe_search_by_ingredient(recipe_data_new):
    search_ingredient = input("Bitte Zutat eingeben: ").lower()
    found = False

    for name, book in recipe_data_new.items():
        for ingredient in book["ingredients"]:
            if search_ingredient in ingredient.lower():
                found = True
                print(f"Zutat '{ingredient}' im Rezept '{name}' gefunden!")
                show = input("Rezept anzeigen? (y/n): ")
                if show.lower() == "y":
                    print(f"\nRezept: {name}")
                    print("Zutaten:")
                    for ing in book["ingredients"]:
                        print(f" - {ing}")
                    print("Anleitung:")
                    for instr in book["instructions"]:
                        print(f" - {instr}")
                break

    if not found:
        print("Keine Rezepte mit dieser Zutat gefunden.")


def delete_recipe(recipe_data_new):
    search_name = input("Bitte Rezeptname eingbene: ").lower()
    found = False
    recipe_found = None
    for name, book in recipe_data_new.items():
         if search_name.lower() == name.lower():
            recipe_found = name
            break

    print(f"Rezept {recipe_found} gefunden!")
    delete_yn = input("Wollen Sie das Rezept löschen?")
    if delete_yn.lower() == "y":
        del recipe_data_new[recipe_found]
    with open("./db_json.json", 'w', encoding='utf-8') as db:
        json.dump(recipe_data_new, db, ensure_ascii=False, indent=4)
        print(f"Rezept {recipe_found} gelöscht!")

    return recipe_data_new



#write to json file

import json

def show_recipes_from_db(recipe_data_new):

        for name, book in recipe_data_new.items():
            print(f"\nRezept {name}:")
            print("Zutaten:")
            for ingredient in book["ingredients"]:
                print(f"- {ingredient}")
            print("Anleitung:")
            for instruction in book["instructions"]:
                print(f"- {instruction}")

def write_recipes_to_db(new_recipe, recipe_data_new):

    recipe_data_new[new_recipe.name] = new_recipe.do_dict()

    with open("./db_json.json", 'w', encoding='utf-8') as db:
        json.dump(recipe_data_new, db, ensure_ascii=False, indent=4)
        print(f"Rezept {new_recipe.name}: Erfolgreich gespeichert")

def edit_recipe(recipe_data_new):
    search_name = input("Bitte Rezeptname eingbene: ").lower()
    found = False
    recipe_found = None
    for name, book in recipe_data_new.items():
         if search_name.lower() == name.lower():
            recipe_found = name
            break
    if recipe_found:
        print(f"Rezept {recipe_found} gefunden!")
        edit_yn = input("Wollen Sie den Rezeptnamen ändern?")

        if edit_yn.lower() == "y":
            new_name = input("Bitte neuen Rezeptnamen eingeben.")

            book = recipe_data_new.pop(recipe_found)
            book["name"] = new_name
            recipe_data_new[new_name] = book

            with open("./db_json.json", 'w', encoding='utf-8') as db:
                json.dump(recipe_data_new, db, ensure_ascii=False, indent=4)
                print(f"Rezept {recipe_found} geändert!")

    return recipe_data_new

#class recipe

class Recipe:
    def __init__(self, name=None, ingredients=None, instructions=None, id=None):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.__id = id or uuid.uuid4() #uniqe id for each recipe for db integration

    def get_id(self):
        return self.__id

    def show_ingredients(self):
        print(f"\nZutaten für {self.name}:")
        for ingredient in self.ingredients:
            print(f"- {ingredient}")

    def show_instructions(self):
        print(f"\nAnleitung für {self.name}:")
        for instruction in self.instructions:
            print(f"- {instruction}")

    def fill_recipe(self):


        self.name = data_validation_name()

        self.ingredients = data_validation_ingredients()
        self.instructions = data_validation_instructions()


#code edit for json export

    def do_dict(self):
        return {
            "name": self.name,
            "ingredients":  self.ingredients,
            "instructions": self.instructions,
            "id": str(self.__id)}