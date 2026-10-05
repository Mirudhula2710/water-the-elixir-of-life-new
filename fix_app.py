with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('@app.route(\'/auto_assign'):
        new_lines.append('    ' + line)
    elif line.startswith('@login_required') and new_lines and '@app.route(\'/auto_assign' in new_lines[-1]:
        new_lines.append('    ' + line)
    elif line.startswith('def auto_assign():'):
        new_lines.append('    ' + line)
    elif line.startswith('    if current_user.role != \'manager\':'):
        new_lines.append('    ' + line)
    elif line.startswith('        return "Unauthorized", 403'):
        new_lines.append('    ' + line)
    elif line.startswith('    unassigned_tickets ='):
        new_lines.append('    ' + line)
    elif line.startswith('    workers ='):
        new_lines.append('    ' + line)
    elif line.startswith('    if workers and unassigned_tickets:'):
        new_lines.append('    ' + line)
    elif line.startswith('        import itertools'):
        new_lines.append('    ' + line)
    elif line.startswith('        worker_cycle = itertools.cycle('):
        new_lines.append('    ' + line)
    elif line.startswith('        for ticket in unassigned_tickets:'):
        new_lines.append('    ' + line)
    elif line.startswith('            ticket.assigned_worker_id = '):
        new_lines.append('    ' + line)
    elif line.startswith('            ticket.status = '):
        new_lines.append('    ' + line)
    elif line.startswith('        db.session.commit()'):
        new_lines.append('    ' + line)
    elif line.startswith('    return redirect(url_for(\'manager_dashboard\'))'):
        new_lines.append('    ' + line)
    elif line.startswith('@app.route(\'/worker\', methods=['):
        new_lines.append('    ' + line)
    else:
        new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
