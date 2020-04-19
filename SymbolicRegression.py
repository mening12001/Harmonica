from Genetica import Genetica
import numpy as np

print("Harmonica Experiments")

genetica = Genetica()

genetica.set_target_function("math.sin(2*math.pi*x)", 11)
genetica.generate_function(100, 50)

genetica.set_target_function("0.8 * math.sin(2 * math.pi * x) + 0.9 * math.cos(2 * math.pi * 2 * x) + 0.3 * math.sin(2 * math.pi * 3 * x) + 0.75 * math.sin(2 * math.pi * 4 * x)", 21)
genetica.generate_function(100, 50)

genetica.set_target_function_values([0.27, 0.33, 0.13, 0.3, 0.15, 0.12, 0.19, 0.33, 0.41, 0.29, 0.44, 0.43, 0.23, 0.24, 0.32, 0.46, 0.35, 0.48, 0.64,0.42 ,0.42, 0.55,0.63, 0.62, 0.55, 0.69, 0.63, 0.66, 0.54, 0.64, 0.71, 0.6, 0.63, 0.65, 0.74, 0.87])
genetica.generate_function(100, 50)