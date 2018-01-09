import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os

app = dash.Dash()
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

OPTIONS = {
		'salary_total': 'Distribution of Salaries',
		'yrs_service': 'Distribution of Years of Service',
		'rank_salary_distribution': 'Rank based Salary distribution',
		'gender_rank': 'Gender in ranked categories',
		'gender_salary': 'Gender based Salary distribution'
}



app.layout = html.Div(children=[
	dcc.Markdown('''
## 2008 - 2009 Academic Salary comparison in U.S.
				  
Podle dat [Salaries for Professors](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/car/Salaries.csv)
	'''),

	dcc.Graph(
		id='example-graph',
		figure = {
			'data': [],
			'layout': {
				'title': ''
			}
		}
	),
   
	 html.Label('Vyberte typ grafu'),
	dcc.Dropdown(
		id = 'chooser',
		options = [{'label': label, 'value': key} for key, label in OPTIONS.items()],
		value = 'salary_total'
	)
])

@app.callback(
	dash.dependencies.Output(component_id='example-graph', component_property='figure'),
	[dash.dependencies.Input(component_id='chooser', component_property='value')],
)
def update_figure(choice):
	figure = {
			'data': [],
			'layout': go.Layout(title = OPTIONS[choice])
	}
	
	if choice == 'salary_total':
		x = academic_salary.salary
		#second_fare = titanic[titanic.pclass == 2].fare
		#third_fare = titanic[titanic.pclass == 3].fare

		plot_function = go.Histogram #if plot_type == 'hist' else go.Box
		trace1 = plot_function(x = x, opacity = 0.75, name = 'Salaries')
		#trace2 = plot_function(x = second_fare, opacity = 0.75, name = 'Druhá třída')
		#trace3 = plot_function(x = third_fare, opacity = 0.75, name = 'Třetí třída')

		data = [trace1]

		figure={
			'data': data,
			'layout': {
				'height' : 600,
				'width' : 900,
				'title': '<b>US college Total Salary distribution</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Salaries (nine-month salary total, in USD)'),
				'yaxis' : dict(
					title = 'Frequency of Salaries')
			},

		}

	elif choice == 'yrs_service':
		x = academic_salary['yrs.service']

		plot_function = go.Histogram
		trace1 = plot_function(x = x, opacity = 0.75, name = 'Years of Service')

		data = [trace1]

		figure={
			'data': data,
			'layout': {
				'height' : 600,
				'width' : 900,
				'title': '<b>US college Distribution of Years of Service</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Years of Service'),
				'yaxis' : dict(
					title = 'Frequency')
			},

		}

	elif choice == 'rank_salary_distribution':
		prof_salary = academic_salary[academic_salary['rank'] == 'Prof'].salary
		assocprof_salary = academic_salary[academic_salary['rank'] == 'AssocProf'].salary
		asstprof_salary = academic_salary[academic_salary['rank'] == 'AsstProf'].salary

		plot_function = go.Box
		trace1 = plot_function(x = prof_salary, opacity = 0.75, name = 'Prof', boxpoints = 'all')
		trace2 = plot_function(x = assocprof_salary, opacity = 0.75, name = 'AssocProf', boxpoints = 'all')
		trace3 = plot_function(x = asstprof_salary, opacity = 0.75, name = 'AsstProf', boxpoints = 'all')

		data = [trace1, trace2, trace3]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'overlay',
				'title': '<b>US college Rank based Salary distribution</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Salaries (nine-month salary total, in USD)'),
				
			},

		}

	elif choice == 'gender_rank':
		academic_salary_groupby = academic_salary.groupby(['rank', 'sex']).size().unstack(level = 1)
		df = academic_salary_groupby.iloc [[1,0,2]]


		plot_function = go.Bar
		trace1 = plot_function(x = df.index, y = df['Female'], opacity = 0.75, name = 'Female', marker = dict(color= 'rgb(252, 0, 120)'))
		trace2 = plot_function(x = df.index, y = df['Male'], opacity = 0.75, name = 'Male', marker = dict(color= 'rgb(0, 0, 255)'))
	

		data = [trace1, trace2]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'group',
				'title': '<b>US college Gender in ranked categories</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'xaxis' : dict(
					title = 'Rank'),
			},

		}

	elif choice == 'gender_salary':
		academic_salary_median = academic_salary.groupby(['rank', 'sex']).salary.median().unstack(level = 1)
		df = academic_salary_median.iloc[[1,0,2]]


		plot_function = go.Bar
		trace1 = plot_function(x = df.index, y = df['Female'], opacity = 0.75, name = 'Female', marker = dict(color= 'rgb(252, 0, 120)'))
		trace2 = plot_function(x = df.index, y = df['Male'], opacity = 0.75, name = 'Male', marker = dict(color= 'rgb(0, 0, 255)'))
	

		data = [trace1, trace2]

		figure={
			'data': data,
			'layout': {
				'barmode' : 'group',
				'title': '<b>US college Gender based Salary distribution</b>',
				'titlefont' : dict(
					size = 20, color = 'black'),
				'yaxis' : dict(
					title = 'Median Salary in USD'),
				'xaxis' : dict(
					title = 'Rank'),
			},

		}
	



	return figure

academic_salary = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/car/Salaries.csv')

if __name__ == '__main__':
	app.run_server()