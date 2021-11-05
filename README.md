# Discord-Mutual-Users

Self-bot script to seek out people you share mutual servers with.

Beware that self-bots are technically not allowed and you might get in trouble for using one.

# Usage
Put your user token into ```token.txt``` and run ```main.py.``` The output will get exported to a new ```mutuals.json``` file.

Specifying arguments
You can pass guilds as arguments into the script, seperated by semicolons. This filters the output, such that it will filter out mutuals that are not in every guild specified. For example, the following Powershell query will only return mutuals that are in at least both ```Server 1 Name``` and ```Server 2 Name```:

```python.exe .\main.py --s1 Server 1 Name --s2 Server 2 Name```

(The backticks are there to escape Powershell formatting.)

How to get your user token:

- open discord client
- ctrl + shift + i
- Application -> local storage -> discordapp.com
- Refresh (F5)
- token string should now show up at the bottom of the local storage, copy it into ```token.txt```
