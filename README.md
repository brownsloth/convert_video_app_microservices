## Directory structure:
.
├── README.md
└── python
    └── src
        └── auth : code for the auth service
            ├── Dockerfile : instructions to deploy auth service as a docker image
            ├── init.sql : auth db to authenticate the user against
            ├── manifests : instructions to launch the auth docker image in a kubernetes cluster
            │   ├── auth-deploy.yaml
            │   ├── configmap.yaml
            │   ├── secret.yaml
            │   └── service.yaml
            ├── requirements.txt
            ├── server.py
            └── venv

## Steps:
1. cd python/src/auth
2. python3 -m venv venv
3. source ./venv/bin/activate 
4. check venv is activated env | grep VIRTUAL_ENV
5. pip install pyjwt
6. pip install flask
7. https://blogs.cuit.columbia.edu/jp3864/2020/07/01/installing-flask-mysqldb-debug-and-solution/ AND THEN pip install flask_mysqldb
8. subl init.sql
9. brew install mysql AND brew services start mysql (keeps running mysql in background on every restart)
9. mysql -uroot
	9a. show databases (check that there's no auth database already)
10. mysql -uroot < init.sql
	- if you fixed a problem with the sql script and ran it again, run `mysql -uroot -e "DROP DATABASE auth"` and `mysql -uroot -e "DROP USER auth_user@localhost"` before rerunning the above command
11. subl server.py
12. subl Dockerfile
13. pip3 freeze > requirements.txt
13. docker build .
14. create a repo "auth" on docker hub
15. Tag the image: docker tag <sha> <docker user>/auth:latest
16. docker push 1starun8/auth:latest
17. mkdir manifests (this will contain kubernetes config .yaml files)
18. cd manifests
19. Create infra code for kubernetes deployment:  auth-deploy.yaml, configmap.yaml, secret.yaml and service.yaml
20. Deploying auth service to the cluster:
	- minikube start
	- install k9s:  HOMEBREW_NO_AUTO_UPDATE=1 brew install derailed/k9s/k9s
	- k9s
	- kubectl apply -f ./. -> creates a cluster WITH OUR INFRA CODE
	- k9s -> pods -> containers -> server:
		- i saw an error here, due to flask version incompatibility with flask_mysqldb
		- now we need to: 
			- make a change: pip uninstall flask, pip install flask==2.3.3, pip3 freeze > requirements.txt
			- update the image: 
				- see all images: docker image ls
				- remove old image: docker image rm 1starun8/auth
				- rebuild: docker build . AND docker tag <sha> <docker user>/auth:latest
			- push updated image to repo: docker push 1starun8/auth:latest
			- make kubectl pull the updated image: It has automatically pulled the updated image! maybe because :latest is the tag or because of the policies we configured in the yaml files
	- 
