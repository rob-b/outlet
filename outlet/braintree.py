import braintree

from outlet import settings

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.MERCHANT_ID,
                                  public_key=settings.PUBLIC_KEY,
                                  private_key=settings.PRIVATE_KEY)


# for reference, here are the valid testing nonces
class Nonces(object):
    Transactable = "fake-valid-nonce"
    Consumed = "fake-consumed-nonce"
    PayPalOneTimePayment = "fake-paypal-one-time-nonce"
    PayPalFuturePayment = "fake-paypal-future-nonce"
    PayPalBillingAgreement = "fake-paypal-billing-agreement-nonce"
    ApplePayVisa = "fake-apple-pay-visa-nonce"
    ApplePayMasterCard = "fake-apple-pay-mastercard-nonce"
    ApplePayAmEx = "fake-apple-pay-amex-nonce"
    AbstractTransactable = "fake-abstract-transactable-nonce"
    Europe = "fake-europe-bank-account-nonce"
    Coinbase = "fake-coinbase-nonce"
    AndroidPayCard = "fake-android-pay-nonce"
    AndroidPayCardDiscover = "fake-android-pay-discover-nonce"
    AndroidPayCardVisa = "fake-android-pay-visa-nonce"
    AndroidPayCardMasterCard = "fake-android-pay-mastercard-nonce"
    AndroidPayCardAmEx = "fake-android-pay-amex-nonce"
    AmexExpressCheckoutCard = "fake-amex-express-checkout-nonce"
    VenmoAccount = "fake-venmo-account-nonce"
    TransactableVisa = "fake-valid-visa-nonce"
    TransactableAmEx = "fake-valid-amex-nonce"
    TransactableMasterCard = "fake-valid-mastercard-nonce"
    TransactableDiscover = "fake-valid-discover-nonce"
    TransactableJCB = "fake-valid-jcb-nonce"
    TransactableMaestro = "fake-valid-maestro-nonce"
    TransactableDinersClub = "fake-valid-dinersclub-nonce"
    TransactablePrepaid = "fake-valid-prepaid-nonce"
    TransactableCommercial = "fake-valid-commercial-nonce"
    TransactableDurbinRegulated = "fake-valid-durbin-regulated-nonce"
    TransactableHealthcare = "fake-valid-healthcare-nonce"
    TransactableDebit = "fake-valid-debit-nonce"
    TransactablePayroll = "fake-valid-payroll-nonce"
    TransactableNoIndicators = "fake-valid-no-indicators-nonce"
    TransactableUnknownIndicators = "fake-valid-unknown-indicators-nonce"
    TransactableCountryOfIssuanceUSA = "fake-valid-country-of-issuance-usa-nonce"
    TransactableCountryOfIssuanceCAD = "fake-valid-country-of-issuance-cad-nonce"
    TransactableIssuingBankNetworkOnly = "fake-valid-issuing-bank-network-only-nonce"
    ProcessorDeclinedVisa = "fake-processor-declined-visa-nonce"
    ProcessorDeclinedMasterCard = "fake-processor-declined-mastercard-nonce"
    ProcessorDeclinedAmEx = "fake-processor-declined-amex-nonce"
    ProcessorDeclinedDiscover = "fake-processor-declined-discover-nonce"
    ProcessorFailureJCB = "fake-processor-failure-jcb-nonce"
    LuhnInvalid = "fake-luhn-invalid-nonce"
    PayPalFuturePaymentRefreshToken = "fake-paypal-future-refresh-token-nonce"
    SEPA = "fake-sepa-bank-account-nonce"
    GatewayRejectedFraud = "fake-gateway-rejected-fraud-nonce"
