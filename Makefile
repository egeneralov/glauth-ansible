

test-playbook:
	ansible-playbook -i tests/{inventory,test.yml}

setup-osx:
	sudo /usr/bin/python -m pip install -r library/requirements.txt 

library-yaml2toml-test:
	cat library/yaml2toml-test.json | python3 library/yaml2toml.py
	cat library/yaml2toml-test.json | python3 library/yaml2toml.py 2>/dev/null | jq
	cat library/yaml2toml-test.json | python3 library/yaml2toml.py 2>/dev/null | jq -r .output
