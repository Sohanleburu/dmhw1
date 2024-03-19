import streamlit as st
import pandas as pd
from google.cloud import bigquery
import os
import plotly.express as px  # Import Plotly Express


# Set the path to your service account key
service_account_key_path = 'bigquery-255-ea3327f6e00b.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key_path

# Generalized function to load data from BigQuery
def load_data_from_bigquery(query):
    project_id = 'bigquery-255'
    client = bigquery.Client(project=project_id)
    dataframe = client.query(query).to_dataframe()
    return dataframe

# Query for top 10 programming tags
top_tags_query = """
SELECT flattened_tags, count(*) as tag_count from 
(select split(tags , '|') as tags FROM `bigquery-public-data.stackoverflow.posts_questions` 
Where EXTRACT (YEAR from creation_date) >= 2008)
cross join unnest(tags) as flattened_tags
group by flattened_tags
order by tag_count desc
limit 10
"""

# Query for yearly count of questions with 'javascript' tag
javascript_trend_query = """
SELECT 
    EXTRACT(YEAR FROM creation_date) AS year, 
    COUNT(*) AS total_questions
FROM 
    `bigquery-public-data.stackoverflow.posts_questions`
WHERE 
    tags LIKE '%javascript%' 
GROUP BY 
    year
ORDER BY 
    year;
"""

# Query for the histogram data of answer count
answer_count_histogram_query = """
SELECT 
    answer_count, 
    COUNT(*) AS number_of_questions
FROM 
    `bigquery-public-data.stackoverflow.posts_questions`
WHERE 
    answer_count <= 20
GROUP BY 
    answer_count
ORDER BY 
    answer_count;
"""

# Add the query for analyzing the relationship between score and view count for JavaScript questions
score_view_count_query = """
SELECT 
    score, 
    view_count
FROM 
    `bigquery-public-data.stackoverflow.posts_questions`
WHERE 
    tags LIKE '%javascript%'
    AND EXTRACT(YEAR FROM creation_date) >= 2008
    AND score > 0
    AND view_count <= 10000
LIMIT 1000;
"""


# Load data for each query
top_tags_df = load_data_from_bigquery(top_tags_query)
javascript_trend_df = load_data_from_bigquery(javascript_trend_query)
answer_count_histogram_df = load_data_from_bigquery(answer_count_histogram_query)
score_view_count_df = load_data_from_bigquery(score_view_count_query)

# Visualize Top 10 Programming Languages Tags with Plotly
import plotly.express as px
import streamlit as st

# Assuming top_tags_df is your DataFrame and it's structured correctly
# with 'flattened_tags' and 'tag_count' columns.

fig_top_tags = px.bar(top_tags_df, x='flattened_tags', y='tag_count', 
                      labels={'flattened_tags': 'Programming Language', 'tag_count': 'Number of Questions'}, 
                      title='Top 10 Programming Languages Tags', color_discrete_sequence=['red'])

st.plotly_chart(fig_top_tags)



# Visualize Javascript Questions Trend with Plotly as a Pie Chart
fig_javascript_trend_pie = px.pie(javascript_trend_df, names='year', values='total_questions', 
                                  title='Distribution of Stack Overflow Questions with "javascript" Tag by Year',
                                  color_discrete_sequence=px.colors.sequential.Reds)
st.plotly_chart(fig_javascript_trend_pie)



import plotly.express as px
import streamlit as st

# Assuming answer_count_histogram_df is your DataFrame and it's structured correctly
# with 'answer_count' and 'number_of_questions' columns.

fig_answer_count_scatter = px.scatter(answer_count_histogram_df, x='answer_count', y='number_of_questions', 
                                      labels={'answer_count': 'Number of Answers', 'number_of_questions': 'Number of Questions'}, 
                                      title='Distribution of Number of Answers per Question', 
                                      color_discrete_sequence=['red'])

st.plotly_chart(fig_answer_count_scatter)


import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Assuming 'dataframe' has columns 'score' and 'view_count'
# Example DataFrame creation (if your 'dataframe' variable isn't defined yet)
# This is just an example and should be replaced with your actual DataFrame loading or creation code
data = {
    'score': [1, 2, 3],  # Example scores
    'view_count': [100, 150, 200]  # Example view counts
}
dataframe = pd.DataFrame(data)

# Make sure this variable is defined before using it in the histogram plot
# This approach weights the view_count by the score, repeating view_count values 'score' times
data_for_histogram = np.repeat(dataframe['view_count'], dataframe['score'])

# Convert the array back to a DataFrame for Plotly
histogram_df = pd.DataFrame(data_for_histogram, columns=['Weighted View Count'])

# Now, you can plot the histogram using Plotly Express
fig = px.histogram(histogram_df, x='Weighted View Count', 
                   nbins=30, color_discrete_sequence=['red'])

# Updating layout for better visualization
fig.update_layout(
    title='Histogram of JavaScript Questions by Weighted View Count',
    xaxis_title='Weighted View Count',
    yaxis_title='Frequency of Questions',
    bargap=0.2,  # Gap between bars
)

# Display the plot in Streamlit
st.plotly_chart(fig)


