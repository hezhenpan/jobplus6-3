from flask import Blueprint, render_template, current_app, request
from jobplus.models import JobInfo as Job

jobs = Blueprint('jobs', __name__, url_prefix='/job')


@jobs.route('/')
def index():
    page = request.args.get('page', 1, int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )

    return render_template('jobs/index.html', pagination=pagination, active='job')



