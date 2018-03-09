node("master"){
    def appName = 'flask-web'
    def imageTag = "${appName}:${env.BUILD_NUMBER}"

    checkout scm

    stage 'Build-Docker-Image'
    echo "Build new docker image ${imageTag}"
    sh("sudo docker build -t ${imageTag} ./src")

    stage 'Deploy Application'
    sh("sed -i.bak 's#docker_web#${imageTag}#' ./docker-compose/docker-compose.yml")
    echo "Build completed successfully!"
}