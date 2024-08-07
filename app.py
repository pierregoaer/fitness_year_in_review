import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import gspread
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# TODO: switch to env variables for deployment
# from google_service_account import GOOGLE_SERVICE_ACCOUNT_CREDENTIALS

pd.set_option('display.max_columns', None)
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']

# --- Get Google Sheet ---
GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = {
    "type": "service_account",
    "project_id": "personal-strava-export-api",
    "private_key_id": "d9a959440b4db51b7dc181c969d5d8ac3a0ca1f7",
    "private_key": f"-----BEGIN PRIVATE KEY-----\n{os.environ['PRIVATE_KEY']}\nizy7Oxadpogay+sPs3asHQeR4IhilxrEDYF2WFTD8G+Ex6++v5590AXKDq4KCzDl\nKD8V5lnfI6jKjt00yxogHV6MkauL5V0VQ+HhNHpjCoy/8WIm+xtR3cQOQ+dPgtyt\nmk+q7cwcwl7Z5e+GvbmdE3QqbZUXNpicq8qTqckk0b+YZydfRs6v6XGE01j/5Zlx\nwwWAFwUk4FVJ+0dr2hRzljTIUIVJ6SzeiMFnj8vd0HhQSNRSMZlSp4LvU+J/5t0w\nyly8K+7VA+1t7ecvg3JOgZYM/JPW6/F3KNt8ky3YvDdX7jkXsW0kPHtYgP9rt1fI\nVBO3baA1AgMBAAECggEAI83WXPacylQrR+A5NVSVQZOLSXG5lYeEEv8Ep3grkV7W\nAIpX2iF0zwdj/vBsE5Z3hPlGVsAoEeOZEab1uAjC7M0OKZKN49U9RanMYwB5YkHz\nhLdl6A70X/x5drazJXmWzpkkgalo3DdG6g/3i82tvT50eNBh33BTZUIOOOPxYGkh\nwN975WGcnD1vCCvRHpaN4cZf9RaB9h4uahMhw6/fvF1r/zH4ebOuSG6McvvI5Hsg\nnkldUR6hRIYeKzb+TjtQZv8LplZBywuOAFiYEEyH0vG1YNCuaObfWvG8zsVz7b7k\nd4/dVPXT2zpaPUUHcm7wrldBISV9uVL4bmBe1KSUdQKBgQD5IfFYlerX1XZy4Iy7\nfso1cvOoGtCECXFByzXN0B0brS0/H+zkQOH0yAMs083q8wfdv/Nyh07aPpNWbbm6\nNWpq3FZEp2iArW+Euks3Dt/sYR3rZQAz9E/FK3K1kPX68caio/BDupdey3BJuuMY\n5KlHtnHVlnwMB5u3P2owxQvkLwKBgQDePBHQ3N+nU6pob6XKFTzPR3Iv3IPzlRbm\nlZDg6ppjfwy3WB9mQDWG0WC4l4gehXDaHepEncuOdKXzEHSnvb7eb4jzuA3L7C9C\n2h4FChk40hHvQahnUdKvpnUi7qkq16lPZXjUTJ4Lusd+OLng4/CASY8K9MIJr1w2\ngWxCxD5U2wKBgQCBRzPOHD15MrP8eLmOsgSMJ9J4cTGy0pOK6MBKxKvWKM9J6m8r\nIuAd/YxoPqCkQujaETlrPPuWFNKwDtBJ6F4Ihb3ecmCwJU+xOFq/f2CDcQHtnMO2\nMhkS37DutwJt7fh9fUS4YKMb9cWW/PvLdxzAsdPwWd6U/322YZnhJN8+0QKBgQDU\n2g/uTj7gkt/aW2UdYq31keaqNLklKhzfCU3UPp9UwLE7QeoBE2qxEAVlh61WHlTy\ndEiXI9N9Q/hWD+LLbo9LmORBGn4MXND/ZM3v4bY6l+mZkPdszg/PMM1sgc4BPMHr\nS7MpE6Ekdubv3AEchvUoykt5IOhgQlc91UQNxsw0lQKBgDgcxKEInX1ZZYJr8fOY\nbzow5CZYZ6Rb6RTZI1MurknWhKFAbEOfiwjJQNXfC9Yp15p5C1CW19QjQVzXdeqZ\n2upHy6sh6HmcLduBV1QYqm3Li4EDl27WpsRX4VqHCfDM4MqBcZ+etQhP/z4catSJ\nZWOCbGDu4nXiywdt87s+UJoX\n-----END PRIVATE KEY-----\n",
    "client_email": "personal-strava-export-api@personal-strava-export-api.iam.gserviceaccount.com",
    "client_id": f"{os.environ['CLIENT_ID']}",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/personal-strava-export-api%40personal-strava-export-api.iam.gserviceaccount.com"
}

service_acc = gspread.service_account_from_dict(GOOGLE_SERVICE_ACCOUNT_CREDENTIALS)
gsheet_file = service_acc.open("personal_strava_export_api")
data_worksheet = gsheet_file.worksheet("data")

# Create main dataframe
main_df = pd.DataFrame(data_worksheet.get_all_records())

# --- Clean up dataframe ---
main_df["start_date_local"] = pd.to_datetime(main_df["start_date_local"])
main_df["start_date_day_only"] = main_df["start_date_local"].dt.normalize()
main_df["start_date_year"] = pd.DatetimeIndex(main_df["start_date_local"]).year
main_df["start_date_month"] = pd.DatetimeIndex(main_df["start_date_local"]).month
main_df["start_date_day"] = pd.DatetimeIndex(main_df["start_date_local"]).day
main_df["start_date_day_month"] = pd.to_datetime(main_df["start_date_local"].dt.strftime('%m-%d'), format='%m-%d', errors='coerce')
main_df["start_date_month_name"] = main_df['start_date_local'].dt.month_name()
main_df['start_date_week_number'] = main_df['start_date_local'].dt.isocalendar().week
main_df.loc[
    (main_df['start_date_week_number'] == 52) & (main_df['start_date_month'] == 1), 'start_date_week_number'] = 0

main_df.loc[(main_df['average_heartrate'] == ""), 'average_heartrate'] = 0
main_df.loc[(main_df['max_heartrate'] == ""), 'max_heartrate'] = 0
main_df.loc[(main_df['average_cadence'] == ""), 'average_cadence'] = 0
main_df.loc[(main_df['average_watts'] == ""), 'average_watts'] = 0
main_df.loc[(main_df['max_watts'] == ""), 'max_watts'] = 0
main_df.loc[(main_df['start_lat'] == ""), 'start_lat'] = 0
main_df.loc[(main_df['start_lng'] == ""), 'start_lng'] = 0
main_df.loc[(main_df['end_lat'] == ""), 'end_lat'] = 0
main_df.loc[(main_df['end_lng'] == ""), 'end_lng'] = 0
main_df.loc[(main_df['elev_high'] == ""), 'elev_high'] = 0
main_df.loc[(main_df['elev_low'] == ""), 'elev_low'] = 0

main_df = main_df.astype({
    'id': 'string',
    'average_heartrate': 'Int64',
    'max_heartrate': 'Int64',
    'average_cadence': 'Int64',
    'average_watts': 'Int64',
    'max_watts': 'Int64',
    'start_lat': 'float',
    'start_lng': 'float',
    'end_lat': 'float',
    'end_lng': 'float',
    'elev_high': 'Int64',
    'elev_low': 'Int64',
})

running_df = main_df[main_df["sport_type"] == "Run"]
running_df['daily_distance_total'] = running_df.groupby(running_df['start_date_day_only'])['distance'].sum()
running_df['cumulative_distance'] = running_df.groupby(running_df['start_date_local'].dt.year)['distance'].cumsum()


def compare_numbers(a, b):
    difference = round((((b - a) / abs(a)) * 100), 1)
    result = f'+{difference}%' if difference > 0 else f'{difference}%'
    return result


# Reduce to 2022 only for analysis
today = pd.to_datetime(datetime.now(), utc=True)
cur_year = today.year
one_year_ago = today - relativedelta(years=1)
prev_year = one_year_ago.year
cur_year_df = main_df[main_df["start_date_year"] == cur_year]
prev_year_df = main_df[main_df["start_date_year"] == cur_year - 1]

# ---- Streamlit page ----
st.set_page_config(page_title=f"{cur_year} Year in Review", page_icon=":runner:", layout="wide")

st.title(f":runner: {cur_year} Year In Review")
st.markdown(
    "This dashboard is refreshed everyday using my [Strava](https://www.strava.com/athletes/20432049) data and the [Strava API](https://developers.strava.com/).")
st.markdown("---")
# st.dataframe(main_df)

# --- Global analysis ---
# --- total activities ---
cur_year_total_activities = cur_year_df.shape[0]
prev_year_total_activities = prev_year_df[prev_year_df['start_date_local'] < one_year_ago].shape[0]
diff_total_activities = compare_numbers(prev_year_total_activities, cur_year_total_activities)

# --- total active days ---
cur_year_total_active_days = cur_year_df.groupby(cur_year_df["start_date_local"].dt.date).count().shape[0]
prev_year_total_active_days = prev_year_df[prev_year_df['start_date_local'] < one_year_ago].groupby(
    prev_year_df["start_date_local"].dt.date).count().shape[0]
diff_total_active_days = compare_numbers(prev_year_total_active_days, cur_year_total_active_days)

# --- total calories ---
cur_year_total_calories = cur_year_df["calories"].sum()
prev_year_total_calories = prev_year_df[prev_year_df['start_date_local'] < one_year_ago]["calories"].sum()
diff_total_calories = compare_numbers(prev_year_total_calories, cur_year_total_calories)

# --- total time ---
cur_year_total_time = round(cur_year_df["moving_time"].sum() / 60)
prev_year_total_time = round(prev_year_df[prev_year_df['start_date_local'] < one_year_ago]["moving_time"].sum() / 60)
diff_total_time = compare_numbers(prev_year_total_time, cur_year_total_time)

# --- total time per month ---
cur_year_total_time_per_month = cur_year_df.groupby(["start_date_month", "start_date_month_name"]).sum('numeric_only')
cur_year_total_time_per_month["moving_time"] = round(cur_year_total_time_per_month["moving_time"] / 60)
prev_year_total_time_per_month = prev_year_df.groupby(["start_date_month", "start_date_month_name"]).sum('numeric_only')
prev_year_total_time_per_month["moving_time"] = round(prev_year_total_time_per_month["moving_time"] / 60)

total_time_per_sport_type = cur_year_df.groupby(["start_date_month", "start_date_month_name", "sport_type"]).sum(
    'numeric_only')
total_time_per_sport_type["moving_time"] = round(total_time_per_sport_type["moving_time"] / 60)
months = total_time_per_sport_type.index.get_level_values('start_date_month_name').tolist()[::2]

# --- Streamlit global section ---
# st.dataframe(running_df[['daily_distance_total', 'cumulative_distance', 'start_date_day_only', 'start_date_day', 'start_date_year', 'start_date_day_month']])
st.markdown(f"## {cur_year} Global")
st.markdown('*Numbers compared to the same day last year.*')
st.markdown("##")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown("##### Total Active Days:")
    st.markdown(f"## {cur_year_total_active_days}")
    st.markdown(f'*{diff_total_active_days} compared to {prev_year} ({prev_year_total_active_days} days)*')
    st.markdown("---")
    st.markdown("##### Total Calories:")
    st.markdown(f"## {cur_year_total_calories:,} calories")
    st.markdown(f'*{diff_total_calories} compared to {prev_year} ({prev_year_total_calories:,} calories)*')
    st.markdown("---")
with middle_column:
    st.markdown("##### Total Time:")
    st.markdown(f"## {cur_year_total_time} hours")
    st.markdown(f'*{diff_total_time} compared to {prev_year} ({prev_year_total_time} hours)*')
    st.markdown("---")
    st.markdown("##### Latest activity:")
    st.markdown(f'## {cur_year_df["start_date_local"].iloc[-1].strftime("%B %d, %Y")}')
    st.markdown(f'*As of yesterday*')
    st.markdown("---")
with right_column:
    st.markdown("##### Total Activities:")
    st.markdown(f"## {cur_year_total_activities}")
    st.markdown(f'*{diff_total_activities} compared to {prev_year} ({prev_year_total_activities})*')
    st.markdown("---")


# Hours per month graphs
hours_per_month_fig = go.Figure()

hours_per_month_fig.add_trace(go.Bar(
    x=prev_year_total_time_per_month.index.get_level_values('start_date_month_name'),
    y=prev_year_total_time_per_month['moving_time'],
    name=prev_year,
    offsetgroup=0,
    # marker_color='orange',
    text=prev_year_total_time_per_month['moving_time']
))

hours_per_month_fig.add_trace(go.Bar(
    x=cur_year_total_time_per_month.index.get_level_values('start_date_month_name'),
    y=cur_year_total_time_per_month['moving_time'],
    name=cur_year,
    offsetgroup=1,
    # marker_color='blue',
    text=cur_year_total_time_per_month['moving_time']
))


# Customize the layout
hours_per_month_fig.update_layout(
    barmode='group',
    xaxis_tickangle=-45,
    xaxis_title='Month',
    yaxis_title='Time [hours]',
    legend_title='Year',
    height=600
)

st.write("#")
st.write("#")
st.markdown(f'### Time spent working out ({prev_year} vs. {cur_year})')
st.plotly_chart(hours_per_month_fig, use_container_width=True, height=800)

# --- Running analysis ---
cur_year_running_df = cur_year_df[cur_year_df["sport_type"] == "Run"]
prev_year_running_df = prev_year_df[prev_year_df["sport_type"] == "Run"]

# total running days
cur_year_total_running_days = cur_year_running_df.groupby(cur_year_running_df["start_date_local"].dt.date).count().shape[0]
prev_year_total_running_days = prev_year_running_df[prev_year_running_df['start_date_local'] < one_year_ago].groupby(prev_year_running_df["start_date_local"].dt.date).count().shape[0]
diff_total_running_days = compare_numbers(prev_year_total_running_days, cur_year_total_running_days)

# total running distance
cur_year_total_running_distance = round(cur_year_running_df["distance"].sum(), 2)
prev_year_total_running_distance = round(prev_year_running_df[prev_year_running_df['start_date_local'] < one_year_ago]["distance"].sum(), 2)
diff_total_running_distance = compare_numbers(prev_year_total_running_distance, cur_year_total_running_distance)


# total running time
cur_year_total_running_time = round(cur_year_running_df["moving_time"].sum() / 60)
prev_year_total_running_time = round(prev_year_running_df[prev_year_running_df['start_date_local'] < one_year_ago]["moving_time"].sum() / 60)
diff_total_running_time = compare_numbers(prev_year_total_running_time, cur_year_total_running_time)

# total running elevation
cur_year_total_running_elevation = cur_year_running_df["total_elevation_gain"].sum()
prev_year_total_running_elevation = prev_year_running_df[prev_year_running_df['start_date_local'] < one_year_ago]["total_elevation_gain"].sum()
diff_total_running_elevation = compare_numbers(prev_year_total_running_elevation, cur_year_total_running_elevation)

# total running calories
cur_year_total_running_calories = cur_year_running_df["calories"].sum()
prev_year_total_running_calories = prev_year_running_df[prev_year_running_df['start_date_local'] < one_year_ago]["calories"].sum()
diff_total_running_calories = compare_numbers(prev_year_total_running_calories, cur_year_total_running_calories)

# max running distance
cur_year_max_running_distance = cur_year_running_df["distance"].max()
prev_year_max_running_distance = prev_year_running_df["distance"].max()
diff_max_running_distance = compare_numbers(prev_year_max_running_distance, cur_year_max_running_distance)


# --- total running distance per month ---
cur_year_total_running_distance_per_month = cur_year_running_df.groupby(["start_date_month", "start_date_month_name"]).sum(
    'numeric_only')
cur_year_total_running_distance_per_month["Month"] = cur_year_total_running_distance_per_month.index.get_level_values(
    "start_date_month_name")
prev_year_total_running_distance_per_month = prev_year_running_df.groupby(["start_date_month", "start_date_month_name"]).sum(
    'numeric_only')
prev_year_total_running_distance_per_month["Month"] = prev_year_total_running_distance_per_month.index.get_level_values(
    "start_date_month_name")

# --- total running distance per week ---
cur_year_total_running_distance_per_week = cur_year_running_df.groupby(["start_date_week_number"]).sum('numeric_only')
cur_year_total_running_distance_per_week["Week number"] = cur_year_total_running_distance_per_week.index.get_level_values(
    "start_date_week_number")
prev_year_total_running_distance_per_week = prev_year_running_df.groupby(["start_date_week_number"]).sum('numeric_only')
prev_year_total_running_distance_per_week["Week number"] = prev_year_total_running_distance_per_week.index.get_level_values(
    "start_date_week_number")

# ---- Streamlit running section ----
st.markdown("---")
st.markdown(f"## {cur_year} Running")
st.markdown('*Numbers compared to the same day last year.*')
st.markdown("##")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown("##### Total Running Days:")
    st.markdown(f"## {cur_year_total_running_days}")
    st.markdown(f'*{diff_total_running_days} compared to {prev_year} ({prev_year_total_running_days} days)*')
    st.markdown("---")
    st.markdown("##### Total Running Elevation:")
    st.markdown(f"## {cur_year_total_running_elevation:,} m")
    st.markdown(f'*{diff_total_running_elevation} compared to {prev_year} ({prev_year_total_running_elevation:,} m)*')
    st.markdown("---")

with middle_column:
    st.markdown("##### Total Running Distance:")
    st.markdown(f"## {cur_year_total_running_distance} kms")
    st.markdown(f'*{diff_total_running_distance} compared to {prev_year} ({prev_year_total_running_distance} kms)*')
    st.markdown("---")
    st.markdown("##### Total Running Calories:")
    st.markdown(f"## {cur_year_total_running_calories:,}")
    st.markdown(f'*{diff_total_running_calories} compared to {prev_year} ({prev_year_total_running_calories:,} calories)*')
    st.markdown("---")

with right_column:
    st.markdown("##### Total Running Time:")
    st.markdown(f"## {cur_year_total_running_time} hours")
    st.markdown(f'*{diff_total_running_time} compared to {prev_year} ({prev_year_total_running_time} hours)*')
    st.markdown("---")
    st.markdown("##### Max Running Distance:")
    st.markdown(f"## {cur_year_max_running_distance} kms")
    st.markdown(f'*{diff_max_running_distance} compared to {prev_year} ({prev_year_max_running_distance} kms)*')
    st.markdown("---")

# Distance per month graphs
running_distance_per_month_fig = go.Figure()

running_distance_per_month_fig.add_trace(go.Bar(
    x=prev_year_total_running_distance_per_month.index.get_level_values('start_date_month_name'),
    y=prev_year_total_running_distance_per_month['distance'],
    name=prev_year,
    offsetgroup=0,
    # marker_color='orange',
    text=round(prev_year_total_running_distance_per_month['distance'])
))

running_distance_per_month_fig.add_trace(go.Bar(
    x=cur_year_total_running_distance_per_month.index.get_level_values('start_date_month_name'),
    y=cur_year_total_running_distance_per_month['distance'],
    name=cur_year,
    offsetgroup=1,
    # marker_color='blue',
    text=round(cur_year_total_running_distance_per_month['distance'])
))


# Customize the layout
running_distance_per_month_fig.update_layout(
    barmode='group',
    xaxis_tickangle=-45,
    xaxis_title='Month',
    yaxis_title='Distance [kms]',
    legend_title='Year',
    height=600
)

st.write("#")
st.write("#")
st.markdown(f'### Running distance per month ({prev_year} vs. {cur_year})')
st.plotly_chart(running_distance_per_month_fig, use_container_width=True, height=800)

# Distance per week graphs
running_distance_per_week_fig = go.Figure()

running_distance_per_week_fig.add_trace(go.Bar(
    x=prev_year_total_running_distance_per_week['Week number'],
    y=prev_year_total_running_distance_per_week['distance'],
    name=prev_year,
    offsetgroup=0,
))

running_distance_per_week_fig.add_trace(go.Bar(
    x=cur_year_total_running_distance_per_week['Week number'],
    y=cur_year_total_running_distance_per_week['distance'],
    name=cur_year,
    offsetgroup=1,
))


# Customize the layout
running_distance_per_week_fig.update_layout(
    barmode='group',
    xaxis_tickangle=-45,
    xaxis_title='Week Number',
    xaxis_range=[-0.5, 52],
    yaxis_title='Distance [kms]',
    legend_title='Year',
    height=600
)

st.write("#")
st.write("#")
st.markdown(f'### Running distance per week ({prev_year} vs. {cur_year})')
st.plotly_chart(running_distance_per_week_fig, use_container_width=True, height=800)


# Cumulative running
st.markdown('### Cumulative Running Distance, Year Over Year:')
cumulative_running = px.line(line_shape='spline')
cumulative_running.add_scatter(x=running_df[running_df["start_date_year"] == cur_year]['start_date_day_month'],
                               y=running_df[running_df["start_date_year"] == cur_year]['cumulative_distance'],
                               name=cur_year, mode='lines')
cumulative_running.add_scatter(x=running_df[running_df["start_date_year"] == cur_year - 1]['start_date_day_month'],
                               y=running_df[running_df["start_date_year"] == cur_year - 1]['cumulative_distance'],
                               name=cur_year - 1, mode='lines')
cumulative_running.add_scatter(x=running_df[running_df["start_date_year"] == cur_year - 2]['start_date_day_month'],
                               y=running_df[running_df["start_date_year"] == cur_year - 2]['cumulative_distance'],
                               name=cur_year - 2, mode='lines')
cumulative_running.add_scatter(x=running_df[running_df["start_date_year"] == cur_year - 3]['start_date_day_month'],
                               y=running_df[running_df["start_date_year"] == cur_year - 3]['cumulative_distance'],
                               name=cur_year - 3, mode='lines')
cumulative_running.update_xaxes(title_text='Date', dtick='M1', tickformat='%d-%b')
cumulative_running.update_yaxes(title_text='Distance [kms]', dtick=200)
cumulative_running.update_layout(height=600)
st.plotly_chart(cumulative_running, use_container_width=True)

# st.dataframe(running_df)
