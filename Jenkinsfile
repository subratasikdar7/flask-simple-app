pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  
        DOCKERHUB_REPO = "your-dockerhub-username/your-repo-name"
        IMAGE_TAG = "${env.BUILD_NUMBER}"  // or use 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                script {
                    sh """
                    echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh """
                    docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
                    docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${DOCKERHUB_REPO}:latest
                    docker push ${DOCKERHUB_REPO}:latest
                    """
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
