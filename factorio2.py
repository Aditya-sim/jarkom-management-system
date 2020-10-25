from fractions import Fraction as F
import json, os

separator = '\n'+'='*30
msgender = ':'*4
outbuffer = ''

conn = None

class RecipeItem:
    def __init__(self):
        pass

def strf(inp):
    f = F(inp)
    if f.denominator>5:
        return str(f)+' ('+str(float(round(f,5)))+')'
    return str(f)

class Recipe:

    name = ''
    ninput = {}
    output = {}
    
    def __init__(self, name, ingredient={}, product={}, recipe = None):
        if recipe:
            self = convertRecipe(recipe)
        else:
            self.name = name
            self.ninput = ingredient
            self.output = product

    def __str__(self,ct=1,expand=False):
        ingstr = ''
        for i in self.ninput:
            if expand: ingstr=ingstr + '\n'
            ingstr=ingstr+strf(self.ninput[i]*ct)+' '+i+' + '
        ingstr=ingstr.rstrip('+ ')
        if expand: ingstr=ingstr + '\n'
        ingstr=ingstr+' ==> '
        for i in self.output:
            if expand: ingstr=ingstr + '\n'
            ingstr=ingstr+strf(self.output[i]*ct)+' '+i+' + '
        ingstr=ingstr.rstrip('+ ')
        return ingstr

    def strme(self,ct=1,expand=False):
        return self.__str__(ct,expand)

def convertRecipe(recipe):
    ingredients = recipe['ingredients']
    products = recipe['products']
    outing = {}
    outpro = {}
    for item in ingredients:
        outing[item['name']] = item['amount']
    for item in products:
        if outpro.get(item['name']):
            outpro[item['name']] += getRealProduct(item)
        else:
            outpro[item['name']] = getRealProduct(item)
    return Recipe(recipe['name'], outing, outpro)

def getRealProduct(product):    
    prod = F(0,1)
    prob = F(1,1)
    if 'probability' in product:
        prob = F(str(product['probability']))
    if 'amount' in product:
        prod = F(product['amount'])*prob
    else:
        prod = F(F(product['amount_min']+product['amount_max']),2)*prob
    return prod


def runprogram(connection):
    conn = connection

    def nprint(strtoprint, prt = None):
        global outbuffer
        outbuffer = outbuffer + strtoprint + '\n'
        if prt:
            conn.sendall(str.encode(outbuffer))
            outbuffer = ''

    def ninput(inpstr):
        nprint(inpstr, True)
        return conn.recv(2048).decode('utf-8')
    
    
    rawdat = {}
    datpath = os.path.join('recipe-lister')
    datfiles = ['assembling-machine','fluid','furnace','item','recipe']

    nprint('Loading file...')
    for datfile in datfiles:
        with open(os.path.join(datpath,datfile+'.json')) as openfile:
            rawdat[datfile] = json.load(openfile)

    items = []
    recipes = {}
    ##craftcategory = {}

    ##Register recipes and items
    nprint('Registering recipes and items...')
    for recipe in rawdat['recipe']:
        if ('uncompress-' not in recipe) and ('rf-' not in recipe) and ('-barrel' not in recipe):
            convertedrecipe = convertRecipe(rawdat['recipe'][recipe])
            recipes[recipe] = convertedrecipe
            for product in convertedrecipe.output:
                if product not in items:
                    items.append(product)

    del rawdat ## Save memory

    runprogram = True
    stage = 0
    init = True
    
    while runprogram:

        if init:
        ##Stage 0: Select initial item(s)
            craftitems = {}
            selecteditem = ''
            inititems = {}
            init = False
            
        while stage == 0:
            iteminput = ninput(separator + '\nAdd initial item(s), enter 'proceed' to proceed:\n')
            if iteminput in items:
                amtinput = ninput('Item amount: ')
                try:
                    amt = F(amtinput)
                    inititems[iteminput] = amt
                except ValueError:
                    nprint('Invalid amount: '+amtinput)
            elif iteminput == 'proceed':
                stage = 1
                craftitems = dict(inititems)
            else:
                nprint('Invalid item: '+iteminput)

        ##Stage 1: Select item to breakdown, or finish breaking down
        while stage == 1:
            currentitems = {}
            currentcounter = 1
            selecteditem = ''
            nprint(separator)
            nprint('Select item to break down:')
            for item in sorted(craftitems.keys()):
                if craftitems[item] != 0:
                    nprint(str(currentcounter)+'. '+item+': '+strf(craftitems[item]))
                    currentitems[currentcounter] = item
                    currentcounter = currentcounter + 1
            selectindex = ninput('Enter index of item to break down (or enter 0 to finish): ')
            selectint = 0
            try:
                selectint = int(float(selectindex))
                selecteditem = currentitems[selectint]
                stage = 2
            except ValueError:
                nprint('Invalid index: '+selectindex)
                continue
            except KeyError:
                if selectint == 0:
                    stage = 3
                    break
                else:
                    nprint('Index out of bounds.')
                

        ##Stage 2: Select recipe for breaking down item
        while stage == 2:
            availablerecipes = {} ##stores recipe name and how much it needs to be multiplied
            for recipe in recipes:
                if selecteditem in recipes[recipe].output:
                    mult = craftitems[selecteditem]/recipes[recipe].output[selecteditem]
                    availablerecipes[recipe] = mult
            if len(availablerecipes) == 0:
                nprint('No recipe available for use with this item.')
                stage = 1
                break
            else:
                if len(availablerecipes) == 1:
                    selectedrecipe = list(availablerecipes)[0]
                else:
                    currentrecipes = {}
                    currentcounter = 1
                    nprint(separator)
                    nprint('Select recipe to use:')
                    for recipe in availablerecipes:
                        nprint('\n'+str(currentcounter) + '. ' + str(recipe) + ' ['+strf(availablerecipes[recipe])+']')
                        nprint('[ '+recipes[recipe].strme(availablerecipes[recipe])+' ]') ##multiply recipe display with mult
                        currentrecipes[currentcounter] = recipe
                        currentcounter = currentcounter + 1
                    selectindex = ninput('\nEnter index of recipe to use (or enter 0 to cancel): ')
                    selectint = 0
                    try:
                        selectint = int(float(selectindex))
                        selectedrecipe = currentrecipes[selectint]
                    except ValueError:
                        nprint('Invalid index.')
                        continue
                    except KeyError:
                        if selectint == 0:
                            stage = 1
                            break
                        else:
                            nprint('Index out of bounds.')
                            continue

                recipeused = recipes[selectedrecipe]
                m = availablerecipes[selectedrecipe]
                for item in recipeused.ninput:
                    craftitems[item] = (craftitems.get(item,0)
                                       +recipeused.ninput[item]*m)
                for item in recipeused.output:
                    craftitems[item] = (craftitems.get(item,0)
                                       -recipeused.output[item]*m)
                nprint('\nRecipe '+str(selectedrecipe)+' crafted '+str(m)+'x :')
                nprint('['+recipeused.strme(m)+']')

                stage = 1
                    
        
        ##Stage 3: View/save large recipe
        while stage == 3:
            for item in inititems:
                craftitems[item]-=inititems[item]
            totalinput = {}
            totaloutput = {}
            for item in craftitems:
                itemamt = craftitems[item]
                if itemamt == 0:
                    continue
                elif itemamt > 0:
                    totalinput[item] = itemamt
                else:
                    totaloutput[item] = -itemamt

            totalrecipe = Recipe('Total',totalinput,totaloutput)
            nprint(separator)
            nprint('Complete recipe:')
            nprint(totalrecipe.strme(expand=True))
            prompttocheck = True
            while prompttocheck:
                checkmore = ninput('\nCheck new recipes? (y/n)').lower()
                if checkmore in 'yn':
                    prompttocheck = False
                    if checkmore == 'y':
                        stage = 0
                        init = True
                        break
                    else:
                        stage = 4
                        runprogram = False
                        break
        ##FUTURE
        ##Stage 4: Select buildings to process recipes
        ##Stage 5: Select beacons

# runprogram()
