import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/labidimedaziz/renderboxing/main/working_data.csv')
df["ko_percentage"] = df["Wins by KO"] / df["Wins"].where(df["Wins"] > 0, 0)

# Combine sex and weight class into a single column for labeling
df["sex_weight_class"] = df["Sex"] + " - " + df["Weight_class"]

# Group by sex_weight_class and calculate average knockout percentage
avg_ko_per_sex_weight_class = df.groupby("sex_weight_class")["ko_percentage"].mean()

# Sort by average KO percentage in descending order
avg_ko_per_sex_weight_class = avg_ko_per_sex_weight_class.sort_values(ascending=False)

# Create bar plot using Plotly Express



# Initialize the Dash app
load_figure_template("sketchy")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY], assets_folder='assets')
server = app.server
fig_ko = px.bar(
    avg_ko_per_sex_weight_class.reset_index(),  # Reset index for labels
    x="sex_weight_class",
    y="ko_percentage",
    title="Average KO Percentage by Sex and Weight Class",
    color_discrete_sequence=['#1f77b4'],
    opacity=0.7
)
from PIL import Image
#pil_image = Image.open(r"src\assets\Cassius.png")
# Custom styles
colors = {
    'background': '#f0f0f0',  # Light gray background
    'text': '#333333',  # Dark gray text
    'accent': '#003f5c',  # Navy blue accent color
}
# Define weight class categories for sorting (male and female)
weight_categories_male = [
    'minimumweight', 'flyweight', 'bantamweight', 'featherweight',
    'lightweight', 'welterweight', 'middleweight', 'cruiserweight', 'heavyweight'
]
weight_categories_female = [
    'minimumweight', 'flyweight',
    'bantamweight',  'featherweight', 
    'lightweight',  'welterweight', 'middleweight', 'heavyweight'
]

# Function to get weight class options based on sex
def get_weight_options(sex):
    if sex == 'M':
        weight_categories = weight_categories_male
    else:
        weight_categories = weight_categories_female
    weight_options = [{'label': weight, 'value': weight} for weight in weight_categories]
    return weight_options


# Create choropleth map figure
fig_choropleth = px.choropleth(
    data_frame=df,
    locations=df['Country'].value_counts().index,
    locationmode='country names',
    color=df['Country'].value_counts().values,
    color_continuous_scale='blues',  # Blue color scale
    labels={'color': 'Boxer Count'},  # Label for the color scale
    projection='natural earth',
    height=730,
)
fig_choropleth.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Adjust margins for better layout
    geo=dict(
        showcoastlines=True,  # Show coastlines for better context
        coastlinecolor=colors['accent'],  # Accent color for coastlines
        showland=True,  # Show land areas
        landcolor=colors['background'],  # Light gray background for land areas
    ),
    title={
        'text': "Boxer Nationalities",
        'y': 0.95,
        'x': 0.45,
        'font': {'color': colors['text']}
    }
)
#fig_heightxreach = px.scatter(df, x='Height_cm', y='Reach_cm', title='Height vs Reach',
#                             labels={'x': 'Height', 'y': 'Reach'}, color_discrete_sequence=['#1f77b4'],
#                             opacity=0.7,  trendline="ols")
#fig_heightxreach.update_layout(
#    xaxis=dict(showgrid=False),  # Remove gridlines from x-axis
#    yaxis=dict(showgrid=False)   # Remove gridlines from y-axis
#)

# Create bar chart figure for zodiac signs
sign_counts = df['Sign'].value_counts()

# Sort sign counts in descending order
sorted_sign_counts = sign_counts.sort_values(ascending=False)

# Get sign names in sorted order
sorted_sign_names = sorted_sign_counts.index

fig_zodiac = px.histogram(
    df, 
    x='Sign', 
    category_orders={'Sign': sorted_sign_names},
    
    color_discrete_sequence=['#1f77b4'], 
    opacity=0.7,
    title='Zodiac Signs Distribution',
    labels={'x': 'Zodiac Sign', 'y': 'Count'}
)

# Count the occurrences of each nationality
nationality_counts = df['Nationality'].value_counts()

# Select the top 10 nationalities
top_10_nationalities = nationality_counts.head(10)

# Create a DataFrame with the top 10 nationalities and their counts
top_10_df = pd.DataFrame({'Nationality': top_10_nationalities.index, 'Count': top_10_nationalities.values})

# Sort the DataFrame by count in descending order
top_10_df = top_10_df.sort_values(by='Count', ascending=False)

# Create a bar plot using Plotly Express
countries = px.bar(top_10_df, x='Nationality', y='Count', title='Top 10 Nationalities',
             labels={'Nationality': 'Nationality', 'Count': 'Count'},color_discrete_sequence=['#1f77b4'],
    opacity=0.5)
#countries = px.bar(
#    df[df["Country"].isin(top_10_nationalities.index)],
#    x="Country",
#    
#    title="Nationality distribution of titleholders",
#    color_discrete_sequence=['#1f77b4'],
#    opacity=0.7
#)
height_fig = px.histogram(df, x='Height_cm', title='Height Distribution Across All Weight Classes and Sexes',color_discrete_sequence=['#1f77b4'],
    opacity=0.7, height=300)
reach_fig = px.histogram(df, x='Reach_cm', title=f'Reach Distribution Across All Weight Classes and Sexes',color_discrete_sequence=['#1f77b4'],
    opacity=0.7, height=300)


# Define app layout
app.layout = html.Div( children=[
    html.H1("Boxing Analytics", style={'textAlign': 'center', 'margin-bottom': '20px'}),
    html.Div(className="col-md-12 col-lg-12 mb-md-2 mb-4 card-chart-container", children=[

  html.Div(className="card", children=[

    dbc.Row([

      dbc.Col(className="col-lg-9", children=[

        html.Br(),
        

        html.Span(
          "Boxing By the Stars: Fact or Fiction?",
          style={"color": "#0084d6", "font-size": "1.5vw"}  
        ),
        html.Br(),
        

        html.P(["Ever heard someone claim their horoscope sign makes them a natural-born fighter? Well, the famous trainer cus d'eamato said that. While intriguing, this sparked a different question:  Does data reveal any truth behind these claims?  We set out to explore the characteristics of champions,  using data analysis to see if there's a science behind boxing success – beyond the stars.  This dashboard is dedicated to analyzing the characteristics of boxing champions. We delve into the science of boxing success, going beyond the stars. Explore the data to uncover valuable insights into the physical attributes, backgrounds, and distinguishing features of boxing's elite. Check the discussion and results in",
          
          html.A("Discussion.", href="/Results", style={"color": "#0084d6"}),
          
          html.P("*Note: dashboard only covers data up to the beginning of 2024.", className="mt-1")
        ], className="card-text")

      ]),

      dbc.Col(className="col-lg-3", children=[
        #html.Img(src=pil_image, className="img-fluid")  
      ], style={"align-self": "self-end"})

    ])

  ])
  
])
,
html.H3("I.     Dashboard", style={'textAlign': 'left', 'padding-top': '20px'}),
    
dbc.Row([
        dbc.Col(  # Chloroplast map on the left
            dcc.Graph(figure=fig_choropleth, style={'textAlign': 'center'} ,className="card"),
            lg=6
        ),
        dbc.Col(children=[  # Histograms and dropdown on the right
            

            html.Div([
                dcc.Dropdown(
                    id='sex-dropdown',
                    options=[
                        {'label': 'Male', 'value': 'M'},
                        {'label': 'Female', 'value': 'F'}
                    ],
                    value='M',
                    clearable=False,
                    style={'margin-right': '20px', 'backgroundColor': '#ffffff', 'color': colors['text']}, className="card"
                ),
                dcc.Dropdown(
                    id='weight-dropdown',
                    placeholder="Select weight class",
                    clearable=False,
                    style={'margin-right': '20px', 'backgroundColor': '#ffffff', 'color': colors['text']}, className="card"
                ),
            ], style={'margin-bottom': '20px'}),

            html.Div([
                dcc.Graph(id='height-graph', className="card mt-4"),
                dcc.Graph(id='reach-graph', className="card mt-4"),
            ], style={'justify-content': 'space-between', 'margin-bottom': '30px'})
        ], lg=6)
    ]),
    #html.Div([
    #    dcc.Graph( figure=fig_heightxreach)
    #], style={'margin-bottom': '30px'}),
#    Notice that the slope is 1.06 indicating that on average, champions have a slightly higher reach than their
    #    height compared the general population.
   
    dbc.Row([dbc.Col(
        dcc.Graph(id='zodiac_freq', figure=fig_zodiac, className="card")),
    dbc.Col(
        dcc.Graph( figure=fig_ko, className="card"))]),
        html.H3("II.     Discussion", style={'textAlign': 'left', 'padding-top': '20px'}),
        dcc.Markdown("""
        ##### •Project Context:
        I have been a passionate follower of boxing for the past five or six years,
        even undergoing training at one point. One question that has always intrigued me is whether
        height and reach provide a competitive advantage in the sport.
        While most people would agree that they do, there have been outliers such as Mike Tyson who was able 
        to consistently defeat opponents much taller than him despite his shorter stature.
        During a recent podcast featuring Teddy Atlas, Tyson's former coach, he mentioned a theory from Cus D'Amato 
        that certain astrological signs, including Aquarius, Capricorn, Taurus, and Cancers, "make good boxers".
        Me being a firm non-believer in astrology, decided to delve into an analysis of boxing champions to answer these questions:
                     
        1. Which countries emerge as the primary producers of titleholders?
                     
        2. How does the height and reach of boxing champions compare to individuals of similar weight in the general population?
                     
        3. Is there a discernible trend indicating that individuals born under certain zodiac signs, such as Aquarius, Capricorn, Taurus, and Cancer,
        tend to excel in the sport?

        ##### • Data Collection:
        I didn't find a good dataset for this project, so I scraped the web for data on boxing champions.
        First, I collected the names of the titleholders for the 4 major organizations (WBA, WBC, WBO, and IBF), 
        the Ring Magazine, and the IBO organization. I also collected some data on Olympic boxers (though limited 
        due to the unpopularity of Olympic boxing). Then I scraped the needed data from their Wikipedia pages.

        ##### • Data Cleaning:
        The data was really messy, so I had to do some cleaning. Extracted the country from the birth address, 
        normalized the height and reach to metric units, removed the duplicates, and added columns like sex and the astrological sign.

        ##### • Analysis and Results:
        •  First, let's see the nationality distribution of the titleholders.
    """
            , style={'margin-bottom': '30px'}),
        dcc.Graph(figure=countries),
        dcc.Markdown("""- USA, Mexico, and UK are expected. I was surprised, though, by seeing Japan and not seeing Russia."""),
                     
        dcc.Markdown("""•    Height && Reach """),
                     

        dbc.Row([dbc.Col(dcc.Graph(figure=height_fig), lg=6),
        dbc.Col(dcc.Graph(figure=reach_fig), lg=6)]),
        dcc.Markdown("""-   It's evident that champion boxers, regardless of sex and weight class, tend to hover around an average height of 
                     approximately 170 cm, slightly surpassing the global average of 168 cm. At first glance, this might suggest that height 
                     isn't a significant factor in boxing success. However, looking at the distribution of reach, we can see the average reach 
                     among champion boxers sits closer to 180 cm. This discrepancy between height and reach indicates 
                     that while height alone may not be a defining factor, reach indeed plays a pivotal role. This observation gains significance
                      when considering the global trend, where people typically maintain a proportional 1:1 relationship between height and reach. 
                     Hence, the reach emerges as a crucial factor influencing competitive advantage. 
                     """
                     ),
                     dcc.Markdown("""•     Zodiac Signs """),

            dcc.Graph(figure=fig_zodiac),
            dcc.Markdown("""-   IT's evident that there is no relationship between zodiac signs and the ability to excel in Boxing. Sorry Cus!""")

    

])



# Define callback to update weight dropdown options based on selected sex
@app.callback(
    Output('weight-dropdown', 'options'),
    [Input('sex-dropdown', 'value')]
)
def update_weight_options(selected_sex):
    return get_weight_options(selected_sex)

sex_mapping = {'M': 'Male', 'F': 'Female'}
colors = ['#1f77b4', '#ff7f0e']
# Define callback to update graph based on selected sex and weight class
@app.callback(
    Output('height-graph', 'figure'),
    Output('reach-graph', 'figure'),
    [Input('sex-dropdown', 'value'),
     Input('weight-dropdown', 'value')]
)
def update_graph(selected_sex, selected_weight):
    filtered_df = df[(df['Sex'] == selected_sex) & (df['Weight_class'] == selected_weight)]
    fig_h = px.histogram(filtered_df, x='Height_cm', title=f'Height distribution for {sex_mapping[selected_sex]} {selected_weight}',color_discrete_sequence=colors,
    opacity=0.7, height=300)
    fig_r = px.histogram(filtered_df, x='Reach_cm', title=f'Reach distribution for {sex_mapping[selected_sex]} {selected_weight}',color_discrete_sequence=colors,
    opacity=0.7, height=300)
    return fig_h, fig_r


if __name__ == '__main__':
    app.run_server(debug=True)
