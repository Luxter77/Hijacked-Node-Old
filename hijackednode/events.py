from hijackednode import bot

@bot.event
async def on_command_error(context, exception):
    print("|--------------- ERR_ START ----------------|")
    print("Ignoring exception in command {}:".format(context.command), file=sys.stderr)
    traceback.print_exception(
        type(exception), exception, exception.__traceback__, file=sys.stderr
    )
    print("|---------------- ERR_ END -----------------|")
    try:
        await logMe(context.message.content)
    except Exception:
        None
    try:
        await logMe(exception, True)
    except Exception:
        None

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

@bot.event
async def on_ready():
    global logMe
    logMe = LogMe(bot, config)
    async def sec():
        await logMe("[ " + str(dt.datetime.now().timestamp()) + " ]")
        await logMe(str(bot.user) + " Is connected to:")
        await logMe("|-------------------------------------------|")
        for guild in bot.guilds:
            await logMe(" - [" + str(guild.id) + "]: " + str(guild.name) + ".")
        await logMe("|-------------------------------------------|")
        await ReSyncDict(fox=False)
        await logMe("|         Bootup Sequence complete          |")
        await bot.change_presence(activity=discord.Game(name="Complex Numbers"))
        # asyncio.create_task(Wednesday())
    await logMe("|---------------doBootUp-st-----------------|")
    await logMe("|Not really an error, but rather an exploit.|", True)
    await logMe("|-------------------------------------------|")
    await bot.change_presence(activity=discord.Game(name="Waking Up..."))
    if config.LogChan:
        async with bot.get_channel(config.LogChan[0]).typing():
            await sec()
    else:
        await sec()
    await logMe("|-------------- doBootUp End ---------------|")
