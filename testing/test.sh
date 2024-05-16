#!/bin/bash
curl --fail 0.0.0.0:8081/checkout --header "Content-Type: application/json"  --request POST --data '{"user":{"name":"123","contact":"123"},"creditCard":{"number":"123","expirationDate":"12/34","cvv":"123"},"userComment":"","items":[{"name":"Learning Python","quantity":1}],"discountCode":"","shippingMethod":"","giftMessage":"","billingAddress":{"street":"123","city":"123","state":"123","zip":"123","country":"Estonia"},"giftWrapping":false,"termsAndConditionsAccepted":true,"notificationPreferences":["email"],"device":{"type":"Smartphone","model":"Samsung Galaxy S10","os":"Android 10.0.0"},"browser":{"name":"Chrome","version":"85.0.4183.127"},"appVersion":"3.0.0","screenResolution":"1440x3040","referrer":"https://www.google.com","deviceLanguage":"en-US"}'
