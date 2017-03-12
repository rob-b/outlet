import braintree

from outlet import settings

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.MERCHANT_ID,
                                  public_key=settings.PUBLIC_KEY,
                                  private_key=settings.PRIVATE_KEY)
