# Makefile para el backend de AdminNegocios

.PHONY: run install freeze clean

# Levanta el servidor de desarrollo con hot reload
run:
	uvicorn app.main:app --reload --port 8000

# Instala las dependencias desde requirements.txt
install:
	pip install -r requirements.txt

# Congela las dependencias actuales
freeze:
	pip freeze > requirements.txt

# Limpia archivos cache de Python
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
