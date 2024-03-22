pipeline {
  agent any

  environment {
    DOCKER_IMAGE_NAME = 'my-coffee-wifi-flask-app'
    DOCKER_CONTAINER_NAME = 'my-coffee-wifi-flask-container'
    CONTAINER_PORT = 5008
    HOST_PORT = 80  // Change to desired host port if not using random
  }

  stages {
    stage('Build') {
      steps {
        script {
          docker.build(DOCKER_IMAGE_NAME)
        }
      }
    }
    stage('Test') {
      steps {
        script {
          docker.image(DOCKER_IMAGE_NAME).inside {
            sh 'python -m pytest app/tests/'
          }
        }
      }
    }
    stage('Deploy') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
            sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
            docker.withRegistry('', DOCKER_USERNAME, DOCKER_PASSWORD) {
              sh "docker push $DOCKER_IMAGE_NAME"
            }
            sh 'docker stop $DOCKER_CONTAINER_NAME || true'
            sh 'docker rm -f $DOCKER_CONTAINER_NAME || true'
            sh "docker run -d -p ${HOST_PORT}:${CONTAINER_PORT} --name $DOCKER_CONTAINER_NAME $DOCKER_IMAGE_NAME"
          }
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout'
    }
  }
}
