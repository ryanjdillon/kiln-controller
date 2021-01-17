black:
	black --exclude "/(\.eggs|\.git|\.venv|build|dist|loopfront/internal/migrations|loopfront/internal/dev_migrations|loopfront/internal/static/sass/node_modules)/" ./

docs:
	cd ./docs && $(MAKE) html

.PHONY: black
