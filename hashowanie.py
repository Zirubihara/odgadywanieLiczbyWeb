import hashlib

haslo = "AlaMAKota1"

hashed_haslo = hashlib.sha256(haslo.encode()).hexdigest()
hashed_haslo2 = hashlib.sha256(haslo.encode()).hexdigest()
hashed_haslo3 = hashlib.sha256(haslo.encode()).hexdigest()

print(hashed_haslo)
print(hashed_haslo2)
print(hashed_haslo3)