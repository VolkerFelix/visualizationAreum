import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_xyz_chart(df):
    """Create an interactive chart showing X, Y, Z acceleration components"""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No acceleration data available",
            height=500
        )
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['x'],
        mode='lines',
        name='X-axis',
        line=dict(color='rgb(31, 119, 180)')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['y'],
        mode='lines',
        name='Y-axis',
        line=dict(color='rgb(44, 160, 44)')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['z'],
        mode='lines',
        name='Z-axis',
        line=dict(color='rgb(255, 127, 14)')
    ))
    
    fig.update_layout(
        title="Acceleration Components",
        xaxis_title="Samples",
        yaxis_title="Acceleration (g)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

def create_magnitude_chart(df):
    """Create an interactive chart showing acceleration magnitude"""
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No magnitude data available",
            height=500
        )
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['index'], 
        y=df['magnitude'],
        mode='lines',
        name='Magnitude',
        line=dict(color='rgb(214, 39, 40)', width=2)
    ))
    
    # Add a reference line for 1g (approximately Earth's gravity)
    fig.add_shape(
        type="line",
        x0=df['index'].min(),
        y0=1.0,
        x1=df['index'].max(),
        y1=1.0,
        line=dict(
            color="rgba(0,0,0,0.3)",
            width=1,
            dash="dash",
        )
    )
    
    fig.update_layout(
        title="Movement Magnitude",
        xaxis_title="Samples",
        yaxis_title="Magnitude (g)",
        height=500,
        annotations=[
            dict(
                x=df['index'].min() + (df['index'].max() - df['index'].min()) * 0.02,
                y=1.05,
                xref="x",
                yref="y",
                text="Earth's gravity (1g)",
                showarrow=False,
                font=dict(
                    size=10,
                    color="rgba(0,0,0,0.5)"
                )
            )
        ]
    )
    
    return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')