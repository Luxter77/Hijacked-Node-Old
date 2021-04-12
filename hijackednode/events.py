from hijackednode import bot

@bot.event
async def on_command_error(context, exception):
    print("|--------------- ERR_ START ----------------|")
    print("Ignoring exception in command {}:".format(context.command), file=sys.stderr)
    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)
    print("|---------------- ERR_ END -----------------|")
    try:
        await logMe(context.message.content)
    except Exception:
        pass
    try:
        await logMe(exception, True)
    except Exception:
        pass

@bot.event
async def on_error(event_method, *args, **kwargs):
    try:
        await logMe(" ``` " + str(event_method) + " ``` ", True)
        await logMe(" ``` " + traceback.format_exc() + " ``` ", True)
    except Exception:
        print("|--------------- ERR_ START ----------------|")
        print(" Ignoring exception in {}".format(event_method), file=sys.stderr)
        traceback.print_exc()
        print("|----------------- ERR_ END -----------------|")
