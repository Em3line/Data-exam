default: pytest

pylint:
	find . -iname "*.py" -not -path "./tests/*" | xargs pylint --output-format=colorized; true

pytest:
	PYTHONDONTWRITEBYTECODE=1 pytest -v -s --color=yes
