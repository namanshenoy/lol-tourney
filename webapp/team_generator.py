from random import randint
import time
import string
from webapp.models import Team
import random

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


class Player:
    MMR = 0
    primary_role = 0
    secondary_role = 0
    lol_summoner_name = randomword(5)

    def __init__(self):
        self.primary_role = randint(1, 5)

        self.secondary_role = randint(1, 5)

	self.lol_summoner_name = randomword(5)

        rank = randint(0, 10000)
        if(rank <= 3):
            self.lol_mmr = randint(2900, 3200)
        elif(rank <= 8):
            self.lol_mmr = randint(2550, 2899)
        elif(rank <= 168):
            self.lol_mmr = randint(2200, 2549)
        elif(rank <= 803):
            self.lol_mmr = randint(1850, 2199)
        elif(rank <= 2403):
            self.lol_mmr = randint(1500, 1849)
        elif(rank <= 6144):
            self.lol_mmr = randint(1150, 1499)
        elif(rank <= 10000):
            self.lol_mmr = randint(900, 1145)


        while (self.secondary_role == self.primary_role):
            self.secondary_role = randint(1, 5)

def make_teams(List):
    # List = []
    print('Making Teams')
    totalMMR = 0
    totalPlayers = 0
    for player in List.all():
        totalPlayers +=1
    #rand = randint(50,150)
    #print("Random number = " + str(rand))
    for player in List.all():
        totalMMR += player.lol_mmr
    '''
    for x in range(1, rand+1):
        List.append(Player())
        totalMMR += List[x - 1].lol_mmr
        totalPlayers += 1
        '''
    '''subsList = []
    if totalPlayers % 5 != 0:
        while totalPlayers %5 != 0:
            subsList.append(List[-1])
    	del List[-1]
    	totalPlayers -=1

    for player in subsList:
        print(player.lol_mmr)
    '''

    avgMMR = totalMMR / totalPlayers
    maxPlayersPerPref = int(totalPlayers / 5)
    print('max playersperpref = ' + str(maxPlayersPerPref))
    # list is indexed 0-99

    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    subs = []

    for item in List.all():
        if item.primary_role == 1 and len(p1) < maxPlayersPerPref:
            p1.append(item)
        elif item.primary_role == 2 and len(p2) < maxPlayersPerPref:
            p2.append(item)
        elif item.primary_role == 3 and len(p3) < maxPlayersPerPref:
            p3.append(item)
        elif item.primary_role == 4 and len(p4) < maxPlayersPerPref:
            p4.append(item)
        elif item.primary_role == 5 and len(p5) < maxPlayersPerPref:
            p5.append(item)

        elif item.secondary_role == 1 and len(p1) < maxPlayersPerPref:
            p1.append(item)
        elif item.secondary_role == 2 and len(p2) < maxPlayersPerPref:
            p2.append(item)
        elif item.secondary_role == 3 and len(p3) < maxPlayersPerPref:
            p3.append(item)
        elif item.secondary_role == 4 and len(p4) < maxPlayersPerPref:
            p4.append(item)
        elif item.secondary_role == 5 and len(p5) < maxPlayersPerPref:
            p5.append(item)

        elif len(p1) < maxPlayersPerPref:
            p1.append(item)
        elif len(p2) < maxPlayersPerPref:
            p2.append(item)
        elif len(p3) < maxPlayersPerPref:
            p3.append(item)
        elif len(p4) < maxPlayersPerPref:
            p4.append(item)
        elif len(p5) < maxPlayersPerPref:
            p5.append(item)

        else:
            subs.append(item)

    print('\nSubs')
    for sub in subs:
    	print (sub.lol_summoner_name + " " +str(sub.lol_mmr))

    print('\nPref 1 = ' + str(len(p1)))
    counter = 1
    for i in p1:
        print(str(counter) + ' ' + i.lol_summoner_name+' ' + str(i.lol_mmr))
        counter += 1
    print('\nPref 2 = ' + str(len(p2)))
    counter = 1
    for i in p2:
        print(str(counter) + ' ' +i.lol_summoner_name+' '+ str(i.lol_mmr))
        counter += 1
    print('\nPref 3 = ' + str(len(p3)))
    counter = 1
    for i in p3:
        print(str(counter) + ' ' + i.lol_summoner_name + ' '+ str(i.lol_mmr))
        counter += 1
    print('\nPref 4 = ' + str(len(p4)))
    counter = 1
    for i in p4:
        print(str(counter) + ' ' + i.lol_summoner_name+ ' ' + str(i.lol_mmr))
        counter += 1
    print('\nPref 5 = ' + str(len(p5)))
    counter = 1
    for i in p5:
        print(str(counter) + ' ' + i.lol_summoner_name+' '+str(i.lol_mmr))
        counter += 1

    team = []

    # balance preferences

    print('Teams:\n')

    for x in range(0, totalPlayers/5):
        team.append([])
        team[x].append(p1.pop(0))
        team[x].append(p2.pop(0))
        team[x].append(p3.pop(0))
        team[x].append(p4.pop(0))
        team[x].append(p5.pop(0))
        team[x].append((team[x][0].lol_mmr + team[x][1].lol_mmr + team[x][2].lol_mmr + team[x][3].lol_mmr + team[x][4].lol_mmr) / 5)

    print('\n')



    for x in range(0, totalPlayers/5):
        print("\nTeam " + str(x) + ":")
        print('info: ' + team[x][0].lol_summoner_name + ' ' + str(team[x][0].lol_mmr))
        print('info: ' + team[x][1].lol_summoner_name + ' ' + str(team[x][1].lol_mmr))
        print('info: ' + team[x][2].lol_summoner_name + ' ' + str(team[x][2].lol_mmr))
        print('info: ' + team[x][3].lol_summoner_name + ' ' + str(team[x][3].lol_mmr))
        print('info: ' + team[x][4].lol_summoner_name + ' ' + str(team[x][4].lol_mmr))
        print("Avg MMR: " + str(team[x][5]) + "\n")

    print('Avg MMR: ' + str(avgMMR))

    millis = int(round(time.time() * 1000))
    print('Time Start: ', millis)

    for player in range(0, 5):
        for i in team:
            for x in team:
                if (i == x):
                    break
                team1swapavg = ((i[5]*5)-i[player].lol_mmr+x[player].lol_mmr)/5
                team2swapavg = ((x[5]*5)-x[player].lol_mmr+i[player].lol_mmr)/5
                if(abs(team1swapavg - avgMMR) < abs(i[5] - avgMMR) and abs(team2swapavg - avgMMR) < abs(x[5] - avgMMR)):
                    temp = i[player]
                    i[player] = x[player]
                    x[player] = i[player]
                    i[5] = team1swapavg
                    x[5] = team2swapavg

    millis2 = int(round(time.time() * 1000))
    print('End Time: ', millis2)
    print('Total Time: ', millis2-millis)

    for x in range(0, totalPlayers/5):
        print("\nTeam " + str(x) + ":")
        print('info: ' + str(team[x][0].lol_mmr))
        print('info: ' + str(team[x][1].lol_mmr))
        print('info: ' + str(team[x][2].lol_mmr))
        print('info: ' + str(team[x][3].lol_mmr))
        print('info: ' + str(team[x][4].lol_mmr))
        print("Team Avg MMR: " + str(team[x][5]) + "\n")

    print('Total Avg MMR: ' + str(avgMMR))


    maxTeam = 1
    minTeam = 2
    counter = 0
    for t in team:
        if t[5] > team[maxTeam][5]:
            maxTeam = counter

        if t[5] < team[minTeam][5]:
            minTeam = counter
        counter += 1




    """while (team[maxTeam][5]) > avgMMR:
        if (team[maxTeam][2].lol_mmr - team[minTeam][2].lol_mmr) > 100:
                maxMid = team[maxTeam][2]
                minMid = team[minTeam][2]
                team[maxTeam][2].replace( minMid)
                team[minTeam][2].replace( maxMid)
        elif (team[maxTeam][1].lol_mmr - team[minTeam][1].lol_mmr) > 100:
                maxJun = team[maxTeam][1]
                minJun = team[minTeam][1]
                team[maxTeam][1] .replace(minJun)
                team[minTeam][1].replace( maxJun)
        elif (team[maxTeam][0].lol_mmr - team[minTeam][0].lol_mmr) > 100:
                maxTop = team[maxTeam][0]
                minTop = team[minTeam][0]
                team[maxTeam][0].replace( minTop)
                team[minTeam][0].replace(maxTop)
        elif (team[maxTeam][3].lol_mmr - team[minTeam][3].lol_mmr) > 100:
                maxADC = team[maxTeam][3]
                minADC = team[minTeam][3]
                team[maxTeam][3].replace( minADC)
                team[minTeam][3].replace(maxADC)
        elif (team[maxTeam][4].lol_mmr - team[minTeam][4].lol_mmr) > 100:
                maxSup = team[maxTeam][4]
                minSup = team[minTeam][4]
                team[maxTeam][4].replace( minSup)
                team[minTeam][4].replace(maxSup)"""

    print("\nTeam MAX " + str(maxTeam) + ":")
    print('info: ' + str(team[maxTeam][0].lol_mmr))
    print('info: ' + str(team[maxTeam][1].lol_mmr))
    print('info: ' + str(team[maxTeam][2].lol_mmr))
    print('info: ' + str(team[maxTeam][3].lol_mmr))
    print('info: ' + str(team[maxTeam][4].lol_mmr))
    print('Max = team ' + str(maxTeam) + ' MMR: ' + str((
                                                        team[maxTeam][0].lol_mmr + team[maxTeam][1].lol_mmr + team[maxTeam][2].lol_mmr +
                                                        team[maxTeam][3].lol_mmr + team[maxTeam][4].lol_mmr) / 5))

    print("\nTeam MIN " + str(minTeam) + ":")
    print('info: ' + str(team[minTeam][0].lol_mmr))
    print('info: ' + str(team[minTeam][1].lol_mmr))
    print('info: ' + str(team[minTeam][2].lol_mmr))
    print('info: ' + str(team[minTeam][3].lol_mmr))
    print('info: ' + str(team[minTeam][4].lol_mmr))
    print('Min = team ' + str(minTeam) + ' MMR: ' + str((
                                                        team[minTeam][0].lol_mmr + team[minTeam][1].lol_mmr + team[minTeam][2].lol_mmr +
                                                        team[minTeam][3].lol_mmr + team[minTeam][4].lol_mmr) / 5))
    counter_t = 0
    counter_p = 0

    teams_model_list = []
    for t in range(0, len(team)):
        temp_team = Team.objects.create(team_name=" Team Name")
        team_mmr = 0
        for p in range(0, 5):
            temp_team.members.add(team[t][p])
            print team[t][p].lol_mmr
            team_mmr += int(team[t][p].lol_mmr)
        temp_team.ranking = int(team_mmr/5)
        temp_team.save()
        teams_model_list.append(temp_team)

    teams_model_list.sort(key=lambda x: x.ranking, reverse=True)
    counter = 1

    for team in teams_model_list:
        team.team_name = "Team Number " + str(counter)
        counter += 1
        team.save()

    sub_team = Team.objects.create(team_name="Substitutes")
    for sub in subs:
        print(str(sub.lol_mmr))
        sub_team.members.add(sub)
    sub_team.save()
    teams_model_list.append(sub_team)



    return teams_model_list
