from random import randint
import time
 
class Player:
    MMR = 0
    Preference = 0
    Preference2 = 0
 
    def __init__(self):
        self.Preference = randint(1, 5)
 
        self.Preference2 = randint(1, 5)


        rank = randint(0, 10000)
        if(rank <= 3):
            self.MMR = randint(2900, 3200)
        elif(rank <= 8):
            self.MMR = randint(2550, 2899)
        elif(rank <= 168):
            self.MMR = randint(2200, 2549)
        elif(rank <= 803):
            self.MMR = randint(1850, 2199)
        elif(rank <= 2403):
            self.MMR = randint(1500, 1849)
        elif(rank <= 6144):
            self.MMR = randint(1150, 1499)
        elif(rank <= 10000):
            self.MMR = randint(0, 1145)


        while (self.Preference2 == self.Preference):
            self.Preference2 = randint(1, 5)
 
 
List = []
totalMMR = 0
totalPlayers = 0
for x in range(1, 101):
    List.append(Player())
    totalMMR += List[x - 1].MMR
    totalPlayers += 1
avgMMR = totalMMR / 100
maxPlayersPerPref = int(len(List) / 5)
print('max playersperpref = ' + str(maxPlayersPerPref))
# list is indexed 0-99
 
p1 = []
p2 = []
p3 = []
p4 = []
p5 = []
subs = []
for x in range(0, 100):
    if List[x].Preference == 1 and len(p1) < maxPlayersPerPref:
        p1.append(List[x])
    elif List[x].Preference == 2 and len(p2) < maxPlayersPerPref:
        p2.append(List[x])
    elif List[x].Preference == 3 and len(p3) < maxPlayersPerPref:
        p3.append(List[x])
    elif List[x].Preference == 4 and len(p4) < maxPlayersPerPref:
        p4.append(List[x])
    elif List[x].Preference == 5 and len(p5) < maxPlayersPerPref:
        p5.append(List[x])
 
    elif List[x].Preference2 == 1 and len(p1) < maxPlayersPerPref:
        p1.append(List[x])
    elif List[x].Preference2 == 2 and len(p2) < maxPlayersPerPref:
        p2.append(List[x])
    elif List[x].Preference2 == 3 and len(p3) < maxPlayersPerPref:
        p3.append(List[x])
    elif List[x].Preference2 == 4 and len(p4) < maxPlayersPerPref:
        p4.append(List[x])
    elif List[x].Preference2 == 5 and len(p5) < maxPlayersPerPref:
        p5.append(List[x])
 
    elif len(p1) < maxPlayersPerPref:
        p1.append(List[x])
    elif len(p2) < maxPlayersPerPref:
        p2.append(List[x])
    elif len(p3) < maxPlayersPerPref:
        p3.append(List[x])
    elif len(p4) < maxPlayersPerPref:
        p4.append(List[x])
    elif len(p5) < maxPlayersPerPref:
        p5.append(List[x])
 
    else:
        subs.append(List[x])
 
print('\nPref 1 = ' + str(len(p1)))
counter = 1
for i in p1:
    print(str(counter) + ' ' + str(i.MMR))
    counter += 1
print('\nPref 2 = ' + str(len(p2)))
counter = 1
for i in p2:
    print(str(counter) + ' ' + str(i.MMR))
    counter += 1
print('\nPref 3 = ' + str(len(p3)))
counter = 1
for i in p3:
    print(str(counter) + ' ' + str(i.MMR))
    counter += 1
print('\nPref 4 = ' + str(len(p4)))
counter = 1
for i in p4:
    print(str(counter) + ' ' + str(i.MMR))
    counter += 1
print('\nPref 5 = ' + str(len(p5)))
counter = 1
for i in p5:
    print(str(counter) + ' ' + str(i.MMR))
    counter += 1
 
team = []
 
# balance preferences
 
print('Teams:\n')
 
for x in range(0, 20):
    team.append([])
    team[x].append(p1.pop(0))
    team[x].append(p2.pop(0))
    team[x].append(p3.pop(0))
    team[x].append(p4.pop(0))
    team[x].append(p5.pop(0))
    team[x].append((team[x][0].MMR + team[x][1].MMR + team[x][2].MMR + team[x][3].MMR + team[x][4].MMR) / 5)
 
print('\n')


 
for x in range(0, 20):
    print("\nTeam " + str(x) + ":")
    print('info: ' + str(team[x][0].MMR))
    print('info: ' + str(team[x][1].MMR))
    print('info: ' + str(team[x][2].MMR))
    print('info: ' + str(team[x][3].MMR))
    print('info: ' + str(team[x][4].MMR))
    print("Avg MMR: " + str(team[x][5]) + "\n")
 
print('Avg MMR: ' + str(avgMMR))

millis = int(round(time.time() * 1000))
print('Time Start: ', millis)

for player in range(0, 5):
    for i in team:
        for x in team:
            if (i == x):
                break
            team1swapavg = ((i[5]*5)-i[player].MMR+x[player].MMR)/5
            team2swapavg = ((x[5]*5)-x[player].MMR+i[player].MMR)/5
            if(abs(team1swapavg - avgMMR) < abs(i[5] - avgMMR) and abs(team2swapavg - avgMMR) < abs(x[5] - avgMMR)):
                temp = i[player]
                i[player] = x[player]
                x[player] = i[player]
                i[5] = team1swapavg
                x[5] = team2swapavg

millis2 = int(round(time.time() * 1000))
print('End Time: ', millis2)
print('Total Time: ', millis2-millis)

for x in range(0, 20):
    print("\nTeam " + str(x) + ":")
    print('info: ' + str(team[x][0].MMR))
    print('info: ' + str(team[x][1].MMR))
    print('info: ' + str(team[x][2].MMR))
    print('info: ' + str(team[x][3].MMR))
    print('info: ' + str(team[x][4].MMR))
    print("Avg MMR: " + str(team[x][5]) + "\n")
 
print('22Avg MMR: ' + str(avgMMR))


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
    if (team[maxTeam][2].MMR - team[minTeam][2].MMR) > 100:
            maxMid = team[maxTeam][2]
            minMid = team[minTeam][2]
            team[maxTeam][2].replace( minMid)
            team[minTeam][2].replace( maxMid)
    elif (team[maxTeam][1].MMR - team[minTeam][1].MMR) > 100:
            maxJun = team[maxTeam][1]
            minJun = team[minTeam][1]
            team[maxTeam][1] .replace(minJun)
            team[minTeam][1].replace( maxJun)
    elif (team[maxTeam][0].MMR - team[minTeam][0].MMR) > 100:
            maxTop = team[maxTeam][0]
            minTop = team[minTeam][0]
            team[maxTeam][0].replace( minTop)
            team[minTeam][0].replace(maxTop)
    elif (team[maxTeam][3].MMR - team[minTeam][3].MMR) > 100:
            maxADC = team[maxTeam][3]
            minADC = team[minTeam][3]
            team[maxTeam][3].replace( minADC)
            team[minTeam][3].replace(maxADC)
    elif (team[maxTeam][4].MMR - team[minTeam][4].MMR) > 100:
            maxSup = team[maxTeam][4]
            minSup = team[minTeam][4]
            team[maxTeam][4].replace( minSup)
            team[minTeam][4].replace(maxSup)"""
 
print("\nTeam MAX " + str(maxTeam) + ":")
print('info: ' + str(team[maxTeam][0].MMR))
print('info: ' + str(team[maxTeam][1].MMR))
print('info: ' + str(team[maxTeam][2].MMR))
print('info: ' + str(team[maxTeam][3].MMR))
print('info: ' + str(team[maxTeam][4].MMR))
print('Max = team ' + str(maxTeam) + ' MMR: ' + str((
                                                    team[maxTeam][0].MMR + team[maxTeam][1].MMR + team[maxTeam][2].MMR +
                                                    team[maxTeam][3].MMR + team[maxTeam][4].MMR) / 5))
 
print("\nTeam MIN " + str(minTeam) + ":")
print('info: ' + str(team[minTeam][0].MMR))
print('info: ' + str(team[minTeam][1].MMR))
print('info: ' + str(team[minTeam][2].MMR))
print('info: ' + str(team[minTeam][3].MMR))
print('info: ' + str(team[minTeam][4].MMR))
print('Min = team ' + str(minTeam) + ' MMR: ' + str((
                                                    team[minTeam][0].MMR + team[minTeam][1].MMR + team[minTeam][2].MMR +
                                                    team[minTeam][3].MMR + team[minTeam][4].MMR) / 5))