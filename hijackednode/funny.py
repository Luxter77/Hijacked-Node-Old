'''TheEyeLoop said to me if I where to do something like this it would be funny.\n
I, of course, did instantly hiperfixated and did it.
This was a mistake.'''

# :(


def why_would_you_do_something_like_this_you_absolute_(downstream: list) -> set:
    '''
    # You may be asking now:
    #    Luxter, why the hug did you make this into a class instead of a recursive function
    # I anwser:
    #    You expect too much out of this dumpster fire of a module.
    UPDATE: hug you Loop
    UPDATE: THIS IS HARDER THAN IT LOOKS
    UPDATE: IT TOOK ME ALL NIGHT BUT I DID IT! self.laugh_maniatically()
    '''
    outstream = []
    for x in downstream:
        if(x.__subclasses__()):
            outstream += list(why_would_you_do_something_like_this_you_absolute_(downstream=x.__subclasses__()))
        outstream.append(x)
    return(set(outstream))
    # IN THE END IT WAS SO SIMPLE WHY THE HUG DID I OVERCOMPLICATE MYSELF ALL THE WAY ONTO HELL

print(why_would_you_do_something_like_this_you_absolute_([BaseException]))
