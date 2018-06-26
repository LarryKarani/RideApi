import re
class Validator():
    def __init__(self):
        self.ride_ofer_props = ["name","From","To","car_model","cost","seats_available", "time", ]
        self.ride_request_props = ["name", "From", "To", "seats_needed", "time"]
        self.register_props = ["name","username","email", "password"]
        self.has_numbers = re.compile('[0-9]')
        self.has_special = re.compile('[^\w\s]')

    def validate(self, obj, activity):
        if activity == 'create_ride':
            for prop in self.ride_ofer_props:
                if prop not in obj:
                    return {"message": f"please provide {prop}"}

                if obj[prop].strip() == "":
                    return {'message': f"empty{prop} not allowed"}

                if len(str(obj['name'])) > 100:
                    return {'message': "name should not be more than 100 characters"}

                if self.has_numbers.search(obj['name']) or self.has_special.search(obj['name']):
                    return {'message': 'name should not contain numbers or special character'}

        if activity == 'request_ride':
            for prop in self.ride_request_props:
                if prop not in obj:
                    return {"message": f"please provide {prop}"}

                if obj[prop].strip() == "":
                    return {'message': f"empty{prop} not allowed"}

                if len(str(obj['name'])) > 100:
                    return {'message': "name should not be more than 100 characters"}

                if self.has_numbers.search(obj['name']) or self.has_special.search(obj['name']):
                    return {'message': 'name should not contain numbers or special character'}

        if activity  == 'reg':
            for prop in self.register_props:
                if prop not in obj:
                    return {"message": f"please provide {prop}"}
            for prop in self.register_props:
                if obj[prop].strip()=="":
                    return {'message': f"empty{prop} not allowed"}

                if len(str(obj['name'])) > 100:
                    return {'message': "name should not be more than 100 characters"}
                
                if '@' not in str(obj['email']):
                    return {"message":"Email is invalid"}

                if '.' not in str(obj['email']):
                    return {"message":"Email is invalid"}

                if len(str(obj['password'])) < 8:
                    return {"message":"password cannot be less than 8 characters"}
                if not self.has_numbers.search(obj['password']):
                    return {"message":"password must have atlist one number"}
                if len(str(obj['password'])) > 150:
                    return  {'message': "password should not be more than 150 characters"}

                if len(str(obj['username'])) > 10:
                    return {'message': "username should not be greater than 10 characters"}

                if self.has_numbers.search(obj['name']):
                    return {'message': "name should not contain numbers"}
                
                if self.has_special.search(obj['name']):
                    return {'message': "name should not contain special chars"}
