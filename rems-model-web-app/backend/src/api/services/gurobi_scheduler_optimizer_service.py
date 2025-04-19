import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np


class GurobiSchedulerOptimizerService:
    """
    This class is a Service which abstracts the initialization and 
    execution of a gurobi linear integer programming model which is used
    to find an optimal scheduling assignment for REMS.
    """
    def __init__(self, names, emails, role_statuses, oc_statuses, availability, dates):
        self.names = names
        self.emails = emails
        self.role_statuses = role_statuses
        self.oc_statuses = oc_statuses
        self.availability = availability
        self.dates = dates

        self.num_people = availability.shape[0]
        self.num_shifts = availability.shape[1]


    def initialize_model(self):
        # model initialization w/ decision vars
        model = gp.Model("REMS")

        # Binary variable for shift assignment
        x = model.addVars(self.num_people, self.num_shifts, vtype = GRB.BINARY, name = "x")

        # Buffer for no more than three people being assigned to a signle shift
        b = model.addVars(self.num_shifts, vtype = GRB.INTEGER, lb = 0, name = "b")

        # Buffer for penalizing people not being assigned to two shifts
        m = model.addVars(self.num_people, vtype = GRB.INTEGER, lb = 0, name = "m")

        # Objective function 
        model.setObjective(sum(m[i] for i in range(self.num_people)) + sum(b[j] for j in range(self.num_shifts)),
                           GRB.MINIMIZE)
        
        # Constraint: No more than 2 duty crew members to 1 shift
        for shift in range(self.num_shifts):
            model.addConstr(sum(x[person, shift]*self.role_statuses[person] for person in range(self.num_people)) + b[shift] == 2)
        # Constraint: No more than 3 total members to 1 shift
        for shift in range(self.num_shifts):
            model.addConstr(sum(x[person, shift] for person in range(self.num_people)) + b[shift] <= 3)
        # Constraint: No more than 2 shifts assigned to 1 person
        for person in range(self.num_people):
            model.addConstr(sum(x[person, shift] for shift in range(self.num_shifts)) + m[person] == 2)
        # Constraint: No more than 2 Off Campus members assigned to 1 shift
        for shift in range(self.num_shifts):
            model.addConstr(sum(x[person, shift]*self.oc_statuses[person] for person in range(self.num_people)) <= 2)
            
        return model, x

    def generate_optimized_schedule(self):
        """
        Generates an optimal schedule in ___ format.
        """
        model, x = self.initialize_model()
        model.optimize()

        x_values = np.zeros((self.num_people, self.num_shifts))

        # populate numpy array with scheduled values
        for person in range(self.num_people):
            for shift in range(self.num_shifts):
                x_values[person, shift] = x[person, shift].X

        # build interpretable schedule for calendar output
        schedule = []
        for person in range(self.num_people):
            for shift in range(self.num_shifts):
                if x_values[person, shift] > 0:
                    schedule.append({
                        "first_name": self.names[person][0],
                        "last_name": self.names[person][1],
                        "email": self.emails[person],
                        "shift": self.dates[shift]
                    })
        return schedule



        
