function onApplePayButtonClicked() { 

  if (!ApplePaySession) {
      return;
  }
  
  // Define ApplePayPaymentRequest
  const request = {
      "countryCode": "US",
      "currencyCode": "USD",
      "merchantCapabilities": ["supports3DS"],
      "supportedNetworks": ["visa", "masterCard", "amex", "discover"],
      "total": {
          "label": "Demo (Card is not charged)",
          "type": "final",
          "amount": "1.99"
      }
  };
  
  // Create ApplePaySession
  const session = new ApplePaySession(3, request);


  session.onvalidatemerchant = event => {
    // Call your own server to request a new merchant session.
    console.log(event);
    fetch('/applepay_validation')
      .then(res => res.json()) // Parse the response as JSON.
      .then(merchantSession => {
        session.completeMerchantValidation(merchantSession);
        console.log('Merchant session received:', merchantSession);
      })
      .catch(err => {
        console.error("Error fetching merchant session", err);
      });

  };


  session.onpaymentauthorized = event => {

      const paymentPayload = event.payment.token
      console.log(paymentPayload)

      fetch('https://tnt9141h1xs-87791d38-602d-4403-862c-59431c9a5150.sandbox.verygoodproxy.com/post', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(paymentPayload)
      })

      // Define ApplePayPaymentAuthorizationResult
      const result = {
          "status": ApplePaySession.STATUS_SUCCESS
      };
      session.completePayment(result);
  };
  

  session.oncancel = event => {
      // Payment canceled by WebKit
  };
  
  session.begin();

}

document.querySelector('apple-pay-button').addEventListener('click', onApplePayButtonClicked);


