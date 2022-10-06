import csv
import sqlite3
from sqlite3 import Error
import traceback

class dbConnection():
    def __init__(self,path):
        self.path = path
    def connect(self):
        connection = None
        try:
            connection = sqlite3.connect(self.path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

class Recepies():
    def __init__(self,recepies):
        self.recepies = recepies
    def alphaValues(self):
        userInput = [skladnik.strip().lower() for skladnik in input("Please provide ingredients (separate answers with comma): ").split(",")]
        if all(skladnik.replace(' ','').isalpha() for skladnik in userInput):
            return userInput

class UserIngredientsListCreation(Recepies):
    def __init__(self,recepies):
        super().__init__(recepies)
    def collectNameandIngredients(self):
        newIngredients = [{"Name":self.getSingleValues("Recipe"),"Ingredients":",".join(str(elem) for elem in self.alphaValues()),"Webpage":self.getSingleValues("Webpage")}]
        print(newIngredients)
    def getSingleValues(self,valueName:str):
        while True:
            try:
                recipeName = input("Please provide name of {name}: \n".format(name=valueName))
                if recipeName[0].isalpha():
                    return recipeName
                else:
                    print("Name must start with alphabetic characters only")
            except:
                print("Please provide input")
    def isWebpageAvailable(self):
        while True:
            isWebPageNeeded=input("Is there a webpage with this recipe? ('Y' for yes 'N' for no)")
            if isWebPageNeeded == "Y":
                return True
            elif isWebPageNeeded == "N":
                return False
            else:
                print("Please provide answer")
class UserIngredientsInput(Recepies):
    def __init__(self,recepies):
        super().__init__(recepies)
    def get_ingredients(self):
            return self.alphaValues()
    
    def assignPossibleRecepies(self,ingredients):  
        possibilities=self.countPossibilities(ingredients)
        print([x for x in possibilities if possibilities[x]>=4])
    def countPossibilities(self,ingredients):
        possibilities = {}
        for row in self.recepies:
            i=0
            for ans in ingredients:
                if ans in self.recepies[row][0]:
                    i+=1
                    possibilities.update({row:i})           
        return possibilities
    def recipeSearch(self):
        while True:
            getIngredients = self.get_ingredients()
            if len(getIngredients)<4:
                print("Please provide more then 4 ingredients")
            elif getIngredients:
                self.assignPossibleRecepies(getIngredients)
            else:
                print("Please provide alpha answers only")

def getFile():
    try:
        with open('przepisy.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            myDict={}
            for row in reader:
                myDict.update({row['Name']:[[skladnik.lower() for skladnik in row['Ingredients'].split(",")],row['Webpage']]})
        return myDict
    except Exception:
        traceback.print_exc()

def menuSelection():
    while True:
        chooseOptions = input("1.Search for possible recepies\n2.Add possible recepies\n3.Random recipe selection\n")
        try:
            int(chooseOptions)
            if chooseOptions == "1":
                t = UserIngredientsInput(getFile())
                getFile()
                t.recipeSearch()
            elif chooseOptions == "2":
                addRecipe = UserIngredientsListCreation(getFile())
                addRecipe.collectNameandIngredients()
        except:
            print("Please provide integer between 1-2")

if __name__ == "__main__":
    menuSelection()
        
        
