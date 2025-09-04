pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/keerthanatp"
        IMAGE = "twitter-bot"
    }

    stages {
        stage('Cleanup') {
            steps {
                deleteDir()  // wipes out everything in workspace
            }
        }
        stage('Checkout') {
    steps {
        checkout([$class: 'GitSCM',
            branches: [[name: '*/main']],
            userRemoteConfigs: [[url: 'https://github.com/Keerthana-T-P/on-this-day.git']],
            doGenerateSubmoduleConfigurations: false,
            extensions: [[$class: 'WipeWorkspace']]
        ])
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
