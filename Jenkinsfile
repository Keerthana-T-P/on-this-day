pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/<your-dockerhub-username>"
        IMAGE = "twitter-bot"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/<your-repo>.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $REGISTRY/$IMAGE:latest ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withDockerRegistry([ credentialsId: 'dockerhub-creds', url: '' ]) {
                    sh "docker push $REGISTRY/$IMAGE:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig-creds']) {
                    sh "kubectl apply -f deployment.yaml"
                }
            }
        }
    }
}
