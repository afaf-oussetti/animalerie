from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Equipement
from django.contrib import messages


# Create your views here.


def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'hamsters/animal_list.html', {'animaux': animaux, 'equipements': equipements})


def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement = animal.lieu
    equipements = Equipement.objects.all()
    return render(request, 'hamsters/animal_detail.html',
                  {'animal': animal, 'equipement': equipement, 'equipements': equipements})


def animal_detail_ingnore_litiere(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement = animal.lieu
    equipements = Equipement.objects.all()

    for e in equipements:
        if (e.id_equip == "litière"):
            e.disponibilite = "libre"
    return render(request, 'hamsters/animal_detail.html',
                  {'animal': animal, 'equipement': equipement, 'equipements': equipements})


def equipement_suivant(id_eq):
    equipements = ["mangeoire", "roue", "nid"]
    marked = False
    for e in equipements:
        if (marked):
            return e
        if (e == id_eq):
            marked = True
    return equipements[0]


def deplacer_animal(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement_courant = animal.lieu

    id_next = equipement_suivant(equipement_courant.id_equip)
    equipement_next = get_object_or_404(Equipement, pk=id_next)
    print(equipement_courant, equipement_next, equipement_courant.disponibilite)
    if (equipement_next.disponibilite != "libre"):
        raise Http404("equipement n'est pas libre")

    equipement_courant.disponibilite = "libre"
    equipement_next.disponibilite = "occupé"
    animal.lieu = equipement_next
    equipement_next.save()
    animal.save()
    equipement_courant.save()

    return redirect("/animal/" + id_animal)


def deplacer_animal_litière(request, id_animal):
    animal = get_object_or_404(Animal, pk=id_animal)
    equipement_courant = animal.lieu

    equipement_courant.disponibilite = "libre"
    equipement_courant.save()

    animal.lieu = get_object_or_404(Equipement, pk="litière")
    animal.save()
    return redirect("/animal/" + id_animal)
