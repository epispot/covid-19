import epispot as epi

sf = open('formatted/sf-hospitalizations.csv').readlines()
ny = open('formatted/ny-hospitalizations.csv').readlines()
london = open('formatted/london-hospitalizations.csv').readlines()
tokyo = open('formatted/tokyo-hospitalizations.csv').readlines()

"""
City populations (for scaling data):
    Tokyo: 9.273 million
    London: 8.982 million
    New York: 8.399 million
    San Francisco: 883,305
"""

tokyo_pop = 9.273e6
london_pop = 8.982e6
ny_pop = 8.399e6
sf_pop = 883305

for el in range(0, len(sf)):
    sf[el] = float(sf[el]) / sf_pop

for el in range(0, len(ny)):
    ny[el] = float(ny[el]) / ny_pop

for el in range(0, len(london)):
    london[el] = float(london[el]) / london_pop

for el in range(0, len(tokyo)):

    str = "".join( list( tokyo[el] )[:-1] )
    str = str.replace(',', '')
    tokyo[el] = float(str) / tokyo_pop

"""
Start & End Dates:
    San Francisco: 3/23/20-12/04/20
    New York: 9/04/20-12/03/20
    London: 8/01/20-12/04/20
    Tokyo: 3/04/20-12/04/20
Combined (for graph-[max-min]): 
    3/04/20-12/04/20 
These will be shown as day 0 & day 275
"""

trends = [[range(19, 276), sf, 'San Francisco'], [range(184, 275), ny, 'New York'], [range(150, 276), london, 'London'],
          [range(0, 276), tokyo, 'Tokyo']]
epi.plots.compare(trends, 'COVID-19-related Hospitalizations', 'In Major Cities around the World since 3/04/20',
                  seed=1000)

print('Process finished. Restart and select `save` on the matplotlib windows to save plot images.')
print('Made with epispot.')
