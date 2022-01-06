 # import streamlit as st
# import pymongo
# import pandas as pd
# import time
# from setup.mongo_class import MongoDB
# import altair as alt


# # st.write(data)


# Mongo = MongoDB(db_name="log", collection_name="invalid")


# # Add a selectbox to the sidebar:

# st.header("Real-time Streaming Logdata Loading!...")
# st.caption("Top 5 countries with highest Vulnerability are as follows...")
# col4, col5 = st.columns(2)
# col1, col2, col3 = st.columns(3)

# time1 = time.strftime("%Y-%m-%d %I:%M") + ":00"

# from datetime import datetime
# from datetime import timedelta

# # Get current time in local timezone
# current_time = datetime.now()


# future_start_time = current_time - timedelta(minutes=2)
# future_start_time_str = future_start_time.strftime("%Y-%m-%d %I:%M") + ":00"
# future_end_time_7days = current_time - timedelta(days=7)
# future_end_time_30days = current_time - timedelta(days=30)
# future_end_time_str_7days = future_end_time_7days.strftime("%Y-%m-%d %I:%M") + ":00"
# future_end_time_str_30days = future_end_time_30days.strftime("%Y-%m-%d %I:%M") + ":00"
# print(
#     "start time is -",
#     future_start_time_str,
#     "\n",
#     "end time is-",
#     future_end_time_str_7days,
# )


# dat = st.sidebar.date_input("Enter Date")
# tim = st.sidebar.time_input("Enter Time")
# print(dat, tim)


# def prev_func(start_time, end_time):
#     pipeline = [
#         {
#             "$group": {
#                 "_id": {
#                     "start_time": f"{start_time}",
#                     "end_time": f"{end_time}",
#                     "country": "$name",
#                 },
#                 "count_ipv4": {"$sum": "$ipv4"},
#             }
#         },
#         {"$sort": {"count_ipv4": -1}},
#         {"$limit": 5},
#     ]
#     ss = Mongo.collection.aggregate(pipeline)
#     return ss


# with col3:
#     if st.button("Customize", key="5"):
#         # col4, col5 = st.columns(2)
#         with col4:
#             start_time = st.text_input(
#                 label="Start Date", key="1", value=future_start_time_str
#             )
#         with col5:
#             end_time = st.text_input(
#                 "End Date",
#                 help="22",
#                 args="5",
#                 key="2",
#                 value=future_end_time_str_7days,
#             )


# def chart():
#     x = []
#     y = []
#     x = [i["_id"]["country"] for i in prev_func(start_time, end_time)]
#     y = [i["count_ipv4"] for i in prev_func(start_time, end_time)]
#     for i in prev_func(start_time, end_time):

#         x.append(i["_id"]["country"])
#         y.append(i["count_ipv4"])

#     # print(x, y)
#     return x, y


# def data():
#     data = pd.DataFrame(
#         {
#             "country": chart()[0],
#             "count_ipv4": chart()[1],
#         }
#     )
#     return data


# def write_chart():
#     st.write(
#         alt.Chart(data, width=700, height=500)
#         .mark_bar(width=50)
#         .encode(
#             x=alt.X("country", sort=None),
#             y="count_ipv4",
#         )
#     )

# st.write(
#         alt.Chart(data, width=700, height=500)
#         .mark_bar(width=50)
#         .encode(
#             x=alt.X("country", sort=None),
#             y="count_ipv4",
#         )
#     )
# with col1:
#     st.button("Last 7 days", key="7")
#     prev_func(start_time, future_end_time_str_7days)
#     chart()
#     data()
#     write_chart()

# with col2:
#     st.button("Last 30 days", key="30")
#     prev_func(start_time, future_end_time_str_30days)
#     chart()
#     data()
#     write_chart()
# ----------------------------------------------------------

import streamlit as st
import pymongo
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import altair as alt
from setup.mongo_class import MongoDB

Mongo = MongoDB(db_name="log", collection_name="inval")

st.header("Real-time Streaming Logdata Loading!...")
st.caption("Top 5 countries with highest Vulnerability are as follows...")

time1 = time.strftime("%Y-%m-%d %I:%M") + ":00"

# Get current time in local timezone
current_time = datetime.now()

future_start_time = current_time - timedelta(minutes=2)
future_start_time_str = future_start_time.strftime("%Y-%m-%d %I:%M") + ":00"
future_end_time = current_time - timedelta(minutes=1)
future_end_time_str = future_end_time.strftime("%Y-%m-%d %I:%M") + ":00"
print(
    "start time is -", future_start_time_str, "\n", "end time is-", future_end_time_str
)


add_selectbox1 = st.sidebar.selectbox(
    "How would you like to be sort?", ("count-asc", "count-desc")
)

add_selectbox2 = st.sidebar.selectbox("How would you like to be display?", ("5", "10"))


def test():
    if add_selectbox1 == "count-desc":
        return 1
    else:
        return -1


start_time = st.sidebar.text_input("Enter Start-time", key="ff")

end_time = st.sidebar.text_input("Enter End-time", key="ii")

# st.sidebar.date_input("Enter Date")
# st.sidebar.time_input("Enter Time")


def prev_func(add_selectbox2, start_time, end_time):
    # pipeline = [
    #     {
    #         "$group": {
    #             "_id": {
    #                 "start_time": f"{start_time}",
    #                 "end_time": f"{end_time}",
    #                 "country": "$name",
    #             },
    #             "count_ipv4": {"$sum": "$ipv4"},
    #         }
    #     },
    #     {"$sort": {"count_ipv4": test()}},
    #     {"$limit": int(add_selectbox2)},
    # ]
    pipeline = [
    {
        "$match": {
            "start_time": {"$gte": f"{start_time}"},
            "end_time": {"$lte": f"{end_time}"},
        }
    },
    {
        "$group": {
            "_id": {
                "country": "$name",
            },
            "count_ipv4": {"$sum": "$ipv4"},
        }
    },
    {"$sort": {"count_ipv4": test()}},
    {"$limit": int(add_selectbox2)},
    ]


    ss = Mongo.collection.aggregate(pipeline)
    return ss


print(start_time, end_time)

if start_time and end_time != "":
    x = []
    y = []
    for i in prev_func(add_selectbox2, start_time, end_time):
        x.append(i["_id"]["country"])
        y.append(i["count_ipv4"])

    print(x, y)

    data = pd.DataFrame(
        {
            "country": x,
            "count_ipv4": y,
        }
    )
    st.write(data)
    st.write(
        alt.Chart(data, width=800, height=500)
        .mark_bar(width=50)
        .encode(
            x=alt.X("country", sort=None),
            y="count_ipv4",
        )
    )
else:
    st.write("loading..")

