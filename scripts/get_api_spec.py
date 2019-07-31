import requests

if __name__ == "__main__":
	schema = requests.get('http://localhost:8080/schema')
	print(schema.text)