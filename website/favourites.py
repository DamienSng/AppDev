# Recipe class
class fav:
    recipes = []

#####################################################################################################################
    # initializer method
    def __init__(self, id, title, image, skill, time, instruction, cuisine, ingredient, alt, optional):
        self.id = id
        self.title = title
        self.cuisine = cuisine
        self.skill = skill
        self.time = time
        self.instruction = instruction
        self.ingredient = ingredient
        self.alt = alt
        self.optional = optional
        self.image = image



# change the class to match initalization with the order of which the parameters are passed in
# The order this recipe class initalize the class attributes dictates which attributes comes first
# make sure the order of which the parameters are passed in matches the order in '__init__'

#####################################################################################################################

    def set_recipe_id(self, recipe_id):
        self.recipe_id = recipe_id
    def set_title(self, title):
        self.title = title
    def set_cuisine(self, cuisine):
        self.cuisine = cuisine
    def set_skill(self, skill):
        self.skill = skill
    def set_time(self, time):
        self.time = time
    def set_instruction(self, instruction):
        self.instruction = instruction
    def set_ingredient(self, ingredient):
        self.ingredient = ingredient
    def set_alt(self, alt):
        self.alt = alt
    def set_optional(self, optional):
        self.optional = optional
    def set_image(self, image):
        self.image = image

    '''def search_recipes(self, query):
        results = []
        for recipe in self.recipes:
            if query.lower() in recipe['name'].lower():
                results.append(recipe)
        return results'''