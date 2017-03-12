import falcon
from outlet import services
from outlet.braintree import braintree
from voluptuous import Invalid


class TransactionResource:
    @falcon.after(services.after_create_transaction)
    def on_post(self, req, resp):
        doc = req.context['doc']
        try:
            services.transaction_schema(doc)
        except Invalid as err:
            raise falcon.HTTPBadRequest(str(err))

        req.context['result_type'] = services.create_user_transaction(
            self.session,
            doc['user_id'],
            services.GBP(doc['amount']),
            doc['account_id'],
        )


class ClientResource:
    def on_get(self, req, resp):
        data = {'token': braintree.ClientToken.generate()}
        req.context['result'] = {'data': data}
