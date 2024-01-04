from flask import (
    Flask,
    render_template,
    request,
    render_template_string,
    session,
    redirect,
    url_for,
)
import os
from flask.blueprints import Blueprint
from .jobs import ManagerProcess


class JobManager:
    tasks = ManagerProcess()
    password_key = None

    def __init__(self, app: Flask = None, password_key=None):
        if app:
            self.init_app(app)

        if password_key:
            self.set_password_key(password_key)

    def set_password_key(self, password_key):
        self.password_key = password_key

    def init_app(self, app: Flask):
        self.app = app
        self.app.extensions["job_manager"] = self
        app.extensions["job_manager"] = self
        if not self.password_key:
            password = os.environ.get("JOB_MANAGER_PASSWORD_KEY")
            if not password:
                if not app.secret_key:
                    raise ValueError("JOB_MANAGER_PASSWORD_KEY não definido!")
                password = app.secret_key
            self.set_password_key(password)
        self.blueprint = self.create_blueprint()
        self.add_urls(self.blueprint)
        app.register_blueprint(self.blueprint)
        return self

    def jobs(self, uuid=None):
        if not self.is_logged():
            return redirect(url_for("job_manager.login"))
        if request.method == "DELETE":
            processo = self.tasks.stop(uuid)
            component = self.render_job(uuid, processo)
            return component
        elif request.method == "POST":
            processo = self.tasks.restart(uuid)
            component = self.render_job(uuid, processo)
            return component
        data = {"jobs": tuple(self.tasks)}
        return render_template("/job_manager/index.html", data=data)

    def check_password(self, password):
        return password == self.password_key

    def set_logged(self):
        session["job_login"] = True

    def is_logged(self):
        return session.get("job_login", False)

    def set_logout(self):
        session.pop("job_login", None)

    def login(self):
        errors = {}
        if request.method == "POST":
            if self.check_password(request.form.get("acesso")):
                self.set_logged()
                return redirect(url_for("job_manager.jobs"))
            errors = {"acesso": "Login invalido!"}
        return render_template("/job_manager/login.html", errors=errors)

    def logout(self):
        self.set_logout()
        return redirect(url_for("job_manager.login"))

    def register_blueprint(self, blueprint: Blueprint):
        self.app.register_blueprint(blueprint)

    def add_urls(self, blueprint: Blueprint):
        blueprint.add_url_rule("/", "jobs", self.jobs)

    def create_blueprint(self, url_prefix="/jobs"):
        blueprint = Blueprint(
            "job_manager",
            __name__,
            url_prefix=url_prefix,
            template_folder="templates",
        )
        blueprint.add_url_rule(
            "/login/",
            "login",
            self.login,
            methods=["GET", "POST"],
        )
        blueprint.add_url_rule(
            "/",
            "jobs",
            self.jobs,
            methods=["GET"],
        )
        blueprint.add_url_rule(
            "/<uuid:uuid>/",
            "jobs-uuid",
            self.jobs,
            methods=["DELETE", "POST"],
        )
        blueprint.add_url_rule(
            "/logout/",
            "logout",
            self.logout,
            methods=["GET"],
        )
        return blueprint

    def render_job(self, uuid, job=None):
        component = """
        {% from 'job_manager/_component_job_macro.html' import ComponentJob %}
        {{
            ComponentJob(
                uuid=job.uuid,
                grupo=job.group,
                titulo=job.name,
                descricao=job.description,
                is_running=job.is_running,
                is_task=job.is_task,
                last_run=job.last_run,
                stoped=job.stoped
            )
        }}"""
        if job:
            component = render_template_string(
                component,
                job=job,
            )
        else:
            component = render_template_string(
                component,
                job=self.tasks.find_by_uuid(uuid),
            )

        return component
