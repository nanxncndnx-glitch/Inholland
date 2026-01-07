import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def analytics_dashboard():
    """Main analytics dashboard function for gym owners."""
    
    # Load data
    df = pd.read_csv("/Users/nanxncndnx/Documents/Endeavors/Inholland/Plugins/gym_daily_exercise_stats.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    df['week_number'] = df['date'].dt.isocalendar().week
    df['peak_hour_int'] = df['peak_hour'].str.replace(':00', '').astype(int)
    
    # Title
    st.title("Gym Analytics Dashboard")
    st.markdown("Comprehensive analysis of gym exercise data")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    else:
        filtered_df = df
    
    exercises = ['All'] + sorted(df['exercise'].unique().tolist())
    selected_exercise = st.sidebar.selectbox("Select Exercise", exercises)
    
    if selected_exercise != 'All':
        filtered_df = filtered_df[filtered_df['exercise'] == selected_exercise]
    
    # Summary metrics
    st.header("Overview")
    
    total_persons = filtered_df['total_persons'].sum()
    total_duration = filtered_df['total_duration_minutes'].sum()
    total_sets = filtered_df['total_sets'].sum()
    total_reps = filtered_df['total_reps'].sum()
    avg_persons_per_day = filtered_df.groupby('date')['total_persons'].sum().mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Visitors", f"{total_persons:,}")
    with col2:
        st.metric("Total Duration", f"{total_duration:,} min")
    with col3:
        st.metric("Total Sets", f"{total_sets:,}")
    with col4:
        st.metric("Total Reps", f"{total_reps:,}")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.metric("Avg Visitors/Day", f"{avg_persons_per_day:.0f}")
    with col6:
        weekly = filtered_df.groupby('week_number')['total_persons'].sum()
        if len(weekly) >= 2:
            growth = ((weekly.iloc[-1] - weekly.iloc[-2]) / weekly.iloc[-2]) * 100
        else:
            growth = 0
        st.metric("Week-over-Week Growth", f"{growth:.1f}%")
    with col7:
        st.metric("Days Analyzed", filtered_df['date'].nunique())
    
    st.markdown("---")
    
    # Daily trends
    st.header("Daily Trends")
    
    daily_data = filtered_df.groupby('date').agg({
        'total_persons': 'sum',
        'total_duration_minutes': 'sum',
        'total_sets': 'sum',
        'total_reps': 'sum'
    }).reset_index()
    
    tab1, tab2, tab3 = st.tabs(["Visitors", "Duration", "Sets and Reps"])
    
    with tab1:
        fig = px.line(
            daily_data, 
            x='date', 
            y='total_persons',
            title='Daily Total Visitors'
        )
        fig.update_traces(line_color='#4CAF50')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.bar(
            daily_data, 
            x='date', 
            y='total_duration_minutes',
            title='Daily Total Duration (minutes)'
        )
        fig.update_traces(marker_color='#2196F3')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily_data['date'], y=daily_data['total_sets'], name='Sets', marker_color='#FF9800'))
        fig.add_trace(go.Bar(x=daily_data['date'], y=daily_data['total_reps'], name='Reps', marker_color='#9C27B0'))
        fig.update_layout(title='Daily Sets and Reps', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Exercise analysis
    st.header("Exercise Analysis")
    
    rankings = filtered_df.groupby('exercise').agg({
        'total_persons': 'sum',
        'total_duration_minutes': 'sum',
        'total_sets': 'sum',
        'total_reps': 'sum'
    }).reset_index().sort_values('total_persons', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            rankings.head(10),
            x='total_persons',
            y='exercise',
            orientation='h',
            title='Top 10 Exercises by Visitors'
        )
        fig.update_traces(marker_color='#4CAF50')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            rankings,
            values='total_duration_minutes',
            names='exercise',
            title='Duration Share by Exercise'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Day of week analysis
    st.header("Day of Week Patterns")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_data = filtered_df.groupby('day_of_week').agg({
        'total_persons': 'mean',
        'total_duration_minutes': 'mean'
    }).reset_index()
    dow_data['day_of_week'] = pd.Categorical(dow_data['day_of_week'], categories=day_order, ordered=True)
    dow_data = dow_data.sort_values('day_of_week')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(dow_data, x='day_of_week', y='total_persons', title='Average Visitors by Day of Week')
        fig.update_traces(marker_color='#2196F3')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(dow_data, x='day_of_week', y='total_duration_minutes', title='Average Duration by Day of Week')
        fig.update_traces(marker_color='#FF9800')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Peak hours analysis
    st.header("Peak Hours Analysis")
    
    peak_data = filtered_df.groupby('peak_hour').agg({
        'total_persons': 'sum',
        'exercise': 'count'
    }).reset_index()
    peak_data.columns = ['peak_hour', 'total_persons', 'frequency']
    peak_data = peak_data.sort_values('peak_hour')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(peak_data, x='peak_hour', y='total_persons', title='Total Visitors by Peak Hour')
        fig.update_traces(marker_color='#E91E63')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(peak_data, x='peak_hour', y='frequency', title='Peak Hour Frequency')
        fig.update_traces(marker_color='#9C27B0')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Heatmap
    st.header("Exercise Popularity Heatmap")
    
    if selected_exercise == 'All':
        heatmap_data = filtered_df.pivot_table(
            values='total_persons',
            index='exercise',
            columns='day_of_week',
            aggfunc='mean'
        )
        heatmap_data = heatmap_data[day_order]
        
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Day of Week", y="Exercise", color="Avg Visitors"),
            title="Average Visitors by Exercise and Day of Week",
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Busiest and slowest days
    st.header("Busiest and Slowest Days")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 5 Busiest Days")
        busiest = daily_data.nlargest(5, 'total_persons')[['date', 'total_persons', 'total_duration_minutes']].copy()
        busiest['date'] = busiest['date'].dt.strftime('%Y-%m-%d')
        busiest.columns = ['Date', 'Visitors', 'Duration (min)']
        st.dataframe(busiest, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Top 5 Slowest Days")
        slowest = daily_data.nsmallest(5, 'total_persons')[['date', 'total_persons', 'total_duration_minutes']].copy()
        slowest['date'] = slowest['date'].dt.strftime('%Y-%m-%d')
        slowest.columns = ['Date', 'Visitors', 'Duration (min)']
        st.dataframe(slowest, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Detailed data
    st.header("Detailed Data")
    
    with st.expander("View Raw Data"):
        display_df = filtered_df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "Download Filtered Data as CSV",
            csv,
            "gym_analytics_export.csv",
            "text/csv"
        )
    
    with st.expander("View Exercise Statistics"):
        rankings['avg_duration_per_person'] = (rankings['total_duration_minutes'] / rankings['total_persons']).round(1)
        rankings['avg_reps_per_set'] = (rankings['total_reps'] / rankings['total_sets']).round(1)
        display_rankings = rankings.copy()
        display_rankings.columns = ['Exercise', 'Total Visitors', 'Total Duration (min)', 'Total Sets', 'Total Reps', 'Avg Duration/Person', 'Avg Reps/Set']
        st.dataframe(display_rankings, use_container_width=True, hide_index=True)