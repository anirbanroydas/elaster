#!/bin/sh
set -e

if [ "$ENV" = "DEV" ]; then
	echo "Running Development Application"
	pip install --no-deps -e .
	if [ -n "$EXAMPLE" ]; then
		if [ -n "$DATASET_PATH" ]; then
			exec python elaster/server.py --example="$EXAMPLE" --datapath="$DATASET_PATH"
		else
			exec python elaster/server.py --example="$EXAMPLE"
		fi
	else	
		exec python elaster/server.py
	fi


elif [ "$ENV" = "UNIT_TEST" ]; then
	echo "Running Unit Tests"
	pip install --no-deps -e .
	exec pytest -v -s --cov=./elaster tests/unit 
	# exec tox -e unit

elif [ "$ENV" = "CONTRACT_TEST" ]; then
	echo "Running Contract Tests"
	pip install --no-deps -e .
	exec pytest -v -s --cov=./elaster tests/contract
	# exec tox -e contract

elif [ "$ENV" = "INTEGRATION_TEST" ]; then
	echo "Running Integration Tests"
	pip install --no-deps -e .
	exec pytest -v -s --cov=./elaster tests/integration
	# exec tox -e integration

elif [ "$ENV" = "COMPONENT_TEST" ]; then
	echo "Running Component Tests"
	pip install --no-deps .
	exec python elaster/server.py

elif [ "$ENV" = "END_TO_END_TEST" ]; then
	echo "Running End_To_End Tests"
	pip install --no-deps .
	exec python elaster/server.py

elif [ "$ENV" = "LOAD" ]; then
	echo "Running Load Tests"
	pip install --no-deps .
	exec python elaster/server.py

elif [ "$ENV" = "PROD" ]; then 
	echo "Running Production Application"
	pip install --no-deps .
	exec python elaster/server.py

else
	echo "Please provide an environment"
	echo "Stopping"
fi
