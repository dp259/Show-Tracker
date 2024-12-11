from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session as flaskSession
from sqlalchemy.exc import SQLAlchemyError
from database.sql_tables_python import Users, User_Trackers, Shows
from backend.engine import session

tracker_bp = Blueprint('tracker_bp', __name__)

@tracker_bp.route('/tracker_ui', methods = ['GET', 'POST'])
def tracker_ui():
    if 'Username' not in flaskSession:
        return redirect(url_for('authorization_bp.login'))
    
    try:
        user = session.query(Users).filter(Users.Username == flaskSession['Username']).first()
        # Filter trackers by status
        if user.user_trackers == None:
            return render_template('tracker_ui.html', planned_trackers = [], in_progress_trackers = [], completed_trackers = [])
        
        planned_trackers = [tracker for tracker in user.user_trackers if tracker.status == "Planned"]
        in_progress_trackers = [tracker for tracker in user.user_trackers if tracker.status == "In-progress"]
        completed_trackers = [tracker for tracker in user.user_trackers if tracker.status == "Completed"]

        return render_template('tracker_ui.html', planned_trackers = planned_trackers, in_progress_trackers = in_progress_trackers, completed_trackers = completed_trackers)
    
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        session.rollback()
        return redirect(url_for('tracker_bp.tracker_ui'))


@tracker_bp.route('/add_tracker', methods = ['GET', 'POST'])
def add_tracker():
    if 'Username' not in flaskSession:
        return redirect(url_for('authentication_bp.login'))
    
    show = request.form['Show']
    status = request.form['Status']

    show = session.query(Shows).filter_by(name = show).first()
    if show.backdrop == '/https://via.placeholder.com/500x281?text=No+Backdrop+Available':
        show.backdrop = '/https://via.placeholder.com/500x281?text=No+Backdrop+Available.jpg'
    else:
        show.backdrop = f'https://image.tmdb.org/t/p/w500{show.backdrop}'

    if not show:
        flash("Show not found.")
        return redirect(url_for('tracker_bp.tracker_ui'))

    #potential exception could be added here
    show_id = show.show_id

    user = session.query(Users).filter(Users.Username == flaskSession['Username']).first()
    exists = session.query(User_Trackers).filter_by(user_id = user.user_id, show_id = show_id).first()
    episode = 0

    if status == 'Completed':
        episode = show.episodes

    if exists:
        flash("Tracker already exists for this show, try updating it.")
    else:
        new_tracker = User_Trackers(user_id = user.user_id, show_id = show_id, status = status, progress = episode)
        session.add(new_tracker)
        session.commit()

    return redirect(url_for('tracker_bp.tracker_ui'))

"""
@tracker_bp.route('/backdrop/<int:tracker_id>', methods = ['POST'])
def backdrop(tracker_id):
    tracker = session.query(User_Trackers).filter(tracker_id == tracker_id).first()
    show = tracker.show

    backdrop_link = 'https://image.tmdb.org/t/p/w'
    return None
"""

@tracker_bp.route('/update_tracker/<int:tracker_id>', methods = ['GET', 'POST'])
def update_tracker(tracker_id):
    if 'Username' not in flaskSession:
        return redirect(url_for('authorization_bp.login'))

    status = request.form[f'status_{tracker_id}']
    progress = request.form[f'progress_{tracker_id}']

    if status is None or progress is None:
        flash("Both status and progress fields are required.")
        return redirect(url_for('tracker_bp.tracker_ui'))

    tracker = session.query(User_Trackers).filter_by(tracker_id = tracker_id).first()
    show = session.query(Shows).filter_by(show_id = tracker.show_id).first()
    progress = int(progress)

    if progress == show.episodes:
        tracker.progress = show.episodes
        tracker.status = 'Completed'
    elif progress == 0 and status != 'Planned':
        tracker.status = 'Planned'
        tracker.progress = 0
    elif progress != show.episodes and status == 'Completed':
        tracker.status = 'Completed'
        tracker.progress = show.episodes
    elif progress != 0 and status == 'Planned':
        if progress == show.episodes:
            tracker.progress = progress
            tracker.status = 'Completed'
        else:
            tracker.progress = progress
            tracker.status = 'In-Progress'
    elif status == 'Completed':
        tracker.progress = show.episodes
        tracker.status = 'Completed'
    else:
        #if tracker and tracker.User.Users == flaskSession['Username']:
        tracker.status = status
        tracker.progress = progress
    session.commit()
        
    return redirect(url_for('tracker_bp.tracker_ui'))

@tracker_bp.route('/remove_tracker/<int:tracker_id>', methods = ['POST'])
def remove_tracker(tracker_id):
    if 'Username' not in flaskSession:
        return redirect(url_for('authorization__bp.login'))
    
    tracker = session.query(User_Trackers).filter_by(tracker_id = tracker_id).first()
    if tracker:
        session.delete(tracker)
        session.commit()
        flash("Tracker was successfully removed.")
    else:
        flash("Tracker cannot be found")

    return redirect(url_for('tracker_bp.tracker_ui'))

@tracker_bp.route('/autocomplete_shows', methods = ['GET'])
def autocomplete_shows():
    if 'Username' not in flaskSession:
        return redirect(url_for('tracker_bp.tracker_ui'))
    
    show_query = request.args.get('q', '')

    if not show_query:
        return jsonify([])

    shows = session.query(Shows).filter((Shows.name.ilike(f'%{show_query}%')) | (Shows.genres.ilike(f'%{show_query}%'))).limit(10).all()
        #implement a better way to go through genres, most likely by normalizing the sql by making a genres table and creating a many to many relationship for shows to genres

        #for show in shows:
            #genres = [genre for genre in show.genres.split(',')]
            #if genre_query in genres:

    return jsonify([show.name for show in shows])