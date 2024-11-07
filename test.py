from pyomo.environ import *

# Create a simple model
model = ConcreteModel()

# Define decision variables
model.x = Var(within=NonNegativeReals)
model.y = Var(within=NonNegativeReals)

# Define objective function
model.obj = Objective(expr=3*model.x + 2*model.y, sense=maximize)

# Define constraints
model.constraint1 = Constraint(expr=2*model.x + 3*model.y <= 12)
model.constraint2 = Constraint(expr=2*model.x + model.y <= 8)

# Create a solver
solver = SolverFactory('glpk')

# Solve the model
solver.solve(model, tee=True)

# Display results
print(f"x = {model.x()}")
print(f"y = {model.y()}")
