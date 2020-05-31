class Data():
    def __init__(self, username, to_person):
        '''
        constructor

        :param username: save the username of application
        :param to_person: save the name of person to whom it will send
        '''
        self.username = username
        self.to_person = to_person
        self.path = 'C:/clip-to-clip/'
        self.filename = ''