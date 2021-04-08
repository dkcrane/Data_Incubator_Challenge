import numpy as np
import pandas as pd

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

df2020 = pd.read_csv('pbp-2020.csv')

def isNaN(string):
    return string != string

comp_pct_weight=1
int_weight = -0.09
fum_weight = -0.06
pen_weight = -0.005
turnover_diff_weight = 0


teams =['BUF','MIA','NE','NYJ','BAL','CIN','CLE','PIT','HOU','IND',\
    'JAX','TEN','DEN','KC','LAC','LV','DAL','NYG','PHI','WAS','CHI',\
        'DET','GB','MIN','ATL','CAR','NO','TB','ARI','LA','SEA','SF']

team_wins_2020 = {'BUF':13,'MIA':10,'NE':7,'NYJ':2,'BAL':11,'CIN':4.5,\
    'CLE':11,'PIT':12,'HOU':4,'IND':11,'JAX':1,'TEN':11,'DEN':5,'KC':14,\
        'LAC':7,'LV':8,'DAL':6,'NYG':6,'PHI':4.5,'WAS':7,'CHI':8,\
        'DET':5,'GB':13,'MIN':7,'ATL':4,'CAR':5,'NO':12,'TB':11,'ARI':8,\
            'LA':10,'SEA':12,'SF':6}
# Find Games by ID.
games = df2020.GameId.unique()

pred_team_wins_2020={}



for game in games:
    # Find data on individual game
    gamedf = df2020[df2020['GameId']==game]
    #find teams who played
    idx=1
    while (isNaN(list(gamedf['OffenseTeam'])[idx])) | (isNaN(list(gamedf['DefenseTeam'])[idx])):
        idx+=1 # Some rows have no values for OffenseTeam and DefenseTeam (due to timeouts/ quarters ending and so on)
    team1 = list(gamedf['OffenseTeam'])[idx]
    team2 = list(gamedf['DefenseTeam'])[idx]

    team1_pts=0
    team2_pts=0
    
    # Find completion percentage
    team1pp = len(gamedf[(gamedf['OffenseTeam']==team1) & (gamedf['IsPass']==1)].index)
    team2pp = len(gamedf[(gamedf['OffenseTeam']==team2) & (gamedf['IsPass']==1)].index)

    team1pc = len(gamedf[(gamedf['OffenseTeam']==team1) & (gamedf['IsPass']==1) & (gamedf['IsIncomplete']==0)].index)
    team2pc = len(gamedf[(gamedf['OffenseTeam']==team2) & (gamedf['IsPass']==1)  & (gamedf['IsIncomplete']==0)].index)
    # Compute completion percentages
    comp_pct1=team1pc/team1pp
    comp_pct2=team2pc/team2pp

    team1_pts+=comp_pct_weight*comp_pct1
    team2_pts+=comp_pct_weight*comp_pct2

    # Interceptions, fumbles and penalties
    team1int = len(gamedf[(gamedf['OffenseTeam']==team1) & (gamedf['IsInterception']==1)].index)
    team1fum = len(gamedf[(gamedf['OffenseTeam']==team1) & (gamedf['IsFumble']==1)].index)

    team1pen = gamedf[(gamedf['IsPenaltyAccepted']==1) & (gamedf['PenaltyTeam']==team1)]
    team1pen_num = len(team1pen.index)
    team1pen_yards = team1pen['PenaltyYards'].sum()

    team2int = len(gamedf[(gamedf['OffenseTeam']==team2) & (gamedf['IsInterception']==1)].index)
    team2fum = len(gamedf[(gamedf['OffenseTeam']==team2) & (gamedf['IsFumble']==1)].index)
    team2pen = len(gamedf[(gamedf['IsPenaltyAccepted']==1) & (gamedf['PenaltyTeam']==team2)].index)

    team2pen = gamedf[(gamedf['IsPenaltyAccepted']==1) & (gamedf['PenaltyTeam']==team2)]
    team2pen_num = len(team2pen.index)
    team2pen_yards = team2pen['PenaltyYards'].sum()
    
    # Penalize teams for INTs, fumbles, penalty yards.
    team1_pts+=(int_weight)*team1int+(fum_weight)*team1fum + (pen_weight)*team1pen_yards + turnover_diff_weight*((team2int+team2fum)-(team1int+team1fum))
    team2_pts+=(int_weight)*team2int+(fum_weight)*team2fum + (pen_weight)*team2pen_yards + turnover_diff_weight*((team1int+team1fum)-(team2int+team2fum))


    # Decide who wins
    if team1_pts>team2_pts:
        team1_win = 1
        team2_win = 0
    elif team2_pts>team1_pts:
        team1_win = 0
        team2_win = 1
    else:
        team1_win = 0.5
        team2_win = 0.5
    
    # Add win to teams dictionary
    if team1 in pred_team_wins_2020:
        pred_team_wins_2020[team1][1]+=team1_win
    else:
        pred_team_wins_2020[team1]=[team_wins_2020[team1],team1_win]
    
    if team2 in pred_team_wins_2020:
        pred_team_wins_2020[team2][1] += team2_win
    else:
        pred_team_wins_2020[team2]=[team_wins_2020[team2],team2_win]

#print(sum(list(pred_team_wins_2020.values())))
print(pred_team_wins_2020)  

show_plots=1
if show_plots==1:
    pred_wins=[]
    actual_wins=[]
    err_vec=[]
    for keys in pred_team_wins_2020:
        a= pred_team_wins_2020[keys][1]
        b=pred_team_wins_2020[keys][0]
        pred_wins.append(a)
        actual_wins.append(b)
        err_vec.append((a-b)**2/2)

    # Scatter Plot of predicted wins vs actual wins.
    plt.figure()
    plt.scatter(pred_wins,actual_wins,s=15)
    for i, txt in enumerate(pred_team_wins_2020.keys()):
        plt.annotate(txt, (pred_wins[i], actual_wins[i]),fontsize=7)
    plt.plot([0, 16], [0, 16], 'k-', color = 'r')
    plt.text(13, 0.5, 'Error: = %0.2f' % sum(err_vec))
    plt.xlim(0,16)
    plt.ylim(0,16)
    plt.title('NFL Teams Predicted Wins vs Actual Wins (2020)')
    plt.xlabel('Predicted Wins')
    plt.ylabel('Actual Wins')
    plt.show()
    


