import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_simulations = 1000
average_waste_per_truck = 10  # tons
std_dev_waste = 2  # standard deviation in tons
fuel_price_per_liter = np.array([1.0, 1.2, 1.5])  # different scenarios of fuel prices
fuel_efficiency = 2.5  # km per liter
distance_per_collection = 50  # km

# Simulate
total_costs = []
for price in fuel_price_per_liter:
    costs = []
    for _ in range(num_simulations):
        waste_collected = np.random.normal(average_waste_per_truck, std_dev_waste)
        fuel_cost = (distance_per_collection / fuel_efficiency) * price
        costs.append(fuel_cost)
    total_costs.append(costs)

# Plotting results
fig, ax = plt.subplots()
ax.boxplot(total_costs, labels=[f'${price} per liter' for price in fuel_price_per_liter])
ax.set_title('Fuel Costs Under Different Price Scenarios')
ax.set_ylabel('Cost ($)')
plt.show()
