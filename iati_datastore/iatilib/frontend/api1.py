import sqlalchemy as sa
from flask import request, Response, Blueprint, jsonify, abort
from flask.views import MethodView
from werkzeug.datastructures import MultiDict
from flask.ext.sqlalchemy import Pagination

from iatilib import db
from iatilib.model import Activity, Transaction

from . import dsfilter, validators, serialize


api = Blueprint('api', __name__)


@api.route('/about')
def about():
    # General status info
    count_activity = db.session.query(Activity).count()
    count_transaction = db.session.query(Transaction).count()
    return jsonify(
        ok=True,
        status='healthy',
        indexed_activities=count_activity,
        indexed_transactions=count_transaction
    )


class DataStoreView(MethodView):
    filter = None
    serializer = None

    @property
    def streaming(self):
        return self.validate_args().get("stream", False)

    def paginate(self, query, page, per_page):
        if page < 1:
            abort(404)
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1:
            abort(404)
        return Pagination(query, page, per_page, query.count(), items)

    def validate_args(self):
        if not hasattr(self, "_valid_args"):
            try:
                self._valid_args = validators.activity_api_args(MultiDict(request.args))
            except validators.Invalid:
                abort(404)
        return self._valid_args

    def get_response(self, serializer=None, mimetype="text/csv"):
        if serializer is None:
            serializer = self.serializer

        valid_args = self.validate_args()
        query = self.filter(valid_args)

        if self.streaming:
            query = query.yield_per(100)
            body = serializer(query)
        else:
            pagination = self.paginate(
                query,
                valid_args.get("page", 1),
                valid_args.get("per_page", 50),
            )
            body = u"".join(serializer(pagination.items))
        return Response(body, mimetype=mimetype)


class ActivityView(DataStoreView):
    filter = staticmethod(dsfilter.activities)

    def get(self, format):
        forms = {
            ".xml": (serialize.xml, "application/xml"),
            ".json": (serialize.json, "application/json"),  # rfc4627
            ".csv": (serialize.csv, "text/csv")  # rfc4180
        }
        if format not in forms:
            abort(404)
        return self.get_response(*forms[format])


class DataStoreCSVView(DataStoreView):
    def get(self, format=".csv"):
        if not request.path.endswith("csv"):
            abort(404)
        return self.get_response()


class ActivityByCountryView(DataStoreCSVView):
    filter = staticmethod(dsfilter.activities_by_country)
    serializer = staticmethod(serialize.csv_activity_by_country)


class ActivityBySectorView(DataStoreCSVView):
    filter = staticmethod(dsfilter.activities_by_sector)
    serializer = staticmethod(serialize.csv_activity_by_sector)


class TransactionsView(DataStoreCSVView):
    filter = staticmethod(dsfilter.transactions)
    serializer = staticmethod(serialize.transaction_csv)


class TransactionsByCountryView(DataStoreCSVView):
    filter = staticmethod(dsfilter.transactions_by_country)
    serializer = staticmethod(serialize.csv_transaction_by_country)


class TransactionsBySectorView(DataStoreCSVView):
    filter = staticmethod(dsfilter.transactions_by_sector)
    serializer = staticmethod(serialize.csv_transaction_by_sector)


class BudgetsView(DataStoreCSVView):
    filter = staticmethod(dsfilter.budgets)
    serializer = staticmethod(serialize.budget_csv)


class BudgetsByCountryView(DataStoreCSVView):
    filter = staticmethod(dsfilter.budgets_by_country)
    serializer = staticmethod(serialize.csv_budget_by_country)


class BudgetsBySectorView(DataStoreCSVView):
    filter = staticmethod(dsfilter.budgets_by_sector)
    serializer = staticmethod(serialize.csv_budget_by_sector)


api.add_url_rule(
    '/access/activities',
    defaults={"format": ".json"},
    view_func=ActivityView.as_view('activities')
)

api.add_url_rule(
    '/access/activities<format>',
    view_func=ActivityView.as_view('activities')
)

api.add_url_rule(
    '/access/activities/by_country<format>',
    view_func=ActivityByCountryView.as_view('activities_by_country'))

api.add_url_rule(
    '/access/activities/by_sector<format>',
    view_func=ActivityBySectorView.as_view('activities_by_sector'))

api.add_url_rule(
    '/access/transactions<format>',
    view_func=TransactionsView.as_view('transactions_list'))

api.add_url_rule(
    '/access/transactions/by_country<format>',
    view_func=TransactionsByCountryView.as_view('transactions_by_country'))

api.add_url_rule(
    '/access/transactions/by_sector<format>',
    view_func=TransactionsBySectorView.as_view('transactions_by_sector'))

api.add_url_rule(
    '/access/budgets<format>',
    view_func=BudgetsView.as_view('budgets_list'))

api.add_url_rule(
    '/access/budgets/by_country<format>',
    view_func=BudgetsByCountryView.as_view('budgets_by_country'))

api.add_url_rule(
    '/access/budgets/by_sector<format>',
    view_func=BudgetsBySectorView.as_view('budgets_by_sector'))