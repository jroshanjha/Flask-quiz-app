## environment
python -m venv myenv

## Docker runs with the following
docker build -t welcome-app .
docker images 


## Run Dockers
docker run -p 5000:5000 welcome-app

## docker port , host
docker psc

## push docker image into docker container
docker login ( jroshan123)

docker image rm -f welcome-app 

# rename 
docker tag jroshan123/welcome-app jroshan123/welcome-app1 


# push 
docker push jroshan123/welcome-app1
docker push jroshan123/welcome-app:lates

docker pull jroshan123/welcome-app1:latest

docker run -d -p 8080:8080 jroshan123/welcome-app1:latest

