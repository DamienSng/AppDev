class Survey:
    count_id = 10
    chinese_id = 2
    korean_id = 3
    japanese_id = 1
    mexican_id = 1
    thai_id = 2
    indian_id = 1
    def __init__(self, date_time, username, email_address, cuisine, recipe_name):
        Survey.count_id += 1
        self.__survey_id = Survey.count_id
        self.__date_time = date_time
        self.__username = username
        self.__email_address = email_address
        self.__cuisine = cuisine
        self.__recipe_name = recipe_name

    def increment(self, cuisine):
        if cuisine == "Chinese":
            Survey.chinese_id = Survey.chinese_id + 1
        elif cuisine == "Korean":
            Survey.korean_id = Survey.korean_id + 1
        elif cuisine == "Japanese":
            Survey.japanese_id = Survey.japanese_id + 1
        elif cuisine == "Mexican":
            Survey.mexican_id = Survey.mexican_id + 1
        elif cuisine == "Thai":
            Survey.thai_id = Survey.thai_id + 1
        elif cuisine == "Indian":
            Survey.indian_id = Survey.indian_id + 1

    def decrement(self, cuisine):
        if cuisine == "Chinese":
            Survey.chinese_id = Survey.chinese_id - 1
        elif cuisine == "Korean":
            Survey.korean_id = Survey.korean_id - 1
        elif cuisine == "Japanese":
            Survey.japanese_id = Survey.japanese_id - 1
        elif cuisine == "Mexican":
            Survey.mexican_id = Survey.mexican_id - 1
        elif cuisine == "Thai":
            Survey.thai_id = Survey.thai_id - 1
        elif cuisine == "Indian":
            Survey.indian_id = Survey.indian_id - 1

    def set_chinese_id(self, chinese_id):
        self.chinese_id = chinese_id

    def get_chinese_id(self):
        return self.chinese_id


    def set_survey_id(self, survey_id):
        self.__survey_id = survey_id

    def set_date_time(self, date_time):
        self.__date_time = date_time

    def set_username(self, username):
        self.__username = username

    def set_email_address(self, email_address):
        self.__email_address = email_address

    def set_cuisine(self, cuisine):
        self.__cuisine = cuisine

    def set_recipe_name(self, recipe_name):
        self.__recipe_name = recipe_name

    def get_survey_id(self):
        return self.__survey_id

    def get_date_time(self):
        return self.__date_time

    def get_username(self):
        return self.__username

    def get_email_address(self):
        return self.__email_address

    def get_cuisine(self):
        return self.__cuisine

    def get_recipe_name(self):
        return self.__recipe_name