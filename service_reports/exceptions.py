class InvalidTransition(Exception):
    pass

class TransitionNotAllowed(Exception):
    '''
    Raised when the transition is in the graph but the action/person is not allowed to perform it.
    '''
    pass