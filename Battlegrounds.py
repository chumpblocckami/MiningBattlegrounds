#abbiamo 4 minion
import random
import copy
import pandas as pd

minions = {"Gatto":{"atk":1,"def":1},
           "Porco":{"atk":3,"def":1},
           "Iena":{"atk":2,"def":2},
           "Murloc":{"atk":2,"def":1},
           "Demon":{"atk":1,"def":1}}

feature_1 = []
feature_2 = []
target = []
who_started = []
battlegrounds_me_real = []
battlegrounds_oppo_real = []

n_simulations = 200

for simulation in range(0,n_simulations):
  battlegrounds_me = copy.deepcopy(battlegrounds_me_real)
  battlegrounds_oppo = copy.deepcopy(battlegrounds_oppo_real)

  #random populate
  for n,i in enumerate(range(0,6)):
    battlegrounds_me.append((n,list(minions.keys())[round(random.uniform(0,len(minions.keys()))-1)]))
    battlegrounds_oppo.append((n,list(minions.keys())[round(random.uniform(0,len(minions.keys()))-1)]))

  feature_1.append(copy.deepcopy(battlegrounds_me))
  feature_2.append(copy.deepcopy(battlegrounds_oppo))

  #attack
  last_man_standing = False
  n_attacker = 0
  last_attacker = round(random.uniform(1,2))
  board = [battlegrounds_me,battlegrounds_oppo]
  who_started.append(0 if last_attacker%2==0 else 1)

  print("-"*10,"MATCH ",simulation,"-"*10)
  while last_man_standing==False:
    first_attacker = board[0] if last_attacker%2==0 else board[1]
    second_attacker = board[1] if last_attacker%2==0 else board[0]
    #assert first_attacker != second_attacker
    last_attacker = last_attacker+1
    print(first_attacker, second_attacker)

    if n_attacker < len(first_attacker):
      attacking_index, attacking_minion = first_attacker[0+n_attacker]
    else:
      attacking_index, attacking_minion = first_attacker[0]
      n_attacker = 0
    defending_index, defending_minion = second_attacker[round(random.uniform(0,len(second_attacker)-1))]
    #print(attacking_index,attacking_minion,defending_index,defending_minion)

    attacking_life = minions[attacking_minion]["def"] - minions[defending_minion]["atk"]
    defending_life = minions[defending_minion]["def"] - minions[attacking_minion]["atk"]
    #print(attacking_life,defending_life)

    if attacking_life <= 0:
      first_attacker.pop(first_attacker.index((attacking_index,attacking_minion)))
    if defending_life <= 0:
      second_attacker.pop(second_attacker.index((defending_index,defending_minion)))
    n_attacker += 1
    #print(first_attacker,second_attacker)

    if len(first_attacker)==0 or len(second_attacker)==0:
      last_man_standing = True

  winner = None
  if len(first_attacker)>0:
    winner = 1
  elif len(second_attacker)>0:
    winner = 2
  else:
    winner = 3
  print("FINISH",winner)
  target.append(winner)

pd.Series(target).value_counts()

data = pd.DataFrame()
for i in range(n_simulations):
  data = data.append(pd.DataFrame([x[1] for x in feature_1[i]]+[x[1] for x in feature_2[i]]).T)
data = data.reset_index().drop(columns=["index"])
data.head()

data = pd.DataFrame({col: data[col].astype('category').cat.codes for col in data}, index=data.index)
data["who_started"] = who_started