import re
class Validator():
    def __init__(self, obj , actity):

        self.ride_ofer_props = ["current_location","destination","depature_time","cost","seats_available" ]
        self.ride_request_props = [ "current_location", "destination", "depature_time", "Username"]
        self.register_props = ["username","email", "password"]
        self.reply_props =["reply"]
        self.has_numbers = re.compile('[0-9]')
        self.has_special = re.compile('[^\w\s]')
        self.activity=actity
        self.obj = obj

    def validate(self):
        
        if self.activity == 'create_ride':
            for prop in self.ride_ofer_props:
                if prop not in self.obj or  self.obj[prop].strip() == "":
                    return {"message": f"please provide {prop}"}

        if self.activity == 'request_ride':
            for prop in self.ride_request_props:
                if prop not in self.obj or self.obj[prop].strip() == "":
                    return {"message": f"please provide {prop}"}

        if self.activity == 'reply':
            for prop in self.reply_props:
                if prop not in self.obj or  self.obj[prop].strip():
                    return {"message": f"please provide {prop}"}

        if self.activity  == 'reg':
            for prop in self.register_props:
                if prop not in self.obj or  self.obj[prop].strip()=="":
                    return {"message": f"please provide {prop}"}
            
                
                if '@' not in str(self.obj['email']) or '.' not in str(self.obj['email']):
                    return {"message":"Email is invalid"}


                if len(str(self.obj['password'])) < 8:
                    return {"message":"password cannot be less than 8 characters"}
                if not self.has_numbers.search(self.obj['password']):
                    return {"message":"password must have atlist one number"}
                if len(str(self.obj['password'])) > 150:
                    return  {'message': "password should not be more than 150 characters"}

                if len(str(self.obj['username'])) > 10:
                    return {'message': "username should not be greater than 10 characters"}

                if self.has_numbers.search(self.obj['username']) or self.has_special.search(self.obj['username']):
                    return {'message': "invalid username"}

            
