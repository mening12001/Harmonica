import random
import math
import numpy as np

class Genetica:

    global target_function_values
    global nr_of_genes
    global amplitude_bounds
    global constant_bounds


    def init_bounds(self):
        self.amplitude_bounds = (0, 1)
        self.constant_bounds = (-10, 10)

    def __init__(self):
        super.__init__(self)

    def __init__(self, target_function_values = "none", periodic_target_function = "none", sample_frequency = "none" ):
      #  self.target_function_values = target_function_values
       # self.nr_of_genes = int(((len(target_function_values) - 1)/2) * 2)
        #self.init_bounds()
        #--------11test_target_function = "math.sin(2*math.pi*x)"
        #test_target_function = "3+0.83*math.sin(2*math.pi*x/5)+0.7*math.cos(2*math.pi*2*x/5)+0.9*math.sin(2*math.pi*3*x/5)"
        #test_target_function = "0.83*math.sin(2*math.pi*x/20)+0.7*math.cos(2*math.pi*2*x/20)+0.9*math.sin(2*math.pi*3*x/20) + 0.2*math.sin(2*math.pi*6*x/20)"
        #test_target_function = "2+math.sin(2*math.pi*x/10)+math.cos(2*math.pi*2*x/10)+math.sin(2*math.pi*3*x/10) + math.sin(2*math.pi*4*x/10)"
        #-------21test_target_function = "0.8 * math.sin(2 * math.pi * x) + 0.9 * math.cos(2 * math.pi * 2 * x) + 0.3 * math.sin(2 * math.pi * 3 * x) + 0.75 * math.sin(2 * math.pi * 4 * x)"
        #climate_temp = [0.27, 0.33, 0.13, 0.3, 0.15, 0.12, 0.19, 0.33, 0.41, 0.29, 0.44, 0.43, 0.23, 0.24, 0.32, 0.46, 0.35, 0.48, 0.64,0.42 ,0.42, 0.55,0.63, 0.62, 0.55, 0.69, 0.63, 0.66, 0.54, 0.64, 0.71, 0.6, 0.63, 0.65, 0.74, 0.87, "x"]
        #self.target_function_values = climate_temp
#        prime_series = [0.2, 0.3, 0.5, 0.7, "x", "x", "x", "x", "x", "x", "x", "x" ,"x", "x", "x", "x", "x", "x"]
 #       self.target_function_values = prime_series
        #self.target_function_values = self.function_to_values(test_target_function, 21)

        if target_function_values != "none":
            self.target_function_values = target_function_values
        else:
            if periodic_target_function != "none" and sample_frequency != "none":
                self.target_function_values = self.function_to_values(periodic_target_function, sample_frequency)
                self.nr_of_genes = int(((((len(self.target_function_values)) -1 ) / 2) - 1) * 2)
                self.init_bounds()

    def set_target_function(self, periodic_target_function, sample_frequency):
        self.target_function_values = self.function_to_values(periodic_target_function, sample_frequency)
        self.nr_of_genes = int(((((len(self.target_function_values)) - 1) / 2) - 1) * 2)
        self.init_bounds()

    def set_target_function_values(self, target_function_values):
        self.target_function_values = target_function_values
        self.nr_of_genes = int(((((len(self.target_function_values)) - 1) / 2) - 1) * 2)
        self.init_bounds()

    def function_to_values(self, function, sample_frequency):
        target_function_values = []
        for x in range(sample_frequency):
            target_function_values.append(eval(function.replace("x",str(x) +"/" + str(sample_frequency - 1))))
        return target_function_values


    def generate_inital_population(self, size):
        population = []
        for ind in range(size):
            genotype = {}
            for gene in range(self.nr_of_genes):
                genotype[gene] = random.uniform(self.amplitude_bounds[0], self.amplitude_bounds[1])
            genotype[self.nr_of_genes] = random.uniform(self.constant_bounds[0], self.constant_bounds[1])
            population.append(genotype)

        return population

    def uniform_mutate(self, genotype):
        random_gene = random.randint(0, len(genotype) - 1)
        if random_gene != self.nr_of_genes:
            genotype[random_gene] = random.uniform(self.amplitude_bounds[0], self.amplitude_bounds[1])
        else:
            genotype[random_gene] = random.uniform(self.constant_bounds[0], self.amplitude_bounds[1])
        return genotype

    def crossover(self, genotype1, genotype2):
        genotype3 = {}
        genotype4 = {}
        for gene in genotype1:
            if gene % 2 == 0:
                genotype3[gene] = genotype1[gene]
                genotype4[gene] = genotype2[gene]
            else:
                genotype3[gene] = genotype2[gene]
                genotype4[gene] = genotype1[gene]
        return [genotype3, genotype4]

    #compose the actuall function based on the coeficients encoded in the genes
    def compose_function(self, genotype):

        function_expression = ""

        for gene in genotype:
            if gene < int(len(genotype)/2):
                function_expression = function_expression + str(genotype[gene]) + " * math.cos(2 * math.pi * " + str(gene+1) + " * x /" + str(len(self.target_function_values)-1)+" )"
            else:
                if gene != self.nr_of_genes:
                    function_expression = function_expression + str(genotype[gene]) + " * math.sin(2 * math.pi * " + str(int(gene+2 - len(genotype)/2)) + " * x /" + str(len(self.target_function_values)-1)+" )"
            if gene != self.nr_of_genes:
                function_expression = function_expression + " + "
        function_expression = function_expression + " (" + str(genotype[self.nr_of_genes]) + ")"

        return function_expression



    #compute fitness based on rms , value between 0... ,100 -> 100, means the best
    def compute_fitness(self, genotype):
        obtained_values = []
        obtained_function = self.compose_function(genotype)
        for x in range(0, len(self.target_function_values)):
            obtained_values.append(eval(obtained_function.replace("x", str(x))))
        #return 100 * 1/(1 + np.sqrt(np.array((np.array(obtained_values) - np.array(self.target_function_values)) ** 2).mean()))

        return (100 / (1 + np.square(np.subtract(obtained_values, self.target_function_values)).mean()))

    #when the are  missing values that intended to be "predicted"
    def compute_fitness_prediction(self, genotype):
        obtained_values = []
        obtained_function = self.compose_function(genotype)
        given = 0
        for x in range(0, len(self.target_function_values)):
            given = given + 1
            if self.target_function_values[x] != "x":
                obtained_values.append(eval(obtained_function.replace("x", str(x))))
            else:
                given = given - 1
                break
        return (100 / (1 + np.square(np.subtract(obtained_values[:given], self.target_function_values[:given])).mean()))


    def show_result(self, genotype):
        obtained_values = []
        obtained_function = self.compose_function(genotype)
        for x in range(0, len(self.target_function_values)):
            obtained_values.append(eval(obtained_function.replace("x", str(x))))
        # return 100 * 1/(1 + np.sqrt(np.array((np.array(obtained_values) - np.array(self.target_function_values)) ** 2).mean()))
        print("obtained values: " + str(obtained_values))
        print("target values: " + str(self.target_function_values))


    def sort_population_by_fitness(self, population):
        return sorted(population, key=self.compute_fitness)


    def generate_next_generation(self, previous_population):
        next_generation = []
        sorted_by_fitness_population = self.sort_population_by_fitness(previous_population)
        population_size = len(previous_population)
        fitness_sum = sum(self.compute_fitness(individual) for individual in sorted_by_fitness_population)

        for i in range(int(population_size/2)):
            first_choice = self.roulette_selection(sorted_by_fitness_population, fitness_sum)
            second_choice = self.roulette_selection(sorted_by_fitness_population, fitness_sum)

            individuals = self.crossover(first_choice, second_choice)
            individual1 = self.uniform_mutate(individuals[0])
            individual2 = self.uniform_mutate(individuals[1])
            #individual1 = self.uniform_mutate(individual1)
            #individual2 = self.uniform_mutate(individual2)
            next_generation.append(individual1)
            next_generation.append(individual2)
            next_generation.extend(previous_population)
            next_generation = sorted(next_generation, key=self.compute_fitness, reverse=True)[:population_size]

        return next_generation

    def roulette_selection(self, sorted_population, fitness_sum):
        normalized_fitness_sum = fitness_sum
        draw = random.uniform(0, 1)

        accumulated = 0
        for genotype in sorted_population:
            fitness = self.compute_fitness(genotype)
            probability = fitness / normalized_fitness_sum
            accumulated += probability

            if draw <= accumulated:
                return genotype

    def show_function(self, genotype):
        function_expression = ""

        for gene in genotype:
            if gene < int(len(genotype) / 2):
                function_expression = function_expression + str(genotype[gene]) + " * cos(2 * pi * " + str(
                    gene + 1) + " * x /" + str(len(self.target_function_values) - 1) + " )"
            else:
                if gene != self.nr_of_genes:
                    function_expression = function_expression + str(
                        genotype[gene]) + " * sin(2 * pi * " + str(
                        int(gene + 2 - len(genotype) / 2)) + " * x /" + str(len(self.target_function_values) - 1) + " )"
            if gene != self.nr_of_genes:
                function_expression = function_expression + " + "
        function_expression = function_expression + " (" + str(genotype[self.nr_of_genes]) + ")"

        print(function_expression)


    def generate_function(self, nr_of_generations, population_size):
        generations = nr_of_generations

        population = self.generate_inital_population(population_size)

        i = 1
        while True:
            print(f"🧬 GENERATION {i}")

            if i == generations:
                break

            i += 1

            population = self.generate_next_generation(population)
           # if self.compute_fitness(population[0]) >= 98.0:
           #     break

        best_individual = self.sort_population_by_fitness(population)[-1]
        print("\n🔬 FINAL RESULT")
        print("Genotype: " + str(best_individual))
        print("Fenotype/Function: " + str(self.show_function(best_individual)))
        print("Fitness: " + str(self.compute_fitness(best_individual)))