class Person:
        def __init__(self, name="unnamed", marriagewith=[], parents = [], children = [], alive=True):
                self.name = name
                self.marriagewith = marriagewith
                self.parents = parents
                self.children = children
                self.alive = alive

        def inform(self):
                CH = []
                for x in self.children:
                        CH += [x.name]
                PR = []
                for x in self.parents:
                        PR += [x.name]
                MR = []
                for x in self.marriagewith:
                        MR += [x.name]
                print("Name:", self.name, "Married:", MR,"Parents:", PR,"Children:", CH,"Alive:", self.alive)

        def __eq__(self, other):
                if type(other) == str:
                        return self.name == other
                else:
                        return self.name == other.name

        def grandparents(self):
                grans = []
                if self.parents != []:
                        for parent in self.parents:
                                if parent.parents != []:
                                        for grandparent in parent.parents:
                                                grans += [grandparent]
                return grans



def informlist(L):
        for x in L:
        	x.inform()

def getnames(Descriptions):
        allnames = []
        for line in Descriptions:
                onlynames = line.split(" ")[1:]
                allnames += onlynames
        return sorted(set(allnames))

def humanizeall(names):
        family = []
        for name in names:
                family += [Person(name)]
        return family

def finder(name, L):
        for People in L:
                if name == People:
                        return People

def familytree(Descriptions):
        People = humanizeall(getnames(Descriptions))
        for x in People:
                for line in Descriptions:
                        spline = line.split(" ")

                        if spline[0] == "CHILD":
                                if x == spline[1] or x == spline[2]:
                                        for y in spline[3:]:
                                                x.children = x.children + [finder(y,People)]
                                if x in spline[3:]:
                                        for y in spline[1:3]:
                                                x.parents = x.parents + [finder(y,People)]

                        if spline[0] == "MARRIED":
                            if x == spline[1]:
                                x.marriagewith = [finder(spline[2], People)]
                            if x == spline[2]:
                                x.marriagewith = [finder(spline[1], People)]

                        if spline[0] == "DEPARTED" or spline[0] == "DECEASED":
                        	if x == spline[1]:
                        		x.alive = False
        return People



def helperinherit(person, heirs, I):
        if person.children:
                if heritable_counter(person.children) == 0:
                        return []
                for child in person.children:
                        if child.alive:
                                heirs += [(child.name, I/heritable_counter(person.children))]
                        if not child.alive:
                                helperinherit(child, heirs, I/heritable_counter(person.children))                        
        return heirs

def corrector(heirs, initialI):
        totalI = 0
        for heir in heirs:
                totalI += heir[1]
        if totalI == 0:
                rate = 0
        else:
                rate = initialI/totalI
        correctheirs = []
        for heir in heirs:
                if rate == 0:
                        correctheirs += [(heir[0], heir[1])]
                else:
                        correctheirs += [(heir[0], heir[1]*rate)]
        return correctheirs

def alivefinder(People):
        alives = []
        for person in People:
                if person.alive:
                        alives += [person]
        return alives

def are_heritable(People):
        for person in People:
                if is_heritable(person):
                        return True
        return False

def is_heritable(person):
        if person.alive:
                return True
        elif person.children:
                for child in person.children:
                        if is_heritable(child):
                                return True
        return False

def heritable_counter(People):
        counter = 0
        for person in People:
                if is_heritable(person):
                        counter += 1
        return counter


def adder(heirs):
        i = 0
        while i < len(heirs):
                j = 1
                while j < len(heirs):
                        if j>i:
                                if heirs[i][0] == heirs[j][0]:
                                        heirs[i] = (heirs[i][0], heirs[i][1] + heirs[j][1])
                                        del(heirs[j])
                        j += 1
                i += 1
        return heirs






def inheritance(Descriptions):
        family = familytree(Descriptions)
        for line in Descriptions:
                if line.split(" ")[0] == "DECEASED":
                        deceased = finder(line.split(" ")[-2], family)
                        I = float(line.split(" ")[-1])
        heirs = []

        if deceased.marriagewith != []:
                spouse = deceased.marriagewith[0]
                if spouse.alive:
                        if are_heritable(deceased.children):
                                heirs += [(spouse.name, I/4)] + corrector(helperinherit(deceased, [], I*3/4), I*3/4)

                        elif are_heritable(deceased.parents):
                                heirs += [(spouse.name, I/2)]
                                for parent in deceased.parents:
                                        if parent.alive:
                                                heirs += [(parent.name, I/(2*heritable_counter(deceased.parents)))]
                                        else:
                                                heirs += corrector(helperinherit(parent, [], I/4), I/4)

                        elif are_heritable(deceased.grandparents()):
                                heirs += [(spouse.name, I*3/4)]
                                for grandparent in deceased.grandparents():
                                        if grandparent.alive:
                                                heirs += [(grandparent.name, (I/4)/(heritable_counter(deceased.grandparents()) ) )] 
                                        else:
                                                heirs += corrector(helperinherit(grandparent, [], (I/4)/(heritable_counter(deceased.grandparents() ) ) ), (I/4)/(heritable_counter(deceased.grandparents())))
                        else:
                                heirs += [(spouse.name, I)]

                if not spouse.alive:
                        if are_heritable(deceased.children):
                                heirs += corrector(helperinherit(deceased, [], I),I)

                        elif are_heritable(deceased.parents):
                                for parent in deceased.parents:
                                        if parent.alive:
                                                heirs += [(parent.name, I/heritable_counter(deceased.parents))]
                                        else:
                                                heirs += corrector(helperinherit(parent, [], I/2), I/2)

                        elif are_heritable(deceased.grandparents()):
                                for grandparent in deceased.grandparents():
                                        if grandparent.alive:
                                                heirs += [(grandparent.name, I/heritable_counter(deceased.grandparents()))]
                                        else:
                                                heirs += corrector(helperinherit(grandparent, [], I/heritable_counter(deceased.grandparents())), I/heritable_counter(deceased.grandparents()))


        if deceased.marriagewith == []:
                if are_heritable(deceased.children):
                        heirs += corrector(helperinherit(deceased, [], I),I)

                elif are_heritable(deceased.parents):
                                for parent in deceased.parents:
                                        if parent.alive:
                                                heirs += [(parent.name, I/heritable_counter(deceased.parents))]
                                        else:
                                                heirs += corrector(helperinherit(parent, [], I/2), I/2)

                elif are_heritable(deceased.grandparents()):
                                for grandparent in deceased.grandparents():
                                        if grandparent.alive:
                                                heirs += [(grandparent.name, I/heritable_counter(deceased.grandparents()))]
                                        else:
                                                heirs += corrector(helperinherit(grandparent, [], I/heritable_counter(deceased.grandparents())), I/heritable_counter(deceased.grandparents()))

        return adder(heirs)