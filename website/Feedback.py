class Feedback:
    count_id = 2
    def __init__(self, date_time, username, email_address, subject, feedback):
        Feedback.count_id +=1
        self.__feedback_id = Feedback.count_id
        self.__date_time = date_time
        self.__username = username
        self.__email_address = email_address
        self.__subject = subject
        self.__feedback = feedback

    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_date_time(self, date_time):
        self.__date_time = date_time

    def set_username(self, username):
        self.__username = username

    def set_email_address(self, email_address):
        self.__email_address = email_address

    def set_subject(self, subject):
        self.__subject = subject

    def set_feedback(self, feedback):
        self.__feedback = feedback

    def get_date_time(self):
        return self.__date_time

    def get_username(self):
        return self.__username

    def get_email_address(self):
        return self.__email_address

    def get_subject(self):
        return self.__subject

    def get_feedback(self):
        return self.__feedback

    def get_feedback_id(self):
        return self.__feedback_id