from flask import Flask, render_template, redirect, url_for, request
from models import db
from auth import auth_bp
from flask_login import LoginManager, login_required, current_user
from auth import role_required
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    # D17: Environment switch for DB_BACKEND
    db_backend = os.environ.get('DB_BACKEND', 'sqlite').lower()
    
    if db_backend == 'mysql':
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '3306')
        db_name = os.environ.get('DB_NAME', 'water_elixir')
        db_user = os.environ.get('DB_USERNAME', 'water_app_user')
        import urllib.parse
        raw_pass = os.environ.get('DB_PASSWORD', '')
        db_pass = urllib.parse.quote_plus(raw_pass)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    else:
        # Default SQLite mode
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///water_app.db?timeout=15'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # D12: Flask login users stay in auth SQLite
    app.config['SQLALCHEMY_BINDS'] = {
        'auth': 'sqlite:///users.db'
    }

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User, Zone, Alert, Complaint, Ticket, Reading

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.route('/manager')
    @login_required
    @role_required('manager')
    def manager_dashboard():
        zones = Zone.query.all()
        alerts = Alert.query.order_by(Alert.created_at.desc()).limit(10).all()
        complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(10).all()
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(10).all()
        workers = User.query.filter_by(role='worker').all()
        users_map = {u.id: u for u in User.query.all()}
        return render_template('manager.html', zones=zones, alerts=alerts, complaints=complaints, tickets=tickets, workers=workers, users=users_map)

    
    @app.route('/auto_assign', methods=['POST'])
    @login_required
    def auto_assign():
        if current_user.role != 'manager':
            return "Unauthorized", 403
        unassigned_tickets = Ticket.query.filter_by(assigned_worker_id=None).order_by(Ticket.created_at.desc()).limit(10).all()
        workers = User.query.filter_by(role='worker').all()
        if workers and unassigned_tickets:
            import itertools
            worker_cycle = itertools.cycle(workers)
            for ticket in unassigned_tickets:
                ticket.assigned_worker_id = next(worker_cycle).id
                ticket.status = 'assigned'
            db.session.commit()
        return redirect(url_for('manager_dashboard') + '#tab-tickets')


    @app.route('/update_ticket_status/<int:ticket_id>', methods=['POST'])
    @login_required
    @role_required('worker')
    def update_ticket_status(ticket_id):
        notes = request.form.get('notes')
        status = request.form.get('status')
        ticket = Ticket.query.get(ticket_id)
        if ticket and ticket.assigned_worker_id == current_user.id:
            ticket.status = status
            ticket.worker_notes = notes
            from datetime import datetime
            if status == 'RESOLVED' or status == 'resolved':
                ticket.resolved_at = datetime.utcnow()
                if ticket.complaint:
                    ticket.complaint.status = 'resolved'
            db.session.commit()
        return redirect(url_for('worker_dashboard'))

    @app.route('/worker', methods=['GET', 'POST'])

    @login_required
    @role_required('worker')
    def worker_dashboard():
        if request.method == 'POST':
            ticket_id = request.form.get('ticket_id')
            notes = request.form.get('notes')
            ticket = Ticket.query.get(ticket_id)
            if ticket and ticket.assigned_worker_id == current_user.id:
                ticket.status = 'resolved'
                ticket.worker_notes = notes
                ticket.resolved_at = datetime.utcnow()
                
                if ticket.alert:
                    ticket.alert.status = 'resolved'
                if ticket.complaint:
                    ticket.complaint.status = 'resolved'
                    
                # Reopen valve on resolution
                if ticket.zone:
                    ticket.zone.valve_state = 'OPEN'
                    
                db.session.commit()
                
        tickets = Ticket.query.filter_by(assigned_worker_id=current_user.id).all()
        return render_template('worker.html', tickets=tickets)

    @app.route('/student', methods=['GET', 'POST'])
    @login_required
    @role_required('student')
    def student_dashboard():
        if request.method == 'POST':
            zone_id = request.form.get('zone_id')
            description = request.form.get('description')
            complaint = Complaint(student_id=current_user.id, zone_id=zone_id, description=description)
            db.session.add(complaint)
            db.session.commit()
            
        complaints = Complaint.query.filter_by(student_id=current_user.id).order_by(Complaint.created_at.desc()).all()
        zones = Zone.query.all()
        return render_template('student.html', complaints=complaints, zones=zones)

    @app.route('/auto_assign_complaint/<int:complaint_id>', methods=['POST'])
    @login_required
    @role_required('manager')
    def auto_assign_complaint(complaint_id):
        complaint = Complaint.query.get(complaint_id)
        workers = User.query.filter_by(role='worker').all()
        if complaint and workers:
            import random
            worker = random.choice(workers)
            ticket = Ticket(
                complaint_id=complaint.id,
                zone_id=complaint.zone_id,
                assigned_worker_id=worker.id,
                status='assigned'
            )
            complaint.status = 'in_progress'
            db.session.add(ticket)
            db.session.commit()
        return redirect(url_for('manager_dashboard') + '#tab-complaints')

    @app.route('/assign_ticket', methods=['POST'])
    @login_required
    @role_required('manager')
    def assign_ticket():
        ticket_id = request.form.get('ticket_id')
        worker_id = request.form.get('worker_id')
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            ticket.assigned_worker_id = worker_id
            ticket.status = 'assigned'
            db.session.commit()()
        return redirect(url_for('manager_dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    # Ensure databases are created on first run
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5000, use_reloader=False)
