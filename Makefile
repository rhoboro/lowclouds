test:
	poetry run isort lowclouds
	poetry run black lowclouds
	poetry run flake8 lowclouds
	poetry run mypy lowclouds
