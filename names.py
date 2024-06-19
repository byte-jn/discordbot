import random

def names():
  namen = [
      "Lukas", "Sophia", "Maximilian", "Emma", "Alexander", "Mia", "Paul", "Hannah", "Leon", "Anna",
      "Felix", "Lena", "David", "Marie", "Julian", "Laura", "Tobias", "Sarah", "Simon", "Julia",
      "Benjamin", "Lisa", "Jonas", "Nina", "Fabian", "Jana", "Florian", "Lara", "Philipp", "Lea",
      "Moritz", "Eva", "Sebastian", "Katharina", "Daniel", "Melanie", "Christian", "Johanna", "Martin", "Jessica",
      "Andreas", "Sandra", "Oliver", "Stefanie", "Jan", "Sabrina", "Markus", "Carolin", "Michael", "Annika",
      "Thomas", "Nicole", "Matthias", "Daniela", "Stefan", "Katrin", "Patrick", "Bianca", "Dennis", "Anja",
      "Marcel", "Tanja", "Tim", "Christina", "Dominik", "Nadine", "Christopher", "Melissa", "Kevin", "Isabel",
      "Sven", "Verena", "Marco", "Vanessa", "Robert", "Jennifer", "Jens", "Natalie", "Andre", "Juliane",
      "Timo", "Claudia", "Björn", "Saskia", "Lars", "Susanne", "Peter", "Kerstin", "Dirk", "Petra",
      "Manuel", "Heike", "Frank", "Silke", "Ralf", "Ines", "Jörg", "Yvonne", "Holger", "Monika"
  ]
  
  # Überprüfe, ob die Datei mit den bereits ausgewählten Namen existiert
  try:
      with open("ausgewaehlte_namen.txt", "r") as file:
          ausgewaehlte_namen = file.read().splitlines()
  except FileNotFoundError:
      ausgewaehlte_namen = []
  
  # Überprüfe, ob alle Namen bereits ausgewählt wurden
  if len(ausgewaehlte_namen) == len(namen):
      return ("Alle Namen wurden bereits ausgewählt.")
  else:
      # Wähle einen zufälligen Namen, der noch nicht ausgewählt wurde
      ausgewaehlter_name = random.choice([name for name in namen if name not in ausgewaehlte_namen])
  
      # Füge den ausgewählten Namen zur Liste der ausgewählten Namen hinzu
      ausgewaehlte_namen.append(ausgewaehlter_name)
  
      # Speichere die aktualisierte Liste der ausgewählten Namen in der Datei
      with open("ausgewaehlte_namen.txt", "w") as file:
          file.write("\n".join(ausgewaehlte_namen))
  
      return (f"{ausgewaehlter_name}")