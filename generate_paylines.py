from enum import Enum
import random
import numpy as np
import json
import csv
from MaleFunkcije import *


target_symbol_frequencies = {
    Reels.ORANGE: None,
    Reels.APPLE: None,
    Reels.GRAPE: None,
    Reels.STRAWBERRY: None,
    Reels.MANGO: None,
    Reels.BANNANA: None,
    Reels.CHERY: None,
    Reels.LEMON: None,
    Reels.SEVENS: None,
    Reels.BONUS: None,
    Reels.WILD: None,
    Reels.MULTIPLAIER: None,

    }

reel = [Reels.ORANGE,Reels.APPLE,Reels.GRAPE,Reels.STRAWBERRY,
         Reels.MANGO,Reels.BANNANA,Reels.CHERY,Reels.LEMON,Reels.SEVENS,
         Reels.BONUS, Reels.MULTIPLAIER, Reels.WILD]

paylines = [
    [0,1,2,3,4],
    [5,6,7,8,9],
    [10,11,12,13,14],
    [15,16,17,18,19],
    [20,21,22,23,24],
    [0,5,10,15,20],
    [1,6,11,16,21],
    [2,7,12,17,22],
    [3,8,13,18,23],
    [4,9,14,19,24],
    ##dijagonale
    [0,6,12,18,24],
    [4,8,12,16,20],
    ##kvadrati
    [0,1,5,6],
    [1,6,2,7],
    [2,7,3,8],
    [3,4,8,9],
    [5,6,10,11],[6,7,11,12],[7,8,12,13],[8,9,13,14],
    [10,11,15,16],[11,12,16,17],[12,13,17,18],[13,14,18,19],
    [15,16,20,21],[16,17,21,22],[17,18,22,23],[18,19,23,24]
]


def find_winners(mapa,payline,spin):
    winners = []
    bonus_spin = 0
    if len(payline) == 4:
        if(len(mapa) == 1):
            for keys in mapa.keys():
                kljuc = keys
                if(kljuc == Reels.BONUS):
                    bonus_spin +=4
                    winners.append([spin,convert_to_name(kljuc),payline,"kvadrat","bonus",bonus_spin])
                if(kljuc != Reels.MULTIPLAIER and kljuc != Reels.WILD):
                    winners.append([spin,convert_to_name(kljuc), payline,"kvadrat","bonus",bonus_spin])
        elif len(mapa) == 2 and Reels.MULTIPLAIER in mapa.keys():
            for keys in mapa.keys():
                if(keys != Reels.MULTIPLAIER):
                    kljuc = keys
                    if kljuc == Reels.BONUS:
                        bonus_spin +=1
                    winners.append([spin,convert_to_name(kljuc), payline,"kvadrat", 'bonus',bonus_spin,"multi", mapa[Reels.MULTIPLAIER]])
        elif len(mapa) == 2 and Reels.WILD in mapa.keys():
           for keys in mapa.keys():
                if(keys != Reels.WILD):
                    kljuc = keys
                    if(kljuc == Reels.BONUS):
                        bonus_spin +=1
                    winners.append([spin,convert_to_name(kljuc), payline,"kvadrat",'bonus',bonus_spin])
    else:
        if(len(mapa) == 1):
            for keys in mapa.keys():
                kljuc = keys
                if kljuc == Reels.BONUS:
                    bonus_spin += 20
                winners.append([spin,convert_to_name(kljuc), payline,"linija",5,"bonus",bonus_spin])
        elif len(mapa) == 2 and Reels.MULTIPLAIER in mapa.keys():
            for keys in mapa.keys():
                if(keys != Reels.MULTIPLAIER):
                    kljuc = keys
                    winners.append([spin,convert_to_name(kljuc), payline, "linija", mapa[kljuc] ,'bonus',bonus_spin,"multi", mapa[Reels.MULTIPLAIER]])
        elif len(mapa) == 2 and Reels.WILD in mapa.keys():
           for keys in mapa.keys():
                if(keys != Reels.WILD and keys != Reels.BONUS):
                    kljuc = keys
                    winners.append([spin,convert_to_name(kljuc), payline,"linija", mapa[kljuc]+mapa[Reels.WILD],'bonus',bonus_spin])
        elif len(mapa) == 2 :
            for keys in mapa.keys():
                if (mapa[keys] == 4 or mapa[keys] == 3):
                    kljuc = keys
                    if(Reels.BONUS in mapa.keys()):
                        bonus_spin +=1
                    winners.append([spin,convert_to_name(kljuc),payline, "linija",mapa[kljuc] ,'bonus',bonus_spin])
        elif len(mapa) == 3:
            for keys in mapa.keys():
                if mapa[keys] == 3 and (keys != Reels.MULTIPLAIER) and (keys != Reels.WILD) and (keys != Reels.BONUS):
                    kljuc = keys
                    if(Reels.BONUS in mapa.keys()):
                        bonus_spin += 1
                    winners.append([spin,convert_to_name(kljuc),payline,"linija", mapa[kljuc] ,'bonus',bonus_spin])

    return winners


def modify_winners(wins,multiplayer):
    lists = []
    for win in wins:
        list = []
        list.append(win[0])
        list.append(win[1])
        list.append(win[2])
        duzina = 0
        bonus = 0
        multi = 0
        if(win[3] == "linija"):
            duzina += win[4]
        else:
            duzina += 4
        if(win[5] == "bonus"):
            bonus +=win[6]
        if(len(win) > 7):
            if(win[7] == 'multi'):
                multi += win[8]
        if(win[1] == 'Bonus'):
            list.append(bonus)
            list.append(bonus+1)
        elif(win[1] == 'Multiplaier'):
            continue
        elif(win[1] == 'Wild'):
            continue
        else:
            list.append(round(multiplayer[convert_to_Enum(win[1])] ** (duzina/2),2))
            list.append(bonus)
        lists.append(list)
    return lists

            

def call_diff_freq(num_spins,symbol_freq, symbol_mult):
    symbol_frequencies = {symbol: 0 for symbol in Reels}
    dataset = []
    for r in range(num_spins):
        spin_outcome = []
        for reel in range(25):
            symbol = select_symbol(symbol_freq)
            spin_outcome.append(symbol)
            symbol_frequencies[symbol] += 1
        wins = []
        win = []
        for payline in paylines:
            symbols_on = {}
            for i in payline:
                if(spin_outcome[i] in symbols_on.keys()):
                    symbols_on[spin_outcome[i]] += 1
                else:
                    symbols_on[spin_outcome[i]] = 1
            potentional_wins = find_potential_wins(symbols_on)
            if potentional_wins != 0:
                wins = find_winners(potentional_wins, payline,r)
                if(len(wins) != 0):
                    win.append(modify_winners(wins,symbol_mult))
        if(len(win) != 0):
            for i in win:
                for j in i:
                    dataset.append(j)

    #dataset.append("R")
    #real_freq = {convert_to_name(symbol): symbol_freq[symbol]*100 for symbol in symbol_freq}
    #dataset.append(real_freq.keys())
    #dataset.append(real_freq.values())
    #dataset.append("O")
    observed_symbol_frequencies = {convert_to_name(symbol): symbol_frequencies[symbol] / num_spins for symbol in symbol_frequencies}
    #dataset.append(observed_symbol_frequencies.keys())
    #dataset.append(observed_symbol_frequencies.values())
    #observed = {}
    ##for symbol,val in symbol_mult.items():
    ##   observed[convert_to_name(symbol)] = val
    #dataset.append("M")
    #dataset.append(observed.keys())
    #dataset.append(observed.values())

    bonus_inf = observed_symbol_frequencies
    return dataset,bonus_inf

## Obrada 

def calculate_volatility(dataset,spins):
    cnt = 1
    last_i = 0
    cnt_in_spin = 0
    full = 0
    for i in dataset:
        if i[0] == last_i:
            cnt_in_spin += 1
        else:
            full += cnt_in_spin
            cnt_in_spin = 1
            cnt+= 1
            last_i = i[0]
    print( full, cnt)
    return full/spins, cnt/spins

def calculate_rtp(dataset):
    rtp = 0
    cnt = 0
    bonuses = 0
    line = 0
    ## 2,Mango,"[17, 18, 22, 23]",2.36,0
    for spin in dataset:
        if(spin[1] != "Wild" and spin[1] != 'Bonus'):
            price = payouts[convert_to_Enum(spin[1])] * spin[3]
            rtp += price
            cnt += 1
            print("Sta je ovde "+ str(spin[4]))
        if(len(spin) > 5):
            print('Obaj mora bolje ' + str(spin))

    return rtp/cnt

def add_into_list(list,map):

    for i in map.values():
        list.append(i)
    return list

def analyze_spin_data(data,spins,freq,payouts):
    total_spins = spins
    total_wins = 0
    spin_win = 1
    last_spin = 0
    total_payout = 0
    total_bonus_spins = 0
    symbol_frequency = {}
    for row in data:
            spin_number = int(row[0])
            if (spin_number != last_spin):
                last_spin = spin_number
                spin_win += 1
            symbol = row[1]
            payline = row[2]
            payout_multiplier = float(row[3])
            bonus_spins = int(row[4])
            if payout_multiplier > 0:
                total_wins += 1
                total_payout += payout_multiplier

            total_bonus_spins += bonus_spins

            # Update symbol frequency count
            if symbol in symbol_frequency:
                symbol_frequency[symbol] += 1
            else:
                symbol_frequency[symbol] = 1

    average_payout = total_payout / total_wins if total_wins > 0 else 0
    bonus_spin_percentage = (total_bonus_spins / total_spins) * 100 if total_spins > 0 else 0
    volatility = spin_win / total_spins * 100
    # Print the analysis results
    print("Total Spins:", total_spins)
    print("Total Wins:", total_wins)
    print("Spin wins: ", volatility)
    print("Total Payout:", total_payout)
    print("Average Payout:", average_payout)
    print("Total Bonus Spins:", total_bonus_spins)
    print("Bonus Spin Percentage:", bonus_spin_percentage)

    print("Symbol Frequency:")
    for symbol, frequency in symbol_frequency.items():
        print(symbol, "-", frequency)
    
    final_data = []
    final_data.append(total_spins)
    final_data.append(total_wins)
    final_data.append(volatility)
    final_data.append(total_payout)
    final_data.append(average_payout)
    final_data.append(total_bonus_spins)
    final_data.append(bonus_spin_percentage)
    final_data = add_into_list(final_data,freq)
    final_data = add_into_list(final_data,payouts)
    return final_data

all_data = [["total_spins",
                "total_wins",
                "volitily",
                "total_payout",
                "avg_payout",
                "total_bonus_spins",
                "bonus_spin_prec",
                "freq_Orange",
                "freq_Apple",
                "freq_Grape",
                "freq_Strawberry",
                "freq_Mango",
                "freq_Banana",
                "freq_Cherry",
                "freq_Lemon",
                "freq_Seven",
                "freq_Bonus",
                "freq_Multiplier",
                "freq_Wild",
                "multi_Orange",
                "multi_Apple",
                "multi_Grape",
                "multi_Strawberry",
                "multi_Mango",
                "multi_Banana",
                "multi_Cherry",
                "multi_Lemon",
                "multi_Seven",
                "multi_Bonus"
    ]]
  
for i in range(1,10):
    number_of_spins = 1500
    target_symbol_frequencies = generate_random_frequncy(target_symbol_frequencies)
    
    payouts = generate_payouts()
    print(payouts)
    dataset,observed_freq = call_diff_freq(number_of_spins,target_symbol_frequencies,payouts)
    ##rtp = calculate_rtp(dataset,payouts)  
    all_data.append(analyze_spin_data(dataset,number_of_spins,target_symbol_frequencies,payouts))

create_csv_file(all_data,"wtf.csv")