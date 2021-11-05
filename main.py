import discord
import json
import sys
import argparse
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
output_filename = "mutuals.json"

def build_users(guilds: list,values) -> dict:
    users = dict()
    for i, g in enumerate(guilds):
        print(f"{i+1}/{len(guilds)} {g} {g.id}")
        g = client.get_guild(g.id)

        print(values)

        playerRoles = dict()
        

        for m in g.members:
            name = f"{m.name}#{m.discriminator}"
            
            if name in users:
                users[name]['servers'].add(g.name)
            else:
                users[name] =  {'servers':dict(),'roles':dict()}
                users[name]['servers'] = {g.name}
            
            playerRoles = []
            if g.name in values:
                targetUser = discord.utils.get(g.members, id=m.id)
                for x in targetUser.roles:
                    playerRoles.append(str(x))
            
        
            users[name]['roles'][g.name] = playerRoles

            
        print(f"|____ {len(g.members)} users")
    print()
    return users

def filter_mutuals(users: dict,values) -> dict:    
    mutuals = {m:users[m] for m in users if len(users[m]) > 1}
    query_guilds = values
    query_roles_A = ['Federation Member']
    query_roles_B = ['[NO] Please Stop']
    print('##############')
    print(query_guilds)
    if len(sys.argv) > 1:
        mutuals = {m:users[m] for m in mutuals if all([g in users[m]['servers'] for g in query_guilds]) and all([g in users[m]['roles']['The Silent'] for g in query_roles_A]) and all([g in users[m]['roles']['Banana Blender'] for g in query_roles_B])}
    return mutuals

def build_json_object(mutual_users: dict) -> dict:
    return {
        "users_total":len(mutual_users),
        "users":[
            {
                "name":m,
                "guilds_total":len(mutual_users[m]['servers']),
                "guilds":json.dumps(mutual_users[m]['servers'],cls=SetEncoder),
                "roles":json.dumps(mutual_users[m]['roles'],cls=SetEncoder)
            } for m in sorted(mutual_users)
        ]
    }

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)


@client.event
async def on_ready():
    print("ready")

    print('####')
    parser = argparse.ArgumentParser()
    parser.add_argument('--s1', help='server name 1')
    parser.add_argument('--s2', help='server name 2')

    values = vars(parser.parse_args())
    values = values['s1'],values['s2']

    guilds = await client.fetch_guilds(limit=None).flatten()
    users = build_users(guilds,values)
    mutual_users = filter_mutuals(users,values)
    json_s = json.dumps(build_json_object(mutual_users))

    with open(output_filename, "w", encoding="utf-8") as fptr:
        fptr.write(json_s)

    print(f"Found {len(mutual_users)} mutual users")
    print(f"Results written to {output_filename}")
    #await client.close()


with open("token.txt", "r") as fptr:
    token = fptr.read().strip().replace('"', "")

client.run(token, bot=False)
