with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

auto_assign_code = '''
@app.route('/auto_assign', methods=['POST'])
@login_required
def auto_assign():
    if current_user.role != 'manager':
        return "Unauthorized", 403
    unassigned_tickets = Ticket.query.filter_by(assigned_worker_id=None).limit(10).all()
    workers = User.query.filter_by(role='worker').all()
    if workers and unassigned_tickets:
        import itertools
        worker_cycle = itertools.cycle(workers)
        for ticket in unassigned_tickets:
            ticket.assigned_worker_id = next(worker_cycle).id
            ticket.status = 'IN_PROGRESS'
        db.session.commit()
    return redirect(url_for('manager_dashboard'))

@app.route('/worker', methods=['GET', 'POST'])
'''

content = content.replace("@app.route('/worker', methods=['GET', 'POST'])", auto_assign_code)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
