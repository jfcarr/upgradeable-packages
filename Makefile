SCRIPT_BASE_NAME = upgradeable_packages

default:
	@echo 'Targets:'
	@echo '  mod     -- make script executable'
	@echo '  deploy  -- deploy script'

mod:
	chmod u+x $(SCRIPT_BASE_NAME).py

deploy: mod
	cp $(SCRIPT_BASE_NAME).py $(HOME)/bin/$(SCRIPT_BASE_NAME)
