pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/keerthanatp"
        IMAGE = "twitter-bot"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Keerthana-T-P/on-this-day.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $REGISTRY/$IMAGE:latest ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withDockerRegistry([ credentialsId: 'docker-hub-creds', url: '' ]) {
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
