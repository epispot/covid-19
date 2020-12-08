import epispot as epi  # load the epi-spot package
from copy import deepcopy


def get_model_predictions(params, return_model=False):

    """with standard values
    p_r_0 = 2.5
    p_delta = 0.5
    p_gamma = 0.2
    p_alpha = 0.01
    """

    p_r_0 = params[0]
    p_delta = params[1]
    p_gamma = params[2]
    p_alpha = params[3]


    # variables (used when defining layers)

    # basic reproductive number
    def R_0(t):
        return p_r_0

    # all other variables are not time dependent (this is not required)

    # recovery rate
    def gamma(t):
        return p_gamma

    # total population
    def N(t):
        return 3711

    # probability of recovering
    def p_recovery(t):
        return 1.0

    def delta(t):
        return p_delta

    def alpha(t):
        return p_alpha

    # layers
    Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
    Exposed = epi.comps.Exposed(1, R_0, gamma, N, delta)
    Infected = epi.comps.Infected(2, N, delta=delta, p_recovery=p_recovery, recovery_rate=gamma,
                                  p_death=alpha, death_rate=gamma)  # Infected layer
    Recovered = epi.comps.Recovered(3, p_from_inf=p_recovery, from_inf_rate=gamma)  # Recovered layer
    Dead = epi.comps.Dead(4, rho_inf=gamma, alpha_inf=alpha)  # Recovered layer

    # the blank array in `layer_map` symbolizes that the Recovered layer has no further layers
    Model = epi.models.Model(N(0), layers=[Susceptible, Exposed, Infected, Recovered, Dead],
                             layer_names=['Susceptible', 'Exposed', 'Infected', 'Recovered', 'Dead'],
                             layer_map=[[Exposed], [Infected], [Recovered, Dead], [], []])

    if return_model:
        return Model

    result = Model.integrate(range(0, 30), starting_state=[3710, 1, 0, 0, 0])
    formatted_res = []
    for system in result:
        formatted_res.append([system[0], system[2], system[4]])
    return formatted_res


parameters = [2.5, 0.5, 0.2, 0.01]  # R_0, delta, gamma, alpha
new_params = epi.fitters.grad_des(get_model_predictions, open('formatted/diamond-princess.csv'), parameters,
                                  10.0, 2, 3711, [0, 26], verbose=False)
new_params[-1] = 0.01

print('Optimized parameters found at:')
print(new_params)

# print('\nPlotting current coronavirus data in San Francisco (on log scale) ↗')
# print('Estimated coronavirus cases will be plotted after window is closed.')

data_timerange = range(0, 115)
file = open('formatted/sf-total-cases.csv').readlines()
data1 = [float(x.split(',')[0]) for x in file[1:]]
data2 = [float(x.split(',')[1]) for x in file[1:]]

# epi.plots.compare([[data_timerange, data1, 'Susceptibles (from data)'], [data_timerange, data2,
#                                                                          'Infecteds (from data)']])

# print('Plotting estimated coronavirus cases after restrictions are removed ↗')
# print('Estimated cases will be plotted against actual figures after window is closed.')

p_r_0 = new_params[0]
p_delta = new_params[1]
p_gamma = new_params[2]
p_alpha = new_params[3]

# variables (used when defining layers)


# basic reproductive number
def R_0(t):
    return p_r_0


# all other variables are not time dependent (this is not required)

# recovery rate
def gamma(t):
    return p_gamma


# total population
# San Francisco total population: 883,305
def N(t):
    return 883305


# probability of recovering
def p_recovery(t):
    return 1.0


def delta(t):
    return p_delta


def alpha(t):
    return p_alpha


"""
MODEL STARTS FROM DAY #116--DATE: 7/12/20
MODEL END DATE: 8/10/20
PARAMETERS ARE TAKEN FROM THE OPTIMIZATION PROCESS ABOVE
"""

Susceptible = epi.comps.Susceptible(0, R_0, gamma, N)  # Susceptible layer
Exposed = epi.comps.Exposed(1, R_0, gamma, N, delta)  # Exposed layer
Infected = epi.comps.Infected(2, N, delta=delta, p_recovery=p_recovery, recovery_rate=gamma,
                              p_death=alpha, death_rate=gamma)  # Infected layer
Recovered = epi.comps.Recovered(3, p_from_inf=p_recovery, from_inf_rate=gamma)  # Recovered layer
Dead = epi.comps.Dead(4, rho_inf=gamma, alpha_inf=alpha)  # Recovered layer

# the blank array in `layer_map` symbolizes that the Recovered layer has no further layers
San_Francisco_Model = epi.models.Model(N(116), layers=[Susceptible, Exposed, Infected, Recovered, Dead],
                         layer_names=['Susceptible', 'Exposed', 'Infected', 'Recovered', 'Dead'],
                         layer_map=[[Exposed], [Infected], [Recovered, Dead], [], []])

# assumes best-case scenario: 0 exposed, 0 recovered
# plotting until 12/31/20
# epi.plots.plot_comp_nums(San_Francisco_Model, range(0, 58), starting_state=[878875, 0, 4430, 0, 50], seed=400)

print('Plotting comparison ↗')

system_integral = San_Francisco_Model.integrate(range(0, 30), starting_state=[878875, 0, 4430, 0, 50])
predicted_infecteds = []

for timestep in system_integral:
    predicted_infecteds.append(deepcopy(timestep[2]))

data2_hos = deepcopy(data2)
predicted_infecteds_hos = deepcopy(predicted_infecteds)

for i in range(len(data2_hos)):
    data2_hos[i] *= 0.052

for i in range(len(predicted_infecteds_hos)):
    predicted_infecteds_hos[i] *= 0.052

range_container = [[data_timerange, data1, 'Susceptibles (from data)'], [data_timerange, data2,
'Infecteds (from data)'], [data_timerange, data2_hos, 'Estimated Hospitalized (from data)'],
[range(116, 146), predicted_infecteds, 'Predicted Infecteds'],
[range(116, 146), predicted_infecteds_hos, 'Predicted Hospitalized']]

epi.plots.compare(range_container, title='Coronavirus Data', subtitle="San Francisco (3/19-8/10)",
markers=[['line', [1897, 0, 146, 'Hospital Capacity']], ['highlighted-box', [122, 135, 0.5, 1]],
['point', [' Triage Required', 122, 1897]]], seed=310)

print('Process finished. Restart and select `save` on the matplotlib windows to save plot images.')
print('Made with epispot.')
