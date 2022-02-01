def menu():
    msg = '''
---Parchis---
1.Enter to game
2.Exit
select:'''
    return msg


def results_message(bd):
    msg = f'''
    player 1:{bd[0].username}, color:{bd[0].color}, dice:{bd[0].dice}, connected:{bd[0].connected}
    player 2:{bd[1].username}, color:{bd[1].color}, dice:{bd[1].dice}, connected:{bd[1].connected}
    turn of:{bd[0].username}
'''
    return msg

def update(user):
    msg = f'''
    user:{user.username}
    dice result:{user.dice}
'''
    return msg


def player_information(bd):
    msg = f'''
number of players:{len(bd)}
name of the players:{",".join(user.username for user in bd)}
colors:{",".join(user.color for user in bd)}'''
    return msg

