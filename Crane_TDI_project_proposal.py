import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

df2020 = pd.read_csv('pbp-2020.csv')


teams =['BUF','MIA','NE','NYJ','BAL','CIN','CLE','PIT','HOU','IND',\
    'JAX','TEN','DEN','KC','LAC','LV','DAL','NYG','PHI','WAS','CHI',\
        'DET','GB','MIN','ATL','CAR','NO','TB','ARI','LA','SEA','SF']

team_wins_2020 = {'BUF':13,'MIA':10,'NE':7,'NYJ':2,'BAL':11,'CIN':4.5,\
    'CLE':11,'PIT':12,'HOU':4,'IND':11,'JAX':1,'TEN':11,'DEN':5,'KC':14,\
        'LAC':7,'LV':8,'DAL':6,'NYG':6,'PHI':4.5,'WAS':7,'CHI':8,\
        'DET':5,'GB':13,'MIN':7,'ATL':4,'CAR':5,'NO':12,'TB':11,'ARI':8,\
            'LA':10,'SEA':12,'SF':6}


def comp_pct_by_tm():
    comp_pct_dict={}
    for team in teams:
        pass_plays = len(df2020[(df2020['OffenseTeam']==team) & (df2020['IsPass']==1)].index)
        pass_comps = len(df2020[(df2020['OffenseTeam']==team) & (df2020['IsPass']==1) & (df2020['IsIncomplete']==0)].index)
        #print(pass_plays)
        #print(team)
        comp_pct_dict[team]=pass_comps/pass_plays
    return comp_pct_dict

p1=0
if p1==1:

    comp_pct_dict = comp_pct_by_tm()
    # Scatter Plot of comp_pct vs wins.
    plt.scatter(list(comp_pct_dict.values()),list(team_wins_2020.values()),s=15)
    for i, txt in enumerate(teams):
        plt.annotate(txt, (list(comp_pct_dict.values())[i], list(team_wins_2020.values())[i]),fontsize=7)
    plt.xlim(0.50,0.75)
    plt.ylim(0,16)
    plt.title('NFL Team Completion Percentage vs Wins (2020)')
    plt.xlabel('Completion Percentage')
    plt.ylabel('Wins in 2020')
    plt.show()
    


def comp_pct_by_tm4():
    comp_pct_dict={}
    for team in teams:
        pass_plays = len(df2020[(df2020['OffenseTeam']==team) & (df2020['IsPass']==1) & (df2020['Quarter']==4)].index)
        pass_comps = len(df2020[(df2020['OffenseTeam']==team) & (df2020['IsPass']==1) & (df2020['IsIncomplete']==0)& (df2020['Quarter']==4)].index)
        comp_pct_dict[team]=pass_comps/pass_plays
    return comp_pct_dict

# Scatter Plot of comp-pct in 4th quarter vs wins 
p2=1
if p2==1:
    comp_pct_dict4 = comp_pct_by_tm4()
    # Scatter Plot of comp_pct vs wins.
    plt.scatter(list(comp_pct_dict4.values()),list(team_wins_2020.values()),s=15)
    for i, txt in enumerate(teams):
        plt.annotate(txt, (list(comp_pct_dict4.values())[i], list(team_wins_2020.values())[i]),fontsize=7)
    plt.xlim(0.50,0.75)
    plt.ylim(0,16)
    plt.title('NFL Team Completion Percentage in 4th Quarter vs Wins (2020)')
    plt.xlabel('Completion Percentage (4th Quarter)')
    plt.ylabel('Wins in 2020')
    plt.show()

def comp_pct_by_tm_2min():
    comp_pct_dict={}
    for team in teams:
        pass_plays = len(df2020[(df2020['OffenseTeam']==team) & (df2020['IsPass']==1) & (df2020['Quarter']==4) & (df2020['Minute']<=3)].index)
        pass_comps = len(df2020[(df2020['OffenseTeam']==team) & (df2020['IsPass']==1) & (df2020['IsIncomplete']==0) & (df2020['Quarter']==4) & (df2020['Minute']<=3)].index)
        comp_pct_dict[team]=pass_comps/pass_plays
    return comp_pct_dict

# Scatter Plot of comp-pct in 4th quarter vs wins 
p3=0
if p3==1:
    comp_pct_dict_xmin = comp_pct_by_tm_2min()
    # Scatter Plot of comp_pct vs wins.
    plt.scatter(list(comp_pct_dict_xmin.values()),list(team_wins_2020.values()),s=15)
    for i, txt in enumerate(teams):
        plt.annotate(txt, (list(comp_pct_dict_xmin.values())[i], list(team_wins_2020.values())[i]),fontsize=7)
    plt.xlim(0.50,0.90)
    plt.ylim(0,16)
    plt.title('NFL Team Completion Percentage in Final 3 minutes of game (2020)')
    plt.xlabel('Completion Percentage (3 mins left in game)')
    plt.ylabel('Wins in 2020')
    plt.show()