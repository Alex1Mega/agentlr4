import random
#1
items = [
    ("Ноутбук", 4, 30),
    ("Навушники", 1, 10),
    ("Камера", 3, 25),
    ("Смартфон", 2, 20),
    ("Планшет", 3, 18),
    ("Книга", 2, 8),
    ("Павербанк", 2, 12),
    ("Миша", 1, 7),
    ("Клавіатура", 2, 11),
    ("SSD", 1, 15)
]
# Максимальна вага
CAPACITY = 10
print("ТАБЛИЦЯ ПРЕДМЕТІВ")
print("-" * 45)
print(f"{'№':<5}{'Назва':<15}{'Вага':<10}{'Цінність'}")
print("-" * 45)
for i, item in enumerate(items, 1): print(f"{i:<5}{item[0]:<15}{item[1]:<10}{item[2]}")
print(f"\nМаксимальна місткість рюкзака: {CAPACITY}")

# Мета: знайти набір предметів з максимальною сумарною цінністю, не перевищуючи допустиму вагу рюкзака.
# Параметри генетичного алгоритму
POPULATION_SIZE = 100
GENERATIONS = 100
MUTATION_RATE = 0.05

# Хромосома складається з 0 та 1: 1 - предмет вибраний 0 - предмет не вибраний
def create_chromosome():
    return [
        random.randint(0, 1)
        for _ in range(len(items))
    ]

def create_population():
    return [
        create_chromosome()
        for _ in range(POPULATION_SIZE)
    ]

def calculate_weight(chromosome):
    return sum(
        chromosome[i] * items[i][1]
        for i in range(len(items))
    )

def calculate_value(chromosome):
    return sum(
        chromosome[i] * items[i][2]
        for i in range(len(items))
    )

# Якщо вага перевищує місткість рюкзака, розв'язок вважається недопустимим.
def fitness(chromosome):
    weight = calculate_weight(chromosome)
    value = calculate_value(chromosome)
    if weight > CAPACITY: return 0
    return value

# Вибір батьків. Турнірний відбір.
def selection(population):
    tournament = random.sample(population, 3)
    return max(tournament, key=fitness)

# 2
# Вибираються дві точки хромосоми. Частина між цими точками обмінюється між двома батьківськими хромосомами.
def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(len(parent1)), 2))

    child1 = (
        parent1[:point1]
        + parent2[point1:point2]
        + parent1[point2:]
    )
    child2 = (
        parent2[:point1]
        + parent1[point1:point2]
        + parent2[point2:]
    )
    return child1, child2

# Для кожної позиції хромосоми окремо вибирається ген від першого або другого батька.
def bitwise_crossover(parent1, parent2):
    child1 = []
    child2 = []
    for bit1, bit2 in zip(parent1, parent2):
        if random.random() < 0.5:
            child1.append(bit1)
            child2.append(bit2)
        else:
            child1.append(bit2)
            child2.append(bit1)
    return child1, child2

# Мутація: кожен ген може випадково змінитися: 0 -> 1 і навпаки
def mutation(chromosome):
    chromosome = chromosome.copy()
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE: chromosome[i] = 1 - chromosome[i]
    return chromosome

def genetic_algorithm(crossover_function):
    population = create_population()
    best_solution = None
    best_value = 0

    # Основний цикл генетичного алгоритму
    for generation in range(GENERATIONS):
        new_population = []
        # Знаходимо найкращу особину поточного покоління
        current_best = max(population, key=fitness)
        current_fitness = fitness(current_best)

        if current_fitness > best_value:
            best_value = current_fitness
            best_solution = current_best.copy()

        # Створення нового покоління
        while len(new_population) < POPULATION_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover_function(parent1, parent2)
            child1 = mutation(child1)
            child2 = mutation(child2)
            # Додавання дітей до нового покоління
            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE: new_population.append(child2)
        # Перехід до нового покоління
        population = new_population
    return best_solution

def print_solution(solution):
    total_weight = calculate_weight(solution)
    total_value = calculate_value(solution)
    print("\nВибрані предмети:")
    for i in range(len(items)):
        if solution[i] == 1:
            print(
                f"- {items[i][0]} "
                f"(вага: {items[i][1]}, "
                f"цінність: {items[i][2]})"
            )
    print(f"\nЗагальна вага: {total_weight}")
    print(f"Загальна цінність: {total_value}")
    print(f"Хромосома: {solution}")

print("\n")
print("TWO-POINT CROSSOVER")

random.seed(42)
solution_two_point = genetic_algorithm(two_point_crossover)
print_solution(solution_two_point)

print("\n")
print("BITWISE CROSSOVER")

random.seed(42)

solution_bitwise = genetic_algorithm(bitwise_crossover)
print_solution(solution_bitwise)

value_two_point = calculate_value(solution_two_point)
weight_two_point = calculate_weight(solution_two_point)

value_bitwise = calculate_value(solution_bitwise)
weight_bitwise = calculate_weight(solution_bitwise)


print("\n")
print("ПОРІВНЯННЯ РЕЗУЛЬТАТІВ")

print(
    f"Two-point crossover: "
    f"цінність = {value_two_point}, "
    f"вага = {weight_two_point}"
)

print(
    f"Bitwise crossover: "
    f"цінність = {value_bitwise}, "
    f"вага = {weight_bitwise}"
)

if value_two_point > value_bitwise: print("\nКращий результат: Two-point crossover")
elif value_bitwise > value_two_point: print("\nКращий результат: Bitwise crossover")
else: print("\nОбидва crossover дали однаковий результат.")