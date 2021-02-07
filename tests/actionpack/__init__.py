from actionpack import Action


class FakeAction(Action):

    result = f'Performing Action.'

    def __init__(self, name=None, exception=None):
        self._name(name)
        self.exception = exception
        self.state = {'this': 'state'}

    def instruction(self):
        return self.result

    def validate(self):
        if self.exception:
            raise self.exception
        return super().validate()

