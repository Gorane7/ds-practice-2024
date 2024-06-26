#!/usr/bin/bash

python setup_db.py

fails=0

parse_res () {
	# $1 is res
	# $2 is errcode
	# $3 is correct result id
	if [ -s $2 ]; then
		if [ $3 -eq 1 ]; then
			echo -en "\033[0;32mSuccess: "
		else
			fails=$(($fails+1))
			echo -en "\033[0;31mFailure: "
		fi
		echo -e "Order request failed with error message"
		cat $2
		echo -en "\033[m"
		> $2
	elif [[ $(echo $1 | jq -r .status) == "Order accepted" ]]; then
		if [ $3 -eq 2 ]; then
			echo -en "\033[0;32mSuccess: "
		else
			fails=$(($fails+1))
			echo -en "\033[0;31mFailure: "
		fi
		echo -e "Order was accepted\033[0m"
	else
		if [ $3 -eq 3 ]; then
			echo -en "\033[0;32mSuccess: "
		else
			fails=$(($fails+1))
			echo -en "\033[0;31mFailure: "
		fi
		echo -e "Order was not accepted\033[0m"
	fi

}

test1 () {
	echo "Running test 1: Single non-fraudulent order"
	errcode=$(mktemp)
	res=$(curl --fail --no-progress-meter 0.0.0.0:8081/checkout --header "Content-Type: application/json"  --request POST --data '{"user":{"name":"123","contact":"123"},"creditCard":{"number":"123","expirationDate":"12/34","cvv":"123"},"userComment":"","items":[{"name":"Learning Python","quantity":1}],"discountCode":"","shippingMethod":"","giftMessage":"","billingAddress":{"street":"123","city":"123","state":"123","zip":"123","country":"Estonia"},"giftWrapping":false,"termsAndConditionsAccepted":true,"notificationPreferences":["email"],"device":{"type":"Smartphone","model":"Samsung Galaxy S10","os":"Android 10.0.0"},"browser":{"name":"Chrome","version":"85.0.4183.127"},"appVersion":"3.0.0","screenResolution":"1440x3040","referrer":"https://www.google.com","deviceLanguage":"en-US"}' 2>$errcode)
	
	parse_res "$res" "$errcode" 2
}

test2 () {
	echo "Running test 2: Single fraudulent order"
	errcode=$(mktemp)
	res=$(curl --fail --no-progress-meter 0.0.0.0:8081/checkout --header "Content-Type: application/json"  --request POST --data '{"user":{"name":"123","contact":"123"},"creditCard":{"number":"666","expirationDate":"12/34","cvv":"123"},"userComment":"","items":[{"name":"Learning Python","quantity":1}],"discountCode":"","shippingMethod":"","giftMessage":"","billingAddress":{"street":"123","city":"123","state":"123","zip":"123","country":"Estonia"},"giftWrapping":false,"termsAndConditionsAccepted":true,"notificationPreferences":["email"],"device":{"type":"Smartphone","model":"Samsung Galaxy S10","os":"Android 10.0.0"},"browser":{"name":"Chrome","version":"85.0.4183.127"},"appVersion":"3.0.0","screenResolution":"1440x3040","referrer":"https://www.google.com","deviceLanguage":"en-US"}' 2>$errcode)

	parse_res "$res" "$errcode" 3
}

test3 () {
	echo "Running test 3: Single malformed order"
	errcode=$(mktemp)
	res=$(curl --fail --no-progress-meter 0.0.0.0:8081/checkout --header "Content-Type: application/json"  --request POST --data '{"userr":{"name":"123","contact":"123"},"creditCard":{"number":"123","expirationDate":"12/34","cvv":"123"},"userComment":"","items":[{"name":"Learning Python","quantity":1}],"discountCode":"","shippingMethod":"","giftMessage":"","billingAddress":{"street":"123","city":"123","state":"123","zip":"123","country":"Estonia"},"giftWrapping":false,"termsAndConditionsAccepted":true,"notificationPreferences":["email"],"device":{"type":"Smartphone","model":"Samsung Galaxy S10","os":"Android 10.0.0"},"browser":{"name":"Chrome","version":"85.0.4183.127"},"appVersion":"3.0.0","screenResolution":"1440x3040","referrer":"https://www.google.com","deviceLanguage":"en-US"}' 2>$errcode)

	parse_res "$res" "$errcode" 1
}

test4 () {
	echo "Running test 4: Running 7 instaces of mixed fraudulent and non-fraudulent requests in rapid succession with overlaps"
	fails=0
	for i in $(seq 0 6); do
		r=0
		if [ $(echo $i % 2 | bc) -eq 0 ]; then
			test1 &>/dev/null &
		else
			test2 &>/dev/null &
		fi
	done
	wait
	if [[ $fails == 0 ]]; then
		echo -en "\033[0;32m"
	else
		echo -en "\033[0;31m"
	fi
	echo -e "$fails orders failed out of 7\033[0m"
}

TIMEFORMAT="Time taken: %3R"
time test1
echo
time test2
echo
time test3
echo
time test4
