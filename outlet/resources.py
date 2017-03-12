import falcon
from attr import attrs, attrib
from outlet import services
from outlet.braintree import braintree, Nonces
from voluptuous import Invalid


@attrs
class TransactionParams:
    # since this params seem to be required together a lot
    # https://martinfowler.com/bliki/DataClump.html
    session = attrib()
    user_id = attrib()
    account_id = attrib()
    amount = attrib(convert=services.GBP)
    nonce = attrib()


class TransactionResource:
    @falcon.after(services.after_create_transaction)
    def on_post(self, req, resp):
        doc = req.context.get('doc', {})
        try:
            services.transaction_schema(doc)
        except Invalid as err:
            raise falcon.HTTPBadRequest(str(err))

        params = TransactionParams(session=self.session, **doc)
        req.context['result_type'] = services.create_account_transaction(
            params
        )


class ClientResource:
    def on_get(self, req, resp):
        data = {'token': braintree.ClientToken.generate()}
        req.context['result'] = {'data': data}


class TestResource:
    def on_get(self, req, resp):
        data = [v for k, v in Nonces.__dict__.items() if not
                k.startswith('__')]
        req.context['result'] = {'data': data}
