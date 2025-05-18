import random
from abc import ABC, abstractmethod

class Creature(ABC):
    def __init__(self, name: str, attack: int, defense: int, health: int, damage_range: tuple):
        if not (1 <= attack <= 30):
            raise ValueError("Атака должна быть от 1 до 30.")
        if not (1 <= defense <= 30):
            raise ValueError("Защита должна быть от 1 до 30.")
        if health <= 0:
            raise ValueError("Здоровье должно быть положительным числом.")
        if not (isinstance(damage_range, tuple) and len(damage_range) == 2 and damage_range[0] < damage_range[1]):
            raise ValueError("Урон должен быть кортежем (минимум, максимум).")

        self.name = name
        self.attack = attack
        self.defense = defense
        self.max_health = health
        self.health = health
        self.damage_range = damage_range

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage: int):
        self.health = max(self.health - damage, 0)
        print(f"{self.name} получает {damage} урона. Осталось здоровья: {self.health}")

    def attack_target(self, target):
        modifier = max(1, self.attack - target.defense + 1)
        rolls = [random.randint(1, 6) for _ in range(modifier)]
        print(f"{self.name} бросает кубики: {rolls}")
        if any(roll >= 5 for roll in rolls):
            damage = random.randint(*self.damage_range)
            print(f"Удар успешен! {self.name} наносит {damage} урона {target.name}.")
            target.take_damage(damage)
        else:
            print(f"{self.name} промахивается!")

    @abstractmethod
    def take_turn(self, opponent):
        pass

class Player(Creature):
    def __init__(self, name: str, attack: int, defense: int, health: int, damage_range: tuple):
        super().__init__(name, attack, defense, health, damage_range)
        self.heals_left = 4

    def heal(self):
        if self.heals_left > 0:
            amount = int(self.max_health * 0.3)
            self.health = min(self.health + amount, self.max_health)
            self.heals_left -= 1
            print(f"{self.name} исцеляется на {amount}. Текущее здоровье: {self.health}. Осталось исцелений: {self.heals_left}")
        else:
            print(f"{self.name} не может больше исцеляться!")

    def take_turn(self, opponent):
        action = input("Выберите действие (удар/исцелить): ").strip().lower()
        if action == "удар":
            self.attack_target(opponent)
        elif action == "исцелить":
            self.heal()
        else:
            print("Неверное действие. Ход пропущен.")

class Monster(Creature):
    def take_turn(self, opponent):
        self.attack_target(opponent)

def generate_random_monster():
    names = ["Орк", "Гоблин", "Тролль", "Скелет", "Вампир"]
    name = random.choice(names)
    attack = random.randint(8, 14)
    defense = random.randint(4, 9)
    health = random.randint(75, 100)
    damage_range = (random.randint(3, 5), random.randint(7, 10))
    return Monster(name, attack, defense, health, damage_range)

def main():
    player = Player("Герой", attack=11, defense=6, health=90, damage_range=(4, 9))
    monster = generate_random_monster()

    print(f"\n⚔️ Вам противостоит: {monster.name} (Атака: {monster.attack}, Защита: {monster.defense}, Здоровье: {monster.health})")

    while player.is_alive() and monster.is_alive():
        print("\nХод игрока:")
        player.take_turn(monster)
        if monster.is_alive():
            print("\nХод монстра:")
            monster.take_turn(player)

    if player.is_alive():
        print("\n🎉 Победа! Вы победили монстра!")
    else:
        print("\n💀 Вы были побеждены...")

if __name__ == "__main__":
    main()
