'''TheEyeLoop said to me if I where to do something like this it would be funny.\n
I, of course, did instantly hiperfixated and did it.
This was a mistake.'''

# :(
from random import choice

class Pain():
    '''
    # You may be asking now:\n
    #    Luxter, why the hug did you make this into a class instead of a recursive function\n
    # I answer:\n
    #    You expect too much out of this dumpster fire of a module.\n
    UPDATE: hug you Loop\n
    UPDATE: THIS IS HARDER THAN IT LOOKS\n
    UPDATE: IT TOOK ME ALL NIGHT BUT I DID IT! self.laugh_maniatically()
    '''

    def why_would_you_do_something_like_this_you_absolute_(self, downstream: list) -> set:
        outstream = []
        for x in downstream:
            if(x.__subclasses__()):
                outstream += list(
                    self.why_would_you_do_something_like_this_you_absolute_(downstream=x.__subclasses__())
                )
            outstream.append(x)
        return(set(outstream))
        # IN THE END IT WAS SO SIMPLE WHY THE HUG DID I OVERCOMPLICATE MYSELF ALL THE WAY ONTO HELL

    def __init__(self, pain):
        print("Hug you Loop.")
        raise(choice(list(self.why_would_you_do_something_like_this_you_absolute_([pain]))))

# if __name__ == '__main__':
#     Pain(BaseException)
