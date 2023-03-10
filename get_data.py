import os
from datetime import datetime
import gspread
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

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
main_df["start_date_year"] = pd.DatetimeIndex(main_df["start_date_local"]).year
main_df["start_date_month"] = pd.DatetimeIndex(main_df["start_date_local"]).month
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

# Reduce to 2022 only for analysis
this_year = datetime.now().year
main_df = main_df.loc[main_df["start_date_year"] == this_year]

# --- Global analysis ---
total_activities = main_df.shape[0]
total_active_days = main_df.groupby(main_df["start_date_local"].dt.date).count().shape[0]
total_calories = main_df["calories"].sum()
total_time = round(main_df["moving_time"].sum() / 60)
total_time_per_month = main_df.groupby(["start_date_month", "start_date_month_name"]).sum('numeric_only')
total_time_per_month["moving_time"] = round(total_time_per_month["moving_time"] / 60)
total_time_per_sport_type = main_df.groupby(["start_date_month", "start_date_month_name", "sport_type"]).sum('numeric_only')
total_time_per_sport_type["moving_time"] = round(total_time_per_sport_type["moving_time"] / 60)
months = total_time_per_sport_type.index.get_level_values('start_date_month_name').tolist()[::2]


# plt.figure(figsize=(14, 8))
# plt.xticks(fontsize=14, rotation=45)
# plt.yticks(fontsize=14)
# ax1 = plt.gca()
# ax1.set_xlabel("Month")
# ax1.set_ylabel("Duration [hours]", fontsize=12, color='b')
# ax1.bar(months, total_time_per_sport_type.loc[total_time_per_sport_type["sport_type"] == "Run"]["moving_time"], color='y')
# plt.show()

print(f'2022 GLOBAL:',
      f'Total activities: {total_activities}',
      f'Total days active: {total_active_days}',
      f'Total calories: {total_calories:,}',
      f'Total time: {total_time} hours\n',
      # f"Activities performed this year: {', '.join(activities_performed_this_year)}",
      sep='\n')

# print(total_time_per_sport_type["moving_time"])
# plt.figure(figsize=(14, 8))
# plt.xticks(fontsize=14, rotation=45)
# plt.yticks(fontsize=14)
# ax1 = plt.gca()
# ax1.set_xlabel("Month")
# ax1.set_ylabel("Distance", fontsize=12, color='b')
# ax1.bar(total_running_distance_per_month.index.get_level_values('start_date_month_name'), total_running_distance_per_month["distance"], color='y')
# plt.show()


# --- Running analysis ---
running_df = main_df.loc[main_df["sport_type"] == "Run"]
total_running_distance = round(running_df["distance"].sum(), 2)
max_running_distance = running_df["distance"].max()
total_running_days = running_df.groupby(main_df["start_date_local"].dt.date).count().shape[0]
total_running_time = round(running_df["moving_time"].sum() / 60)
total_running_calories = running_df["calories"].sum()
total_running_elevation = running_df["total_elevation_gain"].sum()
print(f"2022 RUNNING:",
      f"Total running distance: {total_running_distance} kms",
      f"Max distance: {max_running_distance} kms",
      f"Total running days: {total_running_days} days",
      f"Total running time: {total_running_time} hours",
      f"Total running calories: {total_running_calories:,} calories",
      f"Total running elevation: {total_running_elevation:,} m",
      sep='\n')

total_running_distance_per_month = running_df.groupby(["start_date_month", "start_date_month_name"]).sum('numeric_only')
total_running_distance_per_month["Month"] = total_running_distance_per_month.index.get_level_values("start_date_month_name")

total_running_distance_per_week = running_df.groupby(["start_date_week_number"]).sum('numeric_only')
total_running_distance_per_week["Week number"] = total_running_distance_per_week.index.get_level_values("start_date_week_number")

# Distance per month
plt.figure(figsize=(14, 10))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
ax1 = plt.gca()
ax1.set_xlabel("Month")
ax1.set_ylabel("Distance", fontsize=12, color='b')
ax1.bar(
    total_running_distance_per_month.index.get_level_values('start_date_month_name'),
    total_running_distance_per_month["distance"],
    color='b')
plt.show()

# Distance per week
plt.figure(figsize=(14, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
ax2 = plt.gca()
ax2.set_xlabel("Week")
ax2.set_ylabel("Distance", fontsize=12, color='b')
ax2.bar(
    total_running_distance_per_week.index,
    total_running_distance_per_week["distance"],
    color='g')
plt.show()


# ---- Streamlit page ----
st.set_page_config(page_title=f"{this_year} Year in Review", page_icon=":runner:", layout="wide")
# uploaded_file = st.file_uploader("Choose a CSV file")
# st.button("Upload file to Sandbox")
# ---- MAIN PAGE ----
st.title(f":runner: {this_year} Year In Review")
st.markdown("---")
# st.markdown("##")

st.header("Global")
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.text("Total Active Days:")
    st.subheader(f"{total_active_days}")
    st.text("Total Calories:")
    st.subheader(f"{total_calories:,}")
with middle_column:
    st.text("Total Time:")
    st.subheader(f"{total_time} hours")
with right_column:
    st.text("Total Activities:")
    st.subheader(f"{total_activities}")

hours_per_month_fig = px.bar(
    total_time_per_month,
    x=total_time_per_month.index.get_level_values('start_date_month_name'),
    y=total_time_per_month['moving_time'],
    orientation="v",
    title="Hours per Month",
    template="plotly_white",
)

hours_per_month_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_range=[-0.5, 12],
    xaxis_title="Month",
    yaxis_title="Numbers of Hours",
    height=600
)

st.plotly_chart(hours_per_month_fig, use_container_width=True, height=800)

# ---- Running section ----
st.markdown("---")
st.header("Running")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.text("Total Running Days:")
    st.subheader(f"{total_running_days}")
    st.text("Total Running Elevation:")
    st.subheader(f"{total_running_elevation:,} m")
with middle_column:
    st.text("Total Running Distance:")
    st.subheader(f"{total_running_distance} kms")
    st.text("Total Running Calories:")
    st.subheader(f"{total_running_calories:,}")
with right_column:
    st.text("Total Running Time:")
    st.subheader(f"{total_running_time} hours")
    st.text("Max Running Distance:")
    st.subheader(f"{max_running_distance} kms")

# Distance per month
distance_per_month_fig = px.bar(
    total_running_distance_per_month,
    x=total_running_distance_per_month["Month"],
    y=total_running_distance_per_month['distance'],
    orientation="v",
    title="Running Distance per Month",
    template="plotly_white",
)

distance_per_month_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_range=[-0.5, 12],
    xaxis_title="Month",
    yaxis_title="Distance [kms]",
    height=600
)

st.plotly_chart(distance_per_month_fig, use_container_width=True)

# Distance per week
distance_per_week_fig = px.bar(
    total_running_distance_per_week,
    x=total_running_distance_per_week["Week number"],
    y=total_running_distance_per_week['distance'],
    orientation="v",
    title="Running Distance per Week",
    template="plotly_white",
)

distance_per_week_fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_range=[-0.5, 52],
    xaxis_title="Week Number",
    yaxis_title="Distance [kms]",
    height=600
)

st.plotly_chart(distance_per_week_fig, use_container_width=True)

