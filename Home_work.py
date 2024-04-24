from dataclasses import dataclass

@dataclass
class Item:
    name:str
    price:float
    
    def __str__(self):
        return f"{self.name}: {self.price} Kč"

@dataclass
class Pizza(Item):
    ingredients:dict

    def add_extra(self, ingredient, quantity, price_per_ingredient):
        self.ingredients[ingredient] = quantity
        self.price += quantity * price_per_ingredient

    def __str__(self):
        ingredients_str = ", ".join(f"{ingredient} ({quantity}g)" for ingredient, quantity in self.ingredients.items())
        return f"Pizza {self.name} ({ingredients_str}): {self.price} Kč"

@dataclass
class Drink(Item):
    volume: int

    def __str__(self):
        return f"Nápoj {self.name} ({self.volume} ml): {self.price} Kč"

@dataclass
class Order:
    customer_name:str
    delivery_address:str
    items:list
    status="Nova"

    def mark_delivered(self):
        self.status = "Doručeno"

    def __str__(self):
        item_list = "\n".join(str(item) for item in self.items)
        return f"Objednávka pro {self.customer_name} na adresu {self.delivery_address}:\n{item_list}\nStav: {self.status}"

@dataclass
class DeliveryPerson:
    name:str
    phone_number:str
    available=True
    current_order=None

    def assign_order(self, order):
        if self.available:
            self.current_order = order
            self.current_order.status = "Na cestě"
            self.available = False
            return f"Objednávka {self.current_order} přiřazena doručovateli {self.name}."
        else:
            return f"Doručovatel {self.name} není momentálně dostupný."

    def complete_delivery(self):
        if self.current_order:
            self.current_order.status = "Doručeno"
            self.available = True
            return f"Objednávka {self.current_order} byla úspěšně doručena."
        else:
            return f"Doručovatel {self.name} nemá aktuální objednávku k doručení."

    def __str__(self):
        availability = "Dostupný" if self.available else "Nedostupný"
        return f"Doručovatel: {self.name}, Telefon: {self.phone_number}, Stav: {availability}"
    
    # Vytvoření instance pizzy a manipulace s ní
margarita = Pizza("Margarita", 200, {"sýr": 100, "rajčata": 150})
margarita.add_extra("olivy", 50, 10)

# Vytvoření instance nápoje
cola = Drink("Cola", 1.5, 500)

# Vytvoření a výpis objednávky
order = Order("Jan Novák", "Pražská 123", [margarita, cola])
print(order)

# Vytvoření řidiče a přiřazení objednávky
delivery_person = DeliveryPerson("Petr Novotný", "777 888 999")
delivery_person.assign_order(order)
print(delivery_person)

# Dodání objednávky
delivery_person.complete_delivery()
print(delivery_person)

# Kontrola stavu objednávky po doručení
print(order)