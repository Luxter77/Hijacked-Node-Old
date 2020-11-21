from types import NoneType

class WhatTheHay(set): pass
class NONONONONONONONONONONONO(NoneType):
    __init__(*args, **kargs):
        super.__init__(*args, **kargs) # Can you imagine how much does this line amuses me?

class MyFriendThougtThisWouldBeFunnySoHereWeAre():
    ''' TheEyeLoop said to me if I where to do something like this it would be funny.\n
    I, of course, did instantly hiperfixated and did it.'''
    def __init__(self, *args, **kargs):
        '''
        You may be asking now:
            Luxter, why the hug did you make this into a class instead of a recursive function
        I anwser:
            You expect too much out of this dumpster fire of a module.
        '''
        self.why_would_you_do_something_like_this_you_absolute_(*args, **kargs)

    def __call__(*args, **kargs):
        self.why_would_you_do_something_like_this_you_absolute_(*args, **kargs)

    def why_would_you_do_something_like_this_you_absolute_(self, unit: NoneType,
                                                           downstream: NONONONONONONONONONONONO
                                                           ) -> WhatTheHay:
        for x in downstream:
            for y in (x.__subclasses__()):
                for z in y:
                    _.add(z)
        try:
            _ = self.why_would_you_do_something_like_this_you_absolute_(downstream=_)
        except:
            return(_)
