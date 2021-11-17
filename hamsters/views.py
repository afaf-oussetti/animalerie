from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Equipement


# afficher la liste des animaux et des équipements
def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'hamsters/animal_list.html', {'animaux': animaux, 'equipements': equipements})


# afficher les détails de l'animal selectionné avec l'équipement qu'il utilise
def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement = animal.lieu
    equipements = Equipement.objects.all()
    return render(request, 'hamsters/animal_detail.html',
                  {'animal': animal, 'equipement': equipement, 'equipements': equipements})


# affiche l'équipement suivant en se basant sur l'équipement actuel
# si l'équipement actuel est la litière on l'envoie au mangeoire
def equipement_suivant(id_eq):
    equipements = ["mangeoire", "roue", "nid"]
    marked = False
    for e in equipements:
        if (marked):
            return e
        if (e == id_eq):
            marked = True
    return equipements[0]


# affiche létat actuel de l'animal après avoir éta dans l'équipement passé en paramètre
def etat_suivant(equipement):
    dict = {"mangeoire": "repus", "roue": "fatigués", "nid": "affamés"}
    return dict[equipement]


# faire passer l'animal à l'équipement suivant tout en changeant son état
# afficher une erreur 404 si l'équipement suivant est occupé
def deplacer_animal(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement_courant = animal.lieu

    id_next = equipement_suivant(equipement_courant.id_equip)
    ett_suivant = etat_suivant(id_next)
    equipement_next = get_object_or_404(Equipement, pk=id_next)
    print(equipement_courant, equipement_next, equipement_courant.disponibilite)
    if (equipement_next.disponibilite != "libre"):
        raise Http404("equipement n'est pas libre")

    equipement_courant.disponibilite = "libre"
    equipement_next.disponibilite = "occupé"
    animal.lieu = equipement_next
    animal.etat = ett_suivant
    equipement_next.save()
    animal.save()
    equipement_courant.save()

    return redirect("/animal/" + id_animal)


# faire passer l'animal à la litière
def deplacer_animal_litière(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement_courant = animal.lieu

    equipement_courant.disponibilite = "libre"
    equipement_courant.save()
    animal.etat = "affamés"
    animal.lieu = get_object_or_404(Equipement, pk="litière")
    animal.save()
    return redirect("/animal/" + id_animal)

# afficher les détails relatives à l'équipement choisi.
def equipement_details(request, id_equip):
    equipement = get_object_or_404(Equipement, pk=id_equip)
    return render(request, 'hamsters/equipement_detail.html', {'equipement': equipement})
