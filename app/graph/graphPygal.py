import pygal

from pygal.style import Style

def makeGraph(graphTitle, yTitle, xLabels, yValues, yLegend):
    # Define the style
    custom_style = Style(
        colors=('#00FF00', '#e50000', '#ffff14', '#929591'),
        font_family='Roboto,Helvetica,Arial,sans-serif',
        background='transparent',
        label_font_size=14,
    )

    # Set up the bar plot, ready for data
    c = pygal.Bar(
        title=graphTitle,
        style=custom_style,
        y_title=yTitle,
        width=1200,
        x_label_rotation=270,
    )
    
    c.add(yLegend, yValues)
    #c.add('Labour', df['labour'])
    #c.add('Liberal', df['liberal'])
    #c.add('Others', df['others'])

    # Define the X-labels
    c.x_labels = xLabels

    # Write this to an SVG file
    #c.render_to_file('pygal.svg')
    return c.render_response()

def makeGraphYearByYear(graphTitle, yTitle, xLabels, data):
    # Define the style
    custom_style = Style(
        colors=('#00FF00', '#00CCCC', '#ffff14', '#929591'),
        font_family='Roboto,Helvetica,Arial,sans-serif',
        background='transparent',
        label_font_size=14,
    )
    # Set up the bar plot, ready for data
    c = pygal.Bar(
        title=graphTitle,
        style=custom_style,
        y_title=yTitle,
        width=1200,
        x_label_rotation=270,
    )
    
    for year in data.keys():
        thisYear = data[year]
        print(f"This year {thisYear}")
        print("May: {}".format(data[year].get("5")))
        january = thisYear.get('1',None)
        february = thisYear.get('2',None)
        march = thisYear.get('3',None)
        april = thisYear.get('4',None)
        may = thisYear.get("5",None)
        june = thisYear.get('6',None)
        july = thisYear.get('7',None)
        august = thisYear.get('8',None)
        september = thisYear.get('9',None)
        october = thisYear.get('10',None)
        november = thisYear.get('11',None)
        december = thisYear.get('12',None)
        values = [ january, february, march, april, may, june, july, august, september, october, november, december]
        legend = str(year)
        print(f"Adding Legend {legend} with values {values}")
        c.add(legend, values)
    #c.add('Labour', df['labour'])
    #c.add('Liberal', df['liberal'])
    #c.add('Others', df['others'])

    # Define the X-labels
    c.x_labels = 'Jan','Feb','Mar','Apr','Maj','Jun','Jul','Aug','Sep','Okt','Nov','Dec'

    # Write this to an SVG file
    #c.render_to_file('pygal.svg')
    return c.render_response()