from django.shortcuts import render
from django.http import HttpResponse
class SystemeExpert:
    def __init__(self):
        self.base_faits = {}
        self.base_connaissances = []

    def ajouter_fait(self, fait, valeur):
        self.base_faits[fait] = valeur

    def ajouter_regles(self, regles):
        self.base_connaissances.extend(regles)

    def chainer_avant(self):
        for regle in self.base_connaissances:
            if self.evaluer_regle(regle):
                return True
        return False

    def chainer_arriere(self, objectif):
        if objectif in self.base_faits:
            return self.base_faits[objectif]
        for regle in self.base_connaissances:
            if regle["conclusion"]["fait"] == objectif:
                if self.evaluer_regle(regle):
                    return True
        return False

    def chainer_mixte(self, objectif):
        if self.base_faits.get(objectif):
            return self.base_faits[objectif]
        for regle in self.base_connaissances:
            if regle["conclusion"]["fait"] == objectif:
                if self.evaluer_regle(regle):
                    return True
                continue
        return False

    def evaluer_regle(self, regle):
        conditions = regle["conditions"]
        for condition in conditions:
            if self.base_faits.get(condition["fait"]) != condition["valeur"]:
                return False
        self.base_faits[regle["conclusion"]["fait"]] = regle["conclusion"]["valeur"]
        return True


# Exemple d'utilisation
systeme = SystemeExpert()

# Ajout des faits
faits = {
    "Espèce": "Ficus",
    "Taille": "Petite",
    "Type de Sol": "Terreau",
    "Exposition au Soleil": "Soleil",
}
for fait, valeur in faits.items():
    systeme.ajouter_fait(fait, valeur)

# Ajout des règles
regles = [
    {
        "conditions": [{"fait": "Espèce", "valeur": "Ficus"}],
        "conclusion": {"fait": "Classe", "valeur": "Petite"},
    },
    {
        "conditions": [
            {"fait": "Espèce", "valeur": "Ficus"},
            {"fait": "Taille", "valeur": "Petite"},
            {"fait": "Type de Sol", "valeur": "Terreau"},
            {"fait": "Exposition au Soleil", "valeur": "Soleil"},
        ],
        "conclusion": {"fait": "Fréquence d'Arrosage", "valeur": "Tous les jours"},
    },
    # Ajouter d'autres règles ici
]

systeme.ajouter_regles(regles)

# Utilisation du chaînage avant
if systeme.chainer_avant():
    print("Chaînage avant réussi.")
    print(systeme.base_faits)

# Utilisation du chaînage arrière
objectif = "Fréquence d'Arrosage"
resultat_arriere = systeme.chainer_arriere(objectif)
if resultat_arriere:
    print(f"Chaînage arrière réussi pour {objectif}: {resultat_arriere}")
else:
    print(f"Impossible de déduire {objectif} avec le chaînage arrière.")

# Utilisation du chaînage mixte
objectif_mixte = "Classe"
resultat_mixte = systeme.chainer_mixte(objectif_mixte)
if resultat_mixte:
    print(f"Chaînage mixte réussi pour {objectif_mixte}: {resultat_mixte}")
else:
    print(f"Impossible de déduire {objectif_mixte} avec le chaînage mixte.")


def chatbot_interface(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Create an instance of your expert system
        systeme = SystemeExpert()

        # Add facts and rules to the expert system
        # Note: You may want to load facts and rules from a database or other source instead of hardcoding them.

        # Add facts
        facts = {
            "Espèce": "Rose",
            "Couleur": "Rouge",
            "Taille": "Moyenne",
            "Type de Sol": "Riche",
            "Exposition au Soleil": "Ensoleillé",
            "Parfum": "Fort",
        }
        for fact, value in facts.items():
            systeme.ajouter_fait(fact, value)

        # Add rules
        rules = [
            {
                "conditions": [{"fait": "Espèce", "valeur": "Rose"}],
                "conclusion": {"fait": "Classe", "valeur": "Moyenne"},
            },
            {
                "conditions": [
                    {"fait": "Espèce", "valeur": "Rose"},
                    {"fait": "Couleur", "valeur": "Rouge"},
                    {"fait": "Parfum", "valeur": "Fort"},
                ],
                "conclusion": {"fait": "Appréciation", "valeur": "Très élevée"},
            },
            {
                "conditions": [
                    {"fait": "Espèce", "valeur": "Rose"},
                    {"fait": "Exposition au Soleil", "valeur": "Ensoleillé"},
                ],
                "conclusion": {"fait": "Besoin d'Eau", "valeur": "Modéré"},
            },
            # Add other rules here
        ]
        systeme.ajouter_regles(rules)

        # Process user input using the expert system
        response = process_user_input(systeme, user_input)

        # Return the response as JSON
        return HttpResponse(response)

    return render(request, 'expert.html')

def process_user_input(systeme, user_input):
  
    if "classe" in user_input.lower() and "rose" in user_input.lower():
        if systeme.chainer_mixte("Classe"):
            return f" La classe de la rose est {systeme.base_faits.get('Classe', 'Classe non déterminée')}."
        else:
            return "La classe de la plante n'a pas pu être déterminée."

    # Add more logic for handling different user inputs
    elif "besoin d'eau" in user_input.lower() and "rose" in user_input.lower():
        if systeme.chainer_mixte("Besoin d'Eau"):
         besoin_eau_rose = systeme.base_faits.get('Besoin d\'Eau', 'non déterminé')
         return f"Le besoin en eau de la rose est {besoin_eau_rose}."
        else:
            return "Le besoin en eau de la plante n'a pas pu être déterminé."
        
    elif "couleur" in user_input.lower() and "rose" in user_input.lower():
        if systeme.chainer_mixte("Couleur"):
            # Le système peut répondre à la question sur la couleur de la rose
            return f"La couleur de la rose est {systeme.base_faits.get('Couleur', 'non déterminée')}."
        
        else:
            # Aucune réponse spécifique trouvée
            return "La couleur de la rose n'a pas pu être déterminée."

     # Ajoutez une réponse générique pour les salutations
    elif "bonjour" in user_input.lower():
        return "Bonjour ! Je suis Smart Pot - Système Expert."
    # Handle other types of questions or user inputs

    return "Je ne comprends pas la question."

# Add other views or functions as needed
