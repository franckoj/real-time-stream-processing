 import streamlit as st


import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import altair as alt
from setup.mongo_class import MongoDB

Mongo = MongoDB(db_name="log", collection_name="invalid")


class AppUX:
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time
        self.pipeline = [
            {
                "$match": {
                    "start_time": {"$gte": f"{self.start_time}"},
                    "end_time": {"$lte": f"{self.end_time}"},
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
            {"$sort": {"count_ipv4": -1}},
            {"$limit": 5},
        ]
        self.doc = Mongo.collection.aggregate(self.pipeline)

    def doc(self):
        ss = Mongo.collection.aggregate(self.pipeline)
        return ss

    def im(self, x=None, y=None):
        x = []
        y = []
        for i in self.doc:
            x.append(i["_id"]["country"])
            y.append(i["count_ipv4"])
        data = pd.DataFrame(
            {
                "country": x,
                "count_ipv4": y,
            }
        )
        st.write(
            alt.Chart(data, width=800, height=500)
            .mark_bar(width=50)
            .encode(
                x=alt.X("country", sort=None),
                y="count_ipv4",
            )
        )
        return data

    st.header("Real-time Streaming Logdata Loading!...")
    st.caption("Top 5 countries with highest Vulnerability are as follows...")
    col4, col5 = st.columns(2)
    col1, col2, col3 = st.columns(3)

    with col3:
        if st.button("Customize", key="5"):
        # col4, col5 = st.columns(2)
            with col4:
                start_time = st.text_input(
                label="Start Date", key="1", value="future_start_time_str"
            )
            with col5:
                end_time = st.text_input(
                "End Date",
                help="22",
                args="5",
                key="2",
                value="future_end_time_str_7days",
            )
    # def last_7days():
    #     with col1:
    #         st.button("Last 7 days", key="7")
    #     # prev_func(start_time, future_end_time_str_7days)
    #     # chart()
    #     # data()
    #     # write_chart()

    # with col2:
    #     st.button("Last 30 days", key="30")
    #     # prev_func(start_time, future_end_time_str_30days)
    #     # chart()
    #     # data()
    #     # write_chart()


current_time = datetime.now()

future_start_time = current_time - timedelta(minutes=2)
future_end_time = current_time - timedelta(days=30)
col1, col2, col3 = st.columns(3)
def last_7days():
        with col1:
            st.button("Last 7 days", key="7")
        ui.im()
        # prev_func(start_time, future_end_time_str_7days)
        # chart()
        # data()
        # write_chart()

with col2:
    st.button("Last 30 days", key="30")
        # prev_func(start_time, future_end_time_str_30days)
        # chart()
        # data()
        # write_chart()
ui = AppUX(future_end_time, future_start_time)

# ui.im()