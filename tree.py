#Berk Karabacak 150114823
#Eren Ulas 150114822

from datetime import datetime
import math
import time
import os

# Person class
class Person(object):
    def __init__(self, name, surname=None, gender=None, birthdate=None, father=None, mother=None, deathdate=None, maritalStat=None, partner=None):
        self.name = name
        self.child = []
        self.partner = None
        self.mother = None
        self.father = None
        self.fatherName = None
        self.motherName = None
        self.partnerName = None
        self.generation = None
        self.birthdate = None
        self.deathdate = None
        self.maritalStat = None
        self.gender = None
        if not surname is None:
            self.surname = surname
        if not gender is None:
            self.gender = gender
        if not birthdate is None:
            self.birthdate = birthdate
        if not deathdate is None:
            self.deathdate = deathdate
        if not father is None:
            self.fatherName = father
        if not mother is None:
            self.motherName = mother
        if not partner is None:
            self.partnerName = partner
        if not maritalStat is None:
            self.maritalStat = maritalStat

#this list contains all the people in the family
familytree = []

#calculates the age of a person
def calculate_age(birthdate):
    birthdate = datetime.strptime(birthdate,'%d/%m/%Y')
    return math.floor((datetime.today() - birthdate).days / 365)

#finds if a person is dead or not
def isdead(person):
    if not person.deathdate is None:
        return True
    else:
        return False

#finds if a person is over 18 or not
def resitmi(person):
    return calculate_age(person.birthdate) > 17

#checks if the dates entered are realistic
def datesAreRealistic(person):
    Realistic = True
    if hasattr(person, 'deathdate') and hasattr(person, 'birthdate'):
        if person.birthdate > person.deathdate:
            Realistic = False
    if hasattr(person, 'deathdate'):
        if person.deathdate > datetime.today():
            Realistic = False
    if hasattr(person, 'birthdate'):
        if person.birthdate > datetime.today():
            Realistic = False
    return Realistic

#creates an instance of a person class with the necessary inputs and adds it to the familytree list
def adduser(name, surname, gender, birthdate, father, mother, deathdate, maritalStatus, partnerName):
    # typeofperson child father veya annemi oldugu
    user = Person(name, surname, gender, birthdate, father, mother, deathdate,maritalStatus,partnerName)
    familytree.append(user)

#prints the persons in the family list
def printusernames():
    for number in familytree:
        print (number.name)

#finds the object with the personName
def findperson(personName):
    person = None
    for index in familytree:
        if index.name == personName:
            person = index
    return person

#adds child relations
def addchild():
    for person in familytree:
        person.child = []
    for person in familytree:
        for index in familytree:
            if not person.fatherName is None and person.fatherName == index.name:
                # checks that a father cannot have a child after his death date
                if not index.deathdate is None and calculate_age(index.deathdate) > calculate_age(person.birthdate):
                    print(index.name,"cannot have a child after death")
                    counter = 0
                    for i in familytree:
                        if i.name != person.name:
                            counter += 1
                        else:
                            # removes the newly added child if the child is added after the father's death
                            familytree.remove(familytree[counter])
                else:
                    person.father = index
                    index.child.append(person)
            if not person.motherName is None and person.motherName == index.name:
                # checks that a mother cannot have a child after her death date
                if not index.deathdate is None and calculate_age(index.deathdate) > calculate_age(person.birthdate):
                    print(index.name,"cannot have a child after death")
                    counter = 0
                    for i in familytree:
                        if i.name != person.name:
                            counter += 1
                        else:
                            # removes the newly added child if the child is added after the mother's death
                            familytree.remove(familytree[counter])
                else:
                    person.mother = index
                    index.child.append(person)

#adds partner relations
def addpartner():
    for person in familytree:
        if not person.partnerName is None:
            if not findperson(person.partnerName) is None:
                # if the person is not over 18, it gave warning and removes the added partner. Otherwise it forms the partner relationship
                if calculate_age(findperson(person.partnerName).birthdate) > 17:
                    person.partner = findperson(person.partnerName)
                    if not person.partner is None:
                        person.partner.partner = person
                else:
                    familytree.remove(findperson(person.partnerName))
                    print(person.name,"cannot marry with",person.partnerName,".Person is not over 18")
                    person.partnerName = None


#finds mother
def getmother(person):
    if not person.mother is None:
        return person.mother
    return None

#finds father
def getfather(person):
    if not person.father is None:
        return person.father
    return None
#finds sons
def getson(person):
    son = []
    if not person.child is None:
        for index in person.child:
            if index.gender == "male":
                son.append(index)
        return son
    return None

#finds daughters
def getdaughter(person):
    daughter = []
    if not person.child is None:
        for index in person.child:
            if index.gender == "female":
                daughter.append(index)
        return daughter
    return None

#finds brothers
def getbrother(person):
    brother = []
    if not person.father is None and not person.father.child is None:
        for index in person.father.child:
            if index.gender == "male" and index.name != person.name:
                brother.append(index)
    elif not person.mother is None and not person.mother.child is None:
        for index in person.mother.child:
            if index.gender == "male" and index.name != person.name:
                brother.append(index)
    return brother

#finds sisters
def getsister(person):
    sister = []
    if not person.father is None and not person.father.child is None:
        for index in person.father.child:
            if index.gender == "female" and index.name != person.name:
                sister.append(index)
    elif not person.mother is None and not person.mother.child is None:
        for index in person.mother.child:
            if index.gender == "female" and index.name != person.name:
                sister.append(index)
    return sister

#abileri bulur
def getelderbrother(person):
    elderbrother = []
    if not getbrother(person) is None:
        for index in getbrother(person):
            if calculate_age(person.birthdate) < calculate_age(index.birthdate):
                elderbrother.append(index)
        return elderbrother
    return None

#ablaları bulur
def geteldersister(person):
    eldersister = []
    if not getsister(person) is None:
        for index in getsister(person):
            if calculate_age(person.birthdate) < calculate_age(index.birthdate):
                eldersister.append(index)
        return eldersister
    return None

#amcaları bulur
def getamca(person):
    amca = []
    if not person.father is None and not person.father.father is None and not person.father.father.child is None:
        for index in person.father.father.child:
            if index.gender == "male" and index.name != person.father.name:
                amca.append(index)
        return amca
    return None

#halaları bulur
def gethala(person):
    hala = []
    if not person.father is None and not person.father.father is None and not person.father.father.child is None:
        for index in person.father.father.child:
            if index.gender == "female":
                hala.append(index)
        return hala
    return None

#dayıları bulur
def getdayi(person):
    dayi = []
    if not person.mother is None and not person.mother.father is None and not person.mother.father.child is None:
        for index in person.mother.father.child:
            if index.gender == "male":
                dayi.append(index)
        return dayi
    return None

#teyzeleri bulur
def getteyze(person):
    teyze = []
    if not person.mother is None and not person.mother.father is None and not person.mother.father.child is None:
        for index in person.mother.father.child:
            if index.gender == "female" and index.name != person.mother.name:
                teyze.append(index)
        return teyze
    return None

#yeğenleri bulur
def getnephew(person):
    nephew = []
    if not getsister(person) is None:
        for index in getsister(person):
            if not index.child is None:
                for children in index.child:
                    nephew.append(children)
    if not getbrother(person) is None:
        for index in getbrother(person):
            if not index.child is None:
                for children in index.child:
                    nephew.append(children)
    return nephew

#kuzenleri bulur
def getcousin(person):
    cousin = []
    if not getamca(person) is None:
        for index in getamca(person):
            if not index.child is None:
                for children in index.child:
                    cousin.append(children)
    if not gethala(person) is None:
        for index in gethala(person):
            if not index.child is None:
                for children in index.child:
                    cousin.append(children)
    if not getdayi(person) is None:
        for index in getdayi(person):
            if not index.child is None:
                for children in index.child:
                    cousin.append(children)
    if not getteyze(person) is None:
        for index in getteyze(person):
            if not index.child is None:
                for children in index.child:
                    cousin.append(children)
    return cousin

#enisteleri bulur
def geteniste(person):
    eniste = []
    if not gethala(person) is None:
        for index in gethala(person):
            if not index.partner is None:
                eniste.append(index.partner)
    if not getteyze(person) is None:
        for index in getteyze(person):
            if not index.partner is None:
                eniste.append(index.partner)
    if not getsister(person) is None:
        for index in getsister(person):
            if not index.partner is None:
                eniste.append(index.partner)
    return eniste

#yengeleri bulur
def getyenge(person):
    yenge = []
    if not getamca(person) is None:
        for index in getamca(person):
            if not index.partner is None:
                yenge.append(index.partner)
    if not getdayi(person) is None:
        for index in getdayi(person):
            if not index.partner is None:
                yenge.append(index.partner)
    return yenge

#kayınvalideyi bulur
def getmotherinlaw(person):
    if not person.partner is None and not person.partner.mother is None:
        return person.partner.mother
    return None

#kayınpederi bulur
def getfatherinlaw(person):
    if not person.partner is None and not person.partner.father is None:
        return person.partner.father
    return None

#gelinleri bulur
def getdaughterinlaw(person):
    daughterinlaw = []
    if not person.child is None:
        for index in person.child:
            if index.gender == "male" and not index.partner is None:
                daughterinlaw.append(index.partner)
    return daughterinlaw

#damatları bulur
def getsoninlaw(person):
    soninlaw = []
    if not person.child is None:
        for index in person.child:
            if index.gender == "female" and not index.partner is None:
                soninlaw.append(index.partner)
    return soninlaw

#bacanakları bulur
def getbacanak(person):
    bacanak = []
    if not person.partner is None and not getsister(person.partner) is None:
        for index in getsister(person.partner):
            if not index.partner is None:
                bacanak.append(index.partner)
    return bacanak

#baldızları bulur
def getbaldiz(person):
    if not person.partner is None:
        return getsister(person.partner)

#eltileri bulur
def getelti(person):
    elti = []
    if not person.partner is None and getbrother(person.partner):
        for index in getbrother(person.partner):
            if not index.partner is None:
                elti.append(index.partner)
    return elti

#kayınbiraderleri bulur
def getkayinbirader(person):
    if not person.partner is None:
        return getbrother(person.partner)

#finds grandmothers
def getgrandmother(person):
    grandmother = []
    if not person.mother is None and not person.mother.mother is None:
        grandmother.append(person.mother.mother)
    if not person.father is None and not person.father.mother is None:
        grandmother.append(person.father.mother)
    return grandmother

#finds grandfathers
def getgrandfather(person):
    grandfather = []
    if not person.mother is None and not person.mother.father is None:
        grandfather.append(person.mother.father)
    if not person.father is None and not person.father.father is None:
        grandfather.append(person.father.father)
    return grandfather

#finds grandchilds
def getgrandchild(person):
    grandchild = []
    if not person.child is None:
        for index in person.child:
            if not index.child is None:
                for index2 in index.child:
                    grandchild.append(index2)
    return grandchild

#checks if the person1 and person 2 has a mother relation
def ismother(person1, person2,state):
    if person1.mother is person2:
        if state == 0:
            print(person2.name,person1.name, "'in annesidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a father relation
def isfather(person1, person2,state):
    if person1.father is person2:
        if state == 0:
            print(person2.name,person1.name,"'in babasidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a son relation
def isson(person1, person2,state):
    son = getson(person1)
    if person2 in son:
        if state == 0:
            print(person2.name,person1.name,"'in ogludur")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a daughter relation
def isdaughter(person1, person2,state):
    daughter = getdaughter(person1)
    if person2 in daughter:
        if state == 0:
            print(person2.name,person1.name, "'in kizidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a brother relation
def isbrother(person1, person2,state):
    brother = getbrother(person1)
    if person2 in brother:
        if state == 0:
            print(person2.name,person1.name,"'in erkek kardesidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a sister relation
def issister(person1,person2,state):
    sister = getsister(person1)
    if not sister is None:
        if person2 in sister:
            if state == 0:
                print(person2.name,person1.name, "'in kiz kardesidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has an elder brother relation
def iselderbrother(person1,person2,state):
    elderbrother = getelderbrother(person1)
    if person2 in elderbrother:
        if state == 0:
            print(person2.name,person1.name,"nin abisidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has an elder sister relation
def iseldersister(person1,person2,state):
    eldersister = geteldersister(person1)
    if not eldersister is None:
        if person2 in eldersister:
            if state == 0:
                print(person2.name,person1.name,"nin ablasidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has an amca relation
def isamca(person1, person2,state):
    amca = getamca(person1)
    if not amca is None:
        if person2 in amca:
            if state == 0:
                print(person2.name,person1.name, "nin amcasidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a hala relation
def ishala(person1, person2,state):
    hala = gethala(person1)
    if not hala is None:
        if person2 in hala:
            if state == 0:
                print(person2.name,person1.name, "nin halasidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a dayi relation
def isdayi(person1, person2,state):
    dayi = getdayi(person1)
    if not dayi is None:
        if person2 in dayi:
            if state == 0:
                print(person2.name,person1.name,"nin dayisidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a teyze relation
def isteyze(person1,person2,state):
    teyze = getteyze(person1)
    if not teyze is None:
        if person2 in teyze:
            if state == 0:
                print(person2.name,person1.name,"nin teyzesidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a nephew relation
def isnephew(person1, person2,state):
    nephew = getnephew(person1)
    if person2 in nephew:
        if state == 0:
            print(person2.name,person1.name,"'in yegenidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a cousin relation
def iscousin(person1, person2,state):
    cousin = getcousin(person1)
    if not cousin is None:
        if person2 in cousin:
            if state == 0:
                print(person2.name,person1.name,"'in kuzenidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has an eniste relation
def iseniste(person1, person2,state):
    eniste = geteniste(person1)
    if not eniste is None:
        if person2 in eniste:
            if state == 0:
                print(person2.name,person1.name, "nin enistesidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a yenge relation
def isyenge(person1, person2,state):
    yenge = getyenge(person1)
    if not yenge is None:
        if person2 in yenge:
            if state == 0:
                print(person2.name,person1.name, "nin yengesidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a mother in law relation
def ismotherinlaw(person1,person2,state):
    if not person1.partner is None:
        if getmotherinlaw(person1) is person2:
            if state == 0:
                print(person2.name,person1.name,"'in kayinvalidesidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a father in law relation
def isfatherinlaw(person1, person2,state):
    if not person1.partner is None:
        if getfatherinlaw(person1) is person2:
            if state == 0:
                print(person2.name,person1.name,"'in kayinpederidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a daughter in law relation
def isgelin(person1, person2,state):
    gelin = getdaughterinlaw(person1)
    if person2 in gelin:
        if state == 0:
            print(person2.name,person1.name,"nin gelinidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a son in law relation
def isdamat(person1, person2,state):
    damat = getsoninlaw(person1)
    if person2 in damat:
        if state == 0:
            print(person2.name,person1.name, "nin damadidir")
            return True
        elif state == 1:
            return True

#checks if the person1 and person 2 has a bacanak relation
def isbacanak(person1, person2,state):
    if not person1.partner is None and not person1.gender is None and person1.gender == "male":
        bacanak = getbacanak(person1)
        if person2 in bacanak:
            if state == 0:
                print(person2.name,person1.name, "nin bacanagidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a baldiz relation
def isbaldiz(person1, person2,state):
    if not person1.partner is None and person1.gender == "male":
        baldiz = getbaldiz(person1)
        if not baldiz is None:
            if person2 in baldiz:
                if state == 0:
                    print(person2.name,person1.name, "nin baldizidir")
                    return True
                elif state == 1:
                    return True

#checks if the person1 and person 2 has an elti relation
def iselti(person1, person2,state):
    if not person1.partner is None and person1.gender == "female":
        elti = getelti(person1)
        if person2 in elti:
            if state == 0:
                print(person2.name,person1.name, "nin eltisidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a kayinbirader relation
def iskayindirader(person1, person2,state):
    kayinbirader = getkayinbirader(person1)
    if not kayinbirader is None:
        if person2 in kayinbirader:
            if state == 0:
                print(person2.name,person1.name, "nin kayinbiraderidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a grandmother relation
def isgrandmother(person1,person2,state):
    grandmother = getgrandmother(person1)
    if not grandmother is None:
        if person2 in grandmother:
            if state == 0:
                print(person2.name,person1.name,"'in büyükannesidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a grandfather relation
def isgrandfather(person1,person2,state):
    grandfather = getgrandfather(person1)
    if not grandfather is None:
        if person2 in grandfather:
            if state == 0:
                print(person2.name,person1.name,"'in büyükbabasidir")
                return True
            elif state == 1:
                return True

#checks if the person1 and person 2 has a grandchild relation
def isgrandchild(person1,person2,state):
    grandchild = getgrandchild(person1)
    if not grandchild is None:
        if person2 in grandchild:
            if state == 0:
                print(person2.name,person1.name,"'in torunudur")
                return True
            elif state == 1:
                return True

#finds the relatinship according to the gicen inputs.
#If state is 0, then it shows a sentence that explains the relationship
#If state is 1, then it returns a word that explains the relationship
def findrelationship(person1Name, person2Name,state):
    person1 = findperson(person1Name)
    person2 = findperson(person2Name)
    result = ""

    if state == 0:
        ismother(person1,person2,state)
    elif state == 1 and ismother(person1,person2,state):
        result = "mother"
    if state == 0:
        isfather(person1,person2,state)
    elif state == 1 and isfather(person1,person2,state):
        result = "father"
    if state == 0:
        isson(person1,person2,state)
    elif state ==1 and isson(person1,person2,state):
        result = "son"
    if state == 0:
        isdaughter(person1, person2, state)
    elif state == 1 and isdaughter(person1,person2,state):
        result = "daughter"
    if state == 0:
        isbrother(person1, person2, state)
    elif state == 1 and isbrother(person1,person2,state):
        result = "brother"
    if state == 0:
        issister(person1, person2, state)
    elif state == 1 and issister(person1,person2,state):
        result = "sister"
    if state == 0:
        iseldersister(person1, person2, state)
    elif state == 1 and iseldersister(person1,person2,state):
        result = "eldersister"
    if state == 0:
        iselderbrother(person1, person2, state)
    elif state == 1 and iselderbrother(person1,person2,state):
        result = "elderbrother"
    if state == 0:
        isamca(person1, person2, state)
    elif state == 1 and isamca(person1,person2,state):
        result = "amca"
    if state == 0:
        ishala(person1, person2, state)
    elif state == 1 and ishala(person1,person2,state):
        result = "hala"
    if state == 0:
        isdayi(person1, person2, state)
    elif state == 1 and isdayi(person1,person2,state):
        result = "dayi"
    if state == 0:
        isteyze(person1, person2, state)
    elif state == 1 and isteyze(person1,person2,state):
        result = "teyze"
    if state == 0:
        isnephew(person1, person2, state)
    elif state == 1 and isnephew(person1,person2,state):
        result = "nephew"
    if state == 0:
        iscousin(person1, person2, state)
    elif state == 1 and iscousin(person1,person2,state):
        result = "cousin"
    if state == 0:
        iseniste(person1, person2, state)
    elif state == 1 and iseniste(person1,person2,state):
        result = "eniste"
    if state == 0:
        isyenge(person1, person2, state)
    elif state == 1 and isyenge(person1,person2,state):
        result = "yenge"
    if state == 0:
        ismotherinlaw(person1, person2, state)
    elif state == 1 and ismotherinlaw(person1,person2,state):
        result = "motherinlaw"
    if state == 0:
        isfatherinlaw(person1, person2, state)
    elif state == 1 and isfatherinlaw(person1,person2,state):
        result = "fatherinlaw"
    if state == 0:
        isgelin(person1, person2, state)
    elif state == 1 and isgelin(person1,person2,state):
        result = "gelin"
    if state == 0:
        isdamat(person1, person2, state)
    elif state == 1 and isdamat(person1,person2,state):
        result = "damat"
    if state == 0:
        isbacanak(person1, person2, state)
    elif state == 1 and isbacanak(person1,person2,state):
        result = "bacanak"
    if state == 0:
        isbaldiz(person1, person2, state)
    elif state == 1 and isbaldiz(person1,person2,state):
        result = "baldiz"
    if state == 0:
        iselti(person1, person2, state)
    elif state == 1 and iselti(person1,person2,state):
        result = "elti"
    if state == 0:
        iskayindirader(person1, person2, state)
    elif state == 1 and iskayindirader(person1,person2,state):
        result = "kayinbirader"
    if state == 0:
        isgrandmother(person1,person2,state)
    elif state == 1 and isgrandmother(person1,person2,state):
        result = "grandmother"
    if state == 0:
        isgrandfather(person1,person2,state)
    elif state == 1 and isgrandfather(person1,person2,state):
        result = "grandfather"
    if state == 0:
        isgrandchild(person1,person2,state)
    elif state == 1 and isgrandchild(person1,person2,state):
        result = "grandchild"

    return result

#gets the oldest person in the familytree list
def getoldest():
    max = 0
    maxPerson = None
    for person in familytree:
        if not person.birthdate is None:
            if calculate_age(person.birthdate) > max:
                max = calculate_age(person.birthdate)
                maxPerson = person
    return maxPerson

# sets the generation of the people in the familytree list
def setgeneration():
    #finds the oldest one and sets its generation as 0
    for person in familytree:
        person.generation = None
    maxPerson = getoldest()
    maxPerson.generation = 0
    if not maxPerson.partner is None:
        maxPerson.partner.generation = 0
        generationcounter = 2
    elif maxPerson.partner is None:
        generationcounter = 1

    #person's siblings' generation is set to the same value as the person's value.
    #person's children's generation is set to the person's generation value plus 1
    while generationcounter != len(familytree):
        for person in familytree:
            if not person.generation is None:
                if not person.partner is None and person.partner.generation is None:
                    person.partner.generation = person.generation
                    generationcounter += 1
                if not getson(person) is None:
                    for index in getson(person):
                        if index.generation is None:
                            index.generation = person.generation + 1
                            generationcounter += 1
                        if not index.partner is None and not person.partner is None and person.partner.generation is None:
                            index.partner.generation = index.generation
                            generationcounter += 1
                if not getdaughter(person) is None:
                    for index in getdaughter(person):
                        if index.generation is None:
                            index.generation = person.generation + 1
                            generationcounter += 1
                        if not index.partner is None and not person.partner is None and person.partner.generation is None:
                            index.partner.generation = index.generation
                            generationcounter += 1
                if not getbrother(person) is None:
                    for index in getbrother(person):
                        if index.generation is None:
                            index.generation = person.generation
                            generationcounter += 1
                        if not index.partner is None and not person.partner is None and person.partner.generation is None:
                            index.partner.generation = index.generation
                            generationcounter += 1
                if not getsister(person) is None:
                    for index in getsister(person):
                        if index.generation is None:
                            index.generation = person.generation
                            generationcounter += 1
                        if not index.partner is None and not person.partner is None and person.partner.generation is None:
                            index.partner.generation = index.generation
                            generationcounter += 1
            elif person.generation is None:
                for index in person.child:
                    if not index.generation is None:
                        person.generation = index.generation-1
                        person.partner.generation = person.generation
                        generationcounter +=2

#finds the maximum level(generation) in the list
def findmaxlevel():
    max = 0
    for person in familytree:
        if person.generation > max:
            max = person.generation
    return max

#prints the oldest person(since he/she is the root)
def printroot():
    person = getoldest()
    if not person.partner is None:
        print(person.name,"-",person.partner.name)
    elif person.partner is None:
        print(person.name)

#prints the remaining part of the familytree
def printfamilytree(list):
    for person in list:
        treestruct = " "
        for i in range(person.generation*2 -1):
            treestruct = treestruct + " "
        treestruct = treestruct + "|"
        #prints person's partner's mother and father names next to it
        if not person.partner is None:
            if not person.partner.motherName is None and not person.partner.fatherName is None:
                print(treestruct,person.name,"-",person.partner.name,"(",person.partner.motherName,"-",person.partner.fatherName,")")
            elif not person.partner.motherName is None and person.partner.fatherName is None:
                print(treestruct, person.name, "-", person.partner.name, "(", person.partner.motherName,")")
            elif person.partner.motherName is None and not person.partner.fatherName is None:
                print(treestruct,person.name,"-",person.partner.name,"(",person.partner.fatherName,")")
            else:
                print(treestruct,person.name,"-",person.partner.name)
        else:
            print(treestruct,person.name)
        #it goes to the bottom of the list recursively
        printfamilytree(person.child)

#checks if the relationship between the person and the person's partner is valid or nor.
#if it is not valid, it prints a statement about it, and removes the partner relation between them
def canmarry():
    for person in familytree:
        if not person.partner is None:
            relation = findrelationship(person.name,person.partner.name,1)
            cantmarry = ["mother","father","son,","daughter","sister","brother","amca","dayi","eniste","hala","teyze","yenge","yegen","grandmother","grandfather","grandchild"]
            if relation in cantmarry:
                print(person.name,"can't be married with",person.partner.name,"because they are close relatives")
                person.partner.partner = None
                person.partner.partnerName = None
                person.maritalStat = "s"
                person.partner = None
                person.partnerName = None
                person.maritalStat = "s"


#menu function that shows the menu
def menu():
    print("Press 1 to add a new person,")
    print("Press 2 to update a person, ")
    print("Press 3 to display the basic information about a user,")
    print("Press 4 to display the family tree, ")
    creaOrUpt = input("Press 5 to ask the relationship between two person: ")
    #for creating a person
    if(creaOrUpt == "1"):
        name = input("Name : ")
        surname = input("Surname : ")
        gender = input("Gender (Enter as male or female): ")
        birthDate = input("Birth date : ")
        if birthDate == "":
            birthDate = None
        deathDate = input("Death date : ")
        if deathDate == "":
            deathDate = None
        # if death and birth date are not realistic, it asks the user to enter one of them again
        if not deathDate is None:
            if calculate_age(deathDate) > calculate_age(birthDate):
                while calculate_age(deathDate) > calculate_age(birthDate):
                    print("Deathdate is not realistic. Which data do you want to enter again? ")
                    choice = input("Press 1 for birthdate, Press 2 for deathdate: ")
                    if choice == 1:
                        birthDate = input("Please enter birthdate: ")
                    else:
                        deathDate = input("Please enter deathdate:")
                    if deathDate == "":
                        break
        fatherName = input("Father name :")
        motherName = input("Mother name : ")
        #if the person is over 18 than it doesn't show the marital status question
        if not birthDate is None:
            if(calculate_age(birthDate) >= 18):
                maritalStat = input("Single or marrried ? (Enter s or m) : ")
                if(maritalStat == "m"):
                    partner = input("Partner name: ")
                elif(maritalStat == "s"):
                    partner = None
            else:
                maritalStat = "s"
                partner = None
        else:
            maritalStat = input("Single or marrried ? (Enter s or m) : ")
            if (maritalStat == "m"):
                partner = input("Partner name: ")
            elif (maritalStat == "s"):
                partner = None

        adduser(name, surname, gender, birthDate, fatherName, motherName, deathDate, maritalStat,partner)
    # updates a person
    elif creaOrUpt == "2":
        name = input("Name of the person you want to update:")
        #finds the person that the user wants to update from its name
        person = findperson(name)
        print("Which information do you want to update for this user?")
        print("Press 1 for surname,")
        print("Press 2 for gender (enter as female or male),")
        print("Press 3 for birth date,")
        print("Press 4 for death date,")
        print("Press 5 for father name, ")
        print("Press 6 for mother name, ")
        updtdata = input("Press 7 for marital status: ")
        if updtdata == "1":
            surname = input("Enter the new surname: ")
            person.surname = surname
        elif updtdata == "2":
            gender = input("Enter the new gender: ")
            person.gender = gender
        elif updtdata == "3":
            birthdate = input("Enter the new birth date: ")
            person.birthdate = birthdate
        elif updtdata == "4":
            birthdate = person.birthdate
            deathdate = input("Enter the new death date: ")
            if deathdate == "":
                deathdate = None
            # checks if the death and the birth dates are realistic or nor
            if not deathdate is None:
                if calculate_age(deathdate) > calculate_age(person.birthdate):
                    while calculate_age(deathdate) > calculate_age(person.birthdate):
                        choice = input("Deathdate is not realistic. Which data do you want to enter again? (Press 1 for birthdate, Press 2 for deathdate): ")
                        if choice == 1:
                            birthdate = input("Please enter birthdate: ")
                        else:
                            deathdate = input("Please enter deathdate:")
                        if deathdate == "":
                            break
                person.birthdate = birthdate
                person.deathdate = deathdate
        elif updtdata == "5":
            fathername = input("Enter the new father name: ")
            person.fatherName = fathername
        elif updtdata == "6":
            mothername = input("Enter the new mother name: ")
            person.motherName = mothername
        elif updtdata == "7":
            maritalstat = input("Enter the new marital status: ")
            #if the person is over 18 than user can change the marital status
            #if user changes it from married to single, it removes the partner relationship
            if calculate_age(person.birthdate) > 17:
                if person.maritalStat == "s" and maritalstat == "m":
                    partnername = input("Enter your partner's name: ")
                    person.partnerName = partnername
                    person.maritalStat = maritalstat
                elif person.maritalStat == "m" and maritalstat == "s":
                    person.partner.partnerName = None
                    person.partner.partner = None
                    person.partner.maritalStat = "s"
                    person.partnerName = None
                    person.partner = None
                    person.maritalStat = "s"
            else:
                person.maritalStat = "s"
                person.partner = None
    #shows the basic information about a person
    elif creaOrUpt == "3":
        name = input("Enter the user's name: ")
        person = findperson(name)
        if isdead(person):
            print(person.name,"is dead")
        else:
            print(person.name,"is alive")
        print("Age: ", calculate_age(person.birthdate))
        print("Level of the person: ", person.generation)
    #displays the family tree
    elif creaOrUpt == "4":
        addchild()
        addpartner()
        setgeneration()
        canmarry()
        printroot()
        printfamilytree(getoldest().child)
    # finds the relationship between two person
    elif creaOrUpt == "5":
        person1name = input("Enter the first person's name: ")
        person2name = input("Enter the second person's name: ")
        findrelationship(person1name,person2name,0)



#menu loops
menu()
done = input("Do you want to continue ? (Press y for yes or press n for no)")
while done=="y":
    os.system('cls')
    menu()
    done = input("Do you want to continue ? (Press y for yes or press n for no)")


input()