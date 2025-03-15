from flask import render_template, request, redirect, url_for, session, flash
from . import dashboard
from ..auth.utils import is_authenticated
from ..utils.api import get_acceleration_data
from ..utils.charts import create_xyz_chart, create_magnitude_chart
from ..dashboard.utils import process_acceleration_data, calculate_metrics

@dashboard.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('auth.login'))
    
    try:
        # Fetch user's health data
        success, datasets, error = get_acceleration_data(session['token'])
        
        if not success:
            flash(error or 'Failed to retrieve data', 'danger')
            return render_template('dashboard/index.html', datasets=[])
        
        if not datasets:
            return render_template('dashboard/index.html', datasets=[])
        
        # Sort datasets by created_at, newest first
        datasets.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Get selected dataset ID from query params, default to the first one
        selected_id = request.args.get('dataset', datasets[0]['id'])
        selected_dataset = next((d for d in datasets if d['id'] == selected_id), datasets[0])
        
        # Process the data for plotting
        df = process_acceleration_data(selected_dataset)
        
        # Calculate metrics
        metrics = calculate_metrics(df)
        
        # Create charts
        acceleration_chart = create_xyz_chart(df)
        magnitude_chart = create_magnitude_chart(df)
        
        return render_template(
            'dashboard/index.html',
            datasets=datasets,
            selected_dataset=selected_dataset,
            acceleration_chart=acceleration_chart,
            magnitude_chart=magnitude_chart,
            metrics=metrics
        )
    
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        return render_template('dashboard/index.html', datasets=[])

@dashboard.route('/refresh')
def refresh():
    """Refresh data and redirect to dashboard"""
    return redirect(url_for('dashboard.index'))