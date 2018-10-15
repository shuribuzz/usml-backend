import carbuilder

competitors = []
sportscar_list = []
suv_list = []

ferarry = {'brand': 'ferarry', 'shape': 'sportscar', 'maxspeed': 340,
           'dragcoef': 0.324, 'timetomax': 26, 'ewf': None}
bugatti = {'brand': 'bugatti', 'shape': 'sportscar', 'maxspeed': 407,
           'dragcoef': 0.39, 'timetomax': 32, 'ewf': None}
toyota = {'brand': 'toyota', 'shape': 'SUV', 'maxspeed': 180,
           'dragcoef': 0.25, 'timetomax': 40, 'ewf': 2}
lada = {'brand': 'lada', 'shape': 'SUV', 'maxspeed': 180,
           'dragcoef': 0.32, 'timetomax': 56, 'ewf': 6}
sx4 = {'brand': 'sx4', 'shape': 'SUV', 'maxspeed': 180,
           'dragcoef': 0.33, 'timetomax': 44, 'ewf': 3}


competitors.append(carbuilder.create(**ferarry))
competitors.append(carbuilder.create(**bugatti))
competitors.append(carbuilder.create(**toyota))
competitors.append(carbuilder.create(**lada))
competitors.append(carbuilder.create(**sx4))

for car in competitors:
    if car._Car__body.shape == 'sportscar':
        sportscar_list.append(car)
    elif car._Car__body.shape == 'SUV':
        suv_list.append(car)

def ret_comp(body):
    if body == 'sportscar':
        return sportscar_list
    elif body == 'SUV':
        return  suv_list

