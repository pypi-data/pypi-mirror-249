from flask import Flask
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView


class RuleRouter:
    ABSTRACT_METHOD = None
    ABSTRACT_ROUTERMETHOD = None
    ABSTRACT_ROUTER = None

    IGNORE_PREFIX_IN = []
    _IGNORE_PREFIX_IN = ("/admin", "/static", *IGNORE_PREFIX_IN)
    IGNORE_METHODS = []
    _IGNORE_METHODS = ("HEAD", "OPTIONS", *IGNORE_METHODS)

    def __init__(self, app=None, db=None):
        if app:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        self.app: Flask = app
        self.app.extensions["rule_router"] = self
        if db:
            self.init_tables(db)

    def mapper_rules(self):
        rules = tuple(self.app.url_map.iter_rules())
        for _rule in rules:
            uri = _rule.rule
            if uri.startswith(self._IGNORE_PREFIX_IN):
                continue
            endpoint = _rule.endpoint
            subdomain = _rule.subdomain
            methods = _rule.methods
            methods = filter(lambda x: x not in self._IGNORE_METHODS, methods)
            yield {
                "endpoint": endpoint,
                "uri": uri,
                "subdomain": subdomain,
                "methods": methods,
            }

    def get_abstratc_method(self, db):
        return self.ABSTRACT_METHOD or db.Model

    def get_abstratc_routermethod(self, db):
        return self.ABSTRACT_ROUTERMETHOD or db.Model

    def get_abstratc_router(self, db):
        return self.ABSTRACT_ROUTER or db.Model

    def init_tables(self, db):
        self.db = db

        class Method(self.get_abstratc_method(db)):
            __tablename__ = "Method"
            id = Column(Integer, primary_key=True)
            rule = Column(String(10), nullable=False, unique=True)

            routers = relationship("RouterMethod", backref="Method", lazy=True)

            def __repr__(self):
                return f"<Method {self.rule}>"

        class RouterMethod(self.get_abstratc_routermethod(db)):
            __tablename__ = "RouterMethod"
            id = Column(Integer, primary_key=True)
            router_endpoint = Column(
                String(100),
                ForeignKey("Router.endpoint"),
                nullable=False,
            )
            method_rule = Column(
                String(10),
                ForeignKey("Method.rule"),
                nullable=False,
            )
            active = Column(Boolean, nullable=False, default=True)
            custom = Column(Boolean, nullable=False, default=False)

            __table_args__ = (
                UniqueConstraint(
                    "router_endpoint",
                    "method_rule",
                    name="unique_endpoint_method",
                ),
            )

            def __repr__(self):
                args = f"{self.router_endpoint}:{self.method_rule}"
                return f"<RouterMethod {args}>"

        class Router(self.get_abstratc_router(db)):
            __tablename__ = "Router"
            id = Column(Integer, primary_key=True)
            endpoint = Column(String(100), nullable=False, unique=True)
            uri = Column(String(100), nullable=False)
            subdomain = Column(String(100), nullable=True)
            description = Column(String(200), nullable=True)
            active = Column(Boolean, nullable=False, default=True)

            methods = relationship("RouterMethod", backref="Router", lazy=True)

            def __repr__(self):
                return f"<Router {self.endpoint}>"

        self.Router = Router
        self.RouterMethod = RouterMethod
        self.Method = Method

    def _create_methods(self, _methods: tuple, storage: dict):
        response = []
        for method in _methods:
            if method not in storage:
                m = self.Method.query.filter_by(rule=method).first()
                if not m:
                    m = self.Method(rule=method)
                    self.db.session.add(m)
                    self.db.session.flush()
                storage[method] = m
                response.append(m)
            else:
                response.append(storage[method])
        return response

    def _create_router(self, endpoint, uri, subdomain, description, active):
        router = self.Router.query.filter_by(endpoint=endpoint).first()
        if not router:
            router = self.Router(
                endpoint=endpoint,
                uri=uri,
                subdomain=subdomain,
                description=description,
                active=active,
            )
            self.db.session.add(router)
            self.db.session.flush()
        else:
            router.uri = uri
            router.subdomain = subdomain
            router.description = description or router.description
            router.active = active
        return router

    def _create_relation_router_method(self, router, methods):
        for method in methods:
            router_method = self.RouterMethod.query.filter_by(
                router_endpoint=router.endpoint,
                method_rule=method.rule,
            ).first()
            if not router_method:
                router_method = self.RouterMethod(
                    router_endpoint=router.endpoint,
                    method_rule=method.rule,
                )
                self.db.session.add(router_method)
                self.db.session.flush()
            else:
                router_method.active = True
            router.methods.append(router_method)
        methods = tuple(map(lambda method: method.rule, methods))
        for router_method in router.methods:
            if router_method.custom:
                continue
            if router_method.method_rule not in methods:
                router_method.active = False

    def init_permissions(self):
        with self.app.app_context():
            methods = {}
            for rule in self.mapper_rules():
                _methods = self._create_methods(rule["methods"], methods)
                _router = self._create_router(
                    endpoint=rule["endpoint"],
                    uri=rule["uri"],
                    subdomain=rule["subdomain"],
                    description=None,
                    active=True,
                )
                self._create_relation_router_method(_router, _methods)
            self.db.session.commit()

    def init_view(self, _is_accessible=lambda: True):
        admin = self.app.extensions.get("admin")
        if admin:
            admin = admin[0]
            columns = tuple(
                map(
                    lambda x: x.name,
                    filter(
                        lambda column: column.name != "id",
                        self.RouterMethod.__table__.columns,
                    ),
                )
            )

            class GenericView(ModelView):
                def is_accessible(self):
                    return _is_accessible()

            class RouterMethodView(GenericView):
                column_list = columns
                form_columns = columns

            admin.add_view(
                GenericView(
                    self.Router,
                    self.db.session,
                    category="Permissions",
                )
            )
            admin.add_view(
                RouterMethodView(
                    self.RouterMethod,
                    self.db.session,
                    category="Permissions",
                ),
            )
            admin.add_view(
                GenericView(
                    self.Method,
                    self.db.session,
                    category="Permissions",
                )
            )
        else:
            raise Exception("Instancia de ADMIN não foi encontrada")
