from elemcore import exceptions



class ConstructValidator():
    def __init__(self):
        pass
    def validate(self, form_data):
        if form_data["defense"] < 1:
            raise exceptions.ConstructValidationError("Defense cannot be less than one")

