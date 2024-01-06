Doggeł Inc Package for all services
How do I use it?
It's really simple we were working to make it the simpliest. For example:

Importing package

```
from Doggel_Inc import DI
```

Setting up key

```
DI.setup("YOUR API KEY")
```

Making requests example Discord AI using chat command

```
@bot.command()
async def chat(ctx, message):
    await ctx.send(await DI.request(ctx.author.id, ctx.author.name, message))
```

Everything simple! For more detailed info concact on email or join our discord support server!