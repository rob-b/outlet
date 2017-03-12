Setup
-----
To install the app run::
  python setup.py develop

To setup the db::
  createdb outlet
  DB_URL='postgresql://@/outlet' createoutletdb

Run the application::
  DB_URL='postgresql://@/outlet' gunicorn outlet.server:app

To view the available nonces for testing with::
  curl -H "content-type: application/json" -sv localhost:8000/test

Hit the api::
  curl -H "content-type: application/json" -sv -d '{"amount":"10.25", "user_id": 3001, "account_id": 1, "nonce": "fake-luhn-invalid-nonce"}' localhost:8000

To run the tests create a test db::
  createdb outlet_test
  DB_URL='postgresql://@/outlet_test' python setup.up test
