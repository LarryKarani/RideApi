from datetime import datetime 
class User:
    #class variable holds all users
    users = []

    def regester_user(self, name, username, email, password):
        #adds user into the user list and returs the user
        self.date_registered = str(datetime.now())


        self.user_dict ={
                   'username': username,
                   'name': name,
                   'email': email,
                   'password':password,
                   'date_registered': self.date_registered,
                        }

        self.users.append(self.user_dict)

        return self.user_dict
    @staticmethod
    def return_user(username_or_email):
        #returns a user by name or email
        for user in User.users:
            if user['username']== username_or_email or user['email'] == username_or_email:
                return user
    @staticmethod            
    def get_all_users():
        return User.users
