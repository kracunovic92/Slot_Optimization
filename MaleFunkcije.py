import csv
from enum import Enum
import random
import numpy as np
import json

class Reels(Enum):
    ORANGE = 1
    APPLE = 2
    GRAPE = 3
    STRAWBERRY = 4
    MANGO = 5
    BANNANA = 6
    CHERY = 7
    LEMON = 8
    SEVENS = 9
    BONUS = 10
    MULTIPLAIER = 11
    WILD = 12


def create_csv_file(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


def generate_random_frequncy(target_symbol_frequencies):
    symbols = target_symbol_frequencies.keys()
    frequencies = [random.uniform(0.001, 1) for _ in range(len(target_symbol_frequencies))]
    sevens_index = list(symbols).index(Reels.SEVENS)
    frequencies[sevens_index] = random.uniform(0.001, 0.05)
    ##frequencies = np.random.rand(len(target_symbol_frequencies))
    frequencies /= np.sum(frequencies)
    r = 0
    for i in target_symbol_frequencies.keys():
        target_symbol_frequencies[i] = frequencies[r]
        r = r+1
        

    return target_symbol_frequencies


def convert_to_Enum(name):
    if name == "Orange":
        return Reels.ORANGE
    if name == "Apple":
        return Reels.APPLE
    if name == "Grape":
        return Reels.GRAPE
    if name == "Strawberry":
        return Reels.STRAWBERRY
    if name == "Mango":
        return Reels.MANGO
    if name == "Banana":
        return Reels.BANNANA
    if name == "Cherry":
        return Reels.CHERY
    if name == "Lemon":
        return Reels.LEMON
    if name == "Seven":
        return Reels.SEVENS
    if name == "Bonus":
        return Reels.BONUS
    if name == 'Wild':
        return Reels.WILD
    
def convert_to_name(rel):
    if(rel == Reels.ORANGE):
        return 'Orange'
    if(rel == Reels.APPLE):
        return 'Apple'
    if(rel == Reels.GRAPE):
        return 'Grape'
    if(rel == Reels.STRAWBERRY):
        return 'Strawberry'
    if(rel == Reels.MANGO):
        return 'Mango'
    if(rel == Reels.BANNANA):
        return 'Banana'
    if(rel == Reels.CHERY):
        return 'Cherry'
    if(rel == Reels.LEMON):
        return 'Lemon'
    if(rel == Reels.SEVENS):
        return 'Seven'
    if(rel == Reels.BONUS):
        return 'Bonus'
    if(rel == Reels.MULTIPLAIER):
        return 'Multiplaier'
    if(rel == Reels.WILD):
        return 'Wild'
    
def find_potential_wins(mapa):
    res = 0
    for kljuc, vrednost in mapa.items():
        if vrednost >= 3:
            return mapa
    return  0


def generate_payouts():
    multipliers = {
        Reels.ORANGE: None,
        Reels.APPLE: None,
        Reels.GRAPE: None,
        Reels.STRAWBERRY: None,
        Reels.MANGO: None,
        Reels.BANNANA: None,
        Reels.CHERY: None,
        Reels.LEMON: None,
        Reels.SEVENS: None,
        Reels.BONUS:None

    }
    multipliers[Reels.SEVENS] = random.choice(range(5,15))
    symbols = [Reels.ORANGE, Reels.APPLE,
        Reels.GRAPE,
        Reels.STRAWBERRY,
        Reels.MANGO,
        Reels.BANNANA,
        Reels.CHERY,
        Reels.LEMON]
    for symbol in symbols:
        multipliers[symbol] = round(random.uniform(0.2,2),2)

    return multipliers

def select_symbol(target_symbol_frequencies):
    symbol_probabilities = [target_symbol_frequencies[symbol] for symbol in Reels]
    symbol = random.choices(list(Reels), weights=symbol_probabilities)[0]
    return symbol


