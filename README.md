# Bus Routing Optimization Problem

## 1. Introduction

### Objective
The objective is to develop an optimized routing and scheduling model for a city bus fleet, consisting of both electric and diesel buses. The goal is to minimize operational costs while ensuring each trip is served.

### Background
City bus networks face challenges in assigning buses to routes due to limited charging/refueling resources, vehicle capacity, and operational costs. This mixed-fleet optimization problem becomes more complex with larger numbers of routes and vehicles, making computational efficiency crucial.

---

## 2. Problem Statement

The aim is to assign each bus in the fleet (both electric and diesel) to serve specific trips while:
- Minimizing total operational costs (fuel, charging, and other fixed costs).
- Respecting the capacity constraints of charging stations.
- Ensuring that each route has at least one bus assigned and that each bus has enough fuel or charge for its routes.

**Variables**:
- `x_e[bus_id, trip_id]`: Binary variable representing whether electric bus `bus_id` is assigned to `trip_id`.
- `x_d[bus_id, trip_id]`: Binary variable for diesel buses, indicating if `bus_id` serves `trip_id`.
- `charge[bus_id, t]`: Binary variable representing if electric bus `bus_id` is scheduled to charge at time `t`.
- `refuel[bus_id, t]`: Binary variable for diesel buses, representing refueling events.
- `z_e[bus_id]`, `z_d[bus_id]`: Binary variables tracking whether electric or diesel buses are active for scheduling purposes.

---

## 3. Constraints

1. **Trip Completion Constraint**: Ensures each trip is served by one bus, either electric or diesel.

   \[
   \sum_{e \in \text{electric\_buses}} x_e[e, \text{trip}] + \sum_{d \in \text{diesel\_buses}} x_d[d, \text{trip}] = 1, \quad \forall \text{trip} \in \text{trips}
   \]

2. **Fleet Size Constraint**: Limits the usage of electric and diesel buses to the available fleet.

   \[
   \sum_{e \in \text{electric\_buses}} z_e[e] \leq \text{total\_electric\_buses}
   \]
   \[
   \sum_{d \in \text{diesel\_buses}} z_d[d] \leq \text{total\_diesel\_buses}
   \]

3. **Energy Management Constraints**:
   - **Electric Buses**: Each electric bus must have sufficient charge for its trips. For a given `trip_id` assigned to an electric bus `e`, this constraint ensures enough remaining charge:

     \[
     x_e[e, \text{trip\_id}] \cdot \text{battery\_capacity}[e] \geq \text{distance}[ \text{trip\_id}] \cdot \text{consumption\_rate}[e]
     \]

   - **Diesel Buses**: Each diesel bus must have enough fuel:

     \[
     x_d[d, \text{trip\_id}] \cdot \text{fuel\_capacity}[d] \geq \text{distance}[ \text{trip\_id}] \cdot \text{consumption\_rate}[d]
     \]

4. **Charger Capacity Constraint**: Limits the number of electric buses that can be charged simultaneously at the depot.

   \[
   \sum_{e \in \text{electric\_buses}} \text{charge}[e, t] \leq \text{charger\_capacity}, \quad \forall t
   \]

5. **Depot Return Constraint**: Ensures that each bus returns to the depot by the end of the day.

   \[
   x_e[e, \text{last\_trip}] = 1 \quad \text{and} \quad x_d[d, \text{last\_trip}] = 1
   \]

---

## 4. Objective Function

The objective is to **minimize the total operational costs**, which include the costs of charging electric buses, refueling diesel buses, and any fixed operational costs.

### Objective Function Formula

\[
\text{Minimize:} \sum_{e \in \text{electric\_buses}} \sum_{t=1}^{24} \text{charge}[e, t] \cdot (\text{fixed\_cost\_electric} + \text{unit\_cost\_electric}) + \sum_{d \in \text{diesel\_buses}} \sum_{t=1}^{24} \text{refuel}[d, t] \cdot (\text{fixed\_cost\_diesel} + \text{unit\_cost\_diesel})
\]

Where:
- **Fixed Cost Electric** and **Fixed Cost Diesel** are fixed costs per charging or refueling event.
- **Unit Cost Electric** and **Unit Cost Diesel** are per-unit energy costs for electric charging and fuel refilling.

---

## 5. Methodology

### Mixed Integer Linear Programming (MILP)
This problem is formulated as a MILP, where binary variables track whether a bus serves a specific trip and whether it is scheduled to charge or refuel. Constraints manage resource limitations and enforce the required service.

### Column Generation Technique
Given the large number of buses and trips, solving the full MILP directly would be computationally intensive. To make the solution more feasible, we implemented **column generation**.

#### Column Generation Steps:
1. **Initialization**:
   - Start with a restricted set of bus-trip assignments, solving only a subset of potential assignments.
   - Set an initial fraction of assignments to create a reduced problem size.

2. **Solve the Restricted Problem**:
   - Use the initial subset to solve a smaller problem. This restricted model is solved iteratively, only focusing on the selected assignments.

3. **Add New Columns**:
   - After each restricted problem solution, identify **unserved trips** and **cost-reducing assignments**.
   - For each unserved trip, a bus-trip assignment is added, expanding the model iteratively.

4. **Check Convergence**:
   - The column generation process continues until the improvement in the objective function is below a specified tolerance, indicating that additional columns would not significantly reduce costs.

---

## 6. Optimization and Scalability

### Column Generation Benefits
Column generation reduces memory and computational requirements by focusing only on a subset of assignments initially. This allows us to start with a manageable problem size and gradually add assignments as needed.

### Termination Criteria
To prevent excessive computation, we define a tolerance level for the improvement of the objective function. Once improvements drop below this threshold, the process stops, ensuring computational efficiency.

---

## 7. Results and Interpretation

### Example Results
The column generation approach provides an efficient solution for assigning buses to trips with minimized operational costs. The final output includes:
- **Bus Assignments**: Each bus’s assigned trips.
- **Total Operational Costs**: The minimized cost of charging and refueling, as well as any other fixed operational costs.

This approach balances the trade-off between accuracy and computational efficiency, making it a viable option for large urban transportation networks.

---

## 8. Conclusion

The routing optimization model, enhanced with column generation, efficiently handles the scheduling of a mixed fleet of buses while minimizing operational costs. This iterative approach allows for scalability, enabling real-world application in large-scale transit systems.
